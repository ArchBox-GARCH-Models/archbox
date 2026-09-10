"""Shared machinery for the VaR / ES calculators.

Both :class:`~archbox.risk.var.ValueAtRisk` and
:class:`~archbox.risk.es.ExpectedShortfall` read the same series off a fitted
result object and resolve the same conditional distribution, so that logic
lives here once.

Result-object contract
----------------------
The calculators consume the public :class:`~archbox.core.results.ArchResults`
API and nothing else:

``resid``
    RAW residuals ``eps_t = r_t - mu``, on the scale of the returns.
``std_resid``
    Standardized residuals ``z_t = eps_t / sigma_t``.
``conditional_volatility``
    Conditional standard deviation ``sigma_t``.
``mu``
    Fitted mean of the return process.

The return series used by the historical methods is rebuilt as
``r_t = mu + eps_t``; nothing is ever read off ``endog`` (which is already
demeaned) or guessed through an attribute chain.

References
----------
- McNeil, A.J., Frey, R. & Embrechts, P. (2015).
  Quantitative Risk Management. 2nd ed. Princeton University Press.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy import stats

#: Fallback degrees of freedom, used only when Student-t measures are requested
#: on results that carry no fitted ``nu`` (e.g. a Gaussian GARCH fit).
DEFAULT_NU: float = 8.0

#: Number of grid points of the mid-point rule used to integrate the quantile
#: function of a non-analytic distribution over the tail (Expected Shortfall).
_ES_GRID: int = 2000

_NORMAL_ALIASES = frozenset({"normal", "gaussian", "norm"})
_STUDENTT_ALIASES = frozenset({"studentt", "student-t", "student", "t", "std"})


class RiskMeasure:
    """Common base for the VaR and ES calculators.

    Parameters
    ----------
    results : ArchResults
        Fitted model results (see the module docstring for the attributes that
        are read). An :class:`~archbox.risk.ewma.EWMAResult` is also accepted.
    alpha : float
        Tail probability (e.g. 0.05 for 95% VaR/ES). Default is 0.05.

    Attributes
    ----------
    results : ArchResults
        The fitted model results.
    alpha : float
        Tail probability.
    mu : float
        Fitted mean of the return process.
    resid : NDArray[np.float64]
        Raw residuals ``eps_t``, on the return scale.
    returns : NDArray[np.float64]
        Return series ``r_t = mu + eps_t``, on the return scale.
    std_resid : NDArray[np.float64]
        Standardized residuals ``z_t = eps_t / sigma_t``.
    conditional_volatility : NDArray[np.float64]
        Conditional volatility ``sigma_t``.
    """

    def __init__(self, results: Any, alpha: float = 0.05) -> None:
        """Extract the residual/volatility series from fitted model results."""
        if not 0 < alpha < 1:
            msg = f"alpha must be in (0, 1), got {alpha}"
            raise ValueError(msg)

        self.results = results
        self.alpha = float(alpha)

        missing = [
            name
            for name in ("conditional_volatility", "mu")
            if getattr(results, name, None) is None
        ]
        if missing:
            msg = (
                f"{type(results).__name__} does not expose the fitted-model risk API "
                f"(missing: {', '.join(missing)}). Pass the ArchResults returned by "
                f"model.fit()."
            )
            raise TypeError(msg)

        sigma = np.asarray(results.conditional_volatility, dtype=np.float64).ravel()
        self.conditional_volatility = sigma
        self.mu = float(results.mu)

        # ``resid`` is the raw residual eps_t (ArchResults); ``resids`` is the
        # equivalent name on EWMAResult.
        raw = getattr(results, "resid", None)
        if raw is None:
            raw = getattr(results, "resids", None)
        if raw is None:
            msg = (
                f"{type(results).__name__} exposes no raw residuals ('resid'). "
                f"Pass the ArchResults returned by model.fit()."
            )
            raise TypeError(msg)
        self.resid = np.asarray(raw, dtype=np.float64).ravel()

        if len(self.resid) != len(sigma):
            msg = (
                f"resid and conditional_volatility must have the same length, "
                f"got {len(self.resid)} and {len(sigma)}"
            )
            raise ValueError(msg)

        # Returns on their original scale (the historical methods quantile these).
        self.returns = self.mu + self.resid

        std = getattr(results, "std_resid", None)
        if std is None:
            std = self.resid / np.maximum(sigma, 1e-12)
        self.std_resid = np.asarray(std, dtype=np.float64).ravel()

    # --- Fitted distribution -------------------------------------------------

    def _fitted_distribution(self) -> Any | None:
        """Distribution instance carrying the fitted shape parameters.

        Returns
        -------
        Distribution or None
            ``results._fitted_dist()`` when the results expose it (an
            ``ArchResults``), otherwise ``None``.
        """
        builder = getattr(self.results, "_fitted_dist", None)
        if callable(builder):
            return builder()
        return None

    def _fitted_shape_param(self, name: str) -> float | None:
        """Fitted value of a named distribution shape parameter.

        Reads the trailing distribution block ``results._dist_params`` and
        matches it against the shape-parameter names declared by the fitted
        distribution.

        Parameters
        ----------
        name : str
            Shape-parameter name, e.g. ``'nu'``.

        Returns
        -------
        float or None
            The fitted value, or ``None`` when the model carries no such
            parameter.
        """
        values = np.asarray(getattr(self.results, "_dist_params", []), dtype=np.float64).ravel()
        model = getattr(self.results, "_model", None)
        dist = getattr(model, "dist", None)
        names = list(getattr(dist, "param_names", []))
        if values.size == 0 or len(names) != values.size:
            return None
        for param_name, value in zip(names, values, strict=True):
            if param_name == name:
                return float(value)
        return None

    def _resolve_distribution(
        self,
        dist: str | None,
        nu: float | None,
    ) -> tuple[str, Any, float]:
        """Resolve the conditional distribution used by the parametric measures.

        Parameters
        ----------
        dist : str or None
            Distribution name. ``None`` means "the distribution the model was
            fitted with", including its estimated shape parameters.
        nu : float or None
            Explicit degrees-of-freedom override for Student-t. ``None`` means
            "use the fitted ``nu``".

        Returns
        -------
        tuple
            ``(kind, distribution, nu)`` where ``kind`` is ``'normal'``,
            ``'studentt'`` or ``'other'``. ``distribution`` is the resolved
            :class:`~archbox.distributions.base.Distribution` instance (only
            used when ``kind == 'other'``) and ``nu`` the resolved degrees of
            freedom (``nan`` unless ``kind == 'studentt'``).
        """
        if dist is None and nu is not None:
            # An explicit nu with no name is a Student-t request.
            dist = "studentt"

        if dist is None:
            fitted = self._fitted_distribution()
            if fitted is None:
                return ("normal", None, float("nan"))
            name = str(getattr(fitted, "name", "")).strip().lower()
            if name in ("normal", "gaussian"):
                return ("normal", fitted, float("nan"))
            if name in ("student-t", "studentt"):
                fitted_nu = self._fitted_shape_param("nu")
                if fitted_nu is not None:
                    return ("studentt", fitted, self._validate_nu(fitted_nu))
            return ("other", fitted, float("nan"))

        key = str(dist).strip().lower().replace("_", "-").replace(" ", "-")
        if key in _NORMAL_ALIASES:
            return ("normal", None, float("nan"))
        if key in _STUDENTT_ALIASES:
            resolved = nu if nu is not None else self._fitted_shape_param("nu")
            if resolved is None:
                resolved = DEFAULT_NU
            return ("studentt", None, self._validate_nu(resolved))

        return ("other", self._build_named_distribution(key), float("nan"))

    def _build_named_distribution(self, key: str) -> Any:
        """Build a distribution from a name, preferring the fitted instance.

        Parameters
        ----------
        key : str
            Normalized distribution name (lower case, dashes).

        Returns
        -------
        Distribution
            The fitted distribution when it is of the requested type (so its
            estimated shape parameters are used), otherwise a fresh instance
            with default shape parameters.

        Raises
        ------
        ValueError
            If the name is not a known distribution.
        """
        from archbox.core.volatility_model import VolatilityModel

        try:
            built = VolatilityModel._build_distribution(key)
        except ValueError:
            msg = (
                f"Unknown distribution: {key}. Use 'normal', 'studentt', 'skewed-t', "
                f"'ged', 'mixture-normal', or None for the fitted distribution."
            )
            raise ValueError(msg) from None

        fitted = self._fitted_distribution()
        if fitted is not None and type(fitted) is type(built):
            return fitted
        return built

    @staticmethod
    def _validate_nu(nu: float) -> float:
        """Validate Student-t degrees of freedom.

        Parameters
        ----------
        nu : float
            Degrees of freedom.

        Returns
        -------
        float
            The validated value.

        Raises
        ------
        ValueError
            If ``nu <= 2`` (the standardized Student-t has no variance there).
        """
        value = float(nu)
        if value <= 2:
            msg = f"Degrees of freedom must be > 2, got {value}"
            raise ValueError(msg)
        return value

    # --- Standardized tail functionals --------------------------------------

    def innovation_quantile(self, dist: str | None = None, nu: float | None = None) -> float:
        """alpha-quantile of the standardized innovation distribution.

        Useful to turn a *forecast* volatility into a VaR out of sample:
        ``VaR = mu + sigma_forecast * innovation_quantile()``.

        Parameters
        ----------
        dist : str, optional
            Distribution name; ``None`` (default) uses the fitted one.
        nu : float, optional
            Student-t degrees of freedom override.

        Returns
        -------
        float
            ``F^{-1}(alpha)`` for a zero-mean, unit-variance innovation.
        """
        return self._standardized_quantile(dist, nu)

    def innovation_tail_mean(self, dist: str | None = None, nu: float | None = None) -> float:
        """Mean of the standardized innovation below its alpha-quantile.

        Turns a *forecast* volatility into an ES out of sample:
        ``ES = mu + sigma_forecast * innovation_tail_mean()``.

        Parameters
        ----------
        dist : str, optional
            Distribution name; ``None`` (default) uses the fitted one.
        nu : float, optional
            Student-t degrees of freedom override.

        Returns
        -------
        float
            ``E[z | z <= F^{-1}(alpha)]`` (negative).
        """
        return self._standardized_tail_mean(dist, nu)

    def _standardized_quantile(self, dist: str | None, nu: float | None) -> float:
        """alpha-quantile of the standardized innovation z_t (unit variance).

        Parameters
        ----------
        dist : str or None
            Distribution name, or ``None`` for the fitted distribution.
        nu : float or None
            Student-t degrees of freedom override.

        Returns
        -------
        float
            ``F^{-1}(alpha)`` for a zero-mean, unit-variance innovation.
        """
        kind, distribution, nu_value = self._resolve_distribution(dist, nu)
        if kind == "normal":
            return float(stats.norm.ppf(self.alpha))
        if kind == "studentt":
            scale = np.sqrt((nu_value - 2.0) / nu_value)
            return float(stats.t.ppf(self.alpha, df=nu_value) * scale)
        return float(distribution.ppf(self.alpha))

    def _standardized_tail_mean(self, dist: str | None, nu: float | None) -> float:
        """Mean of the standardized innovation below its alpha-quantile.

        ``E[z | z <= F^{-1}(alpha)] = (1/alpha) * int_0^alpha F^{-1}(u) du``.

        Parameters
        ----------
        dist : str or None
            Distribution name, or ``None`` for the fitted distribution.
        nu : float or None
            Student-t degrees of freedom override.

        Returns
        -------
        float
            The tail mean (negative), on the standardized scale.
        """
        kind, distribution, nu_value = self._resolve_distribution(dist, nu)
        alpha = self.alpha

        if kind == "normal":
            z_alpha = float(stats.norm.ppf(alpha))
            return -float(stats.norm.pdf(z_alpha)) / alpha

        if kind == "studentt":
            # McNeil et al. (2015), eq. (2.26), rescaled to unit variance.
            t_alpha = float(stats.t.ppf(alpha, df=nu_value))
            f_nu = float(stats.t.pdf(t_alpha, df=nu_value))
            scale = np.sqrt((nu_value - 2.0) / nu_value)
            factor = (f_nu / alpha) * ((nu_value + t_alpha**2) / (nu_value - 1.0))
            return -float(factor * scale)

        # Generic distribution: mid-point rule on the quantile function, which
        # never evaluates F^{-1}(0).
        grid = (np.arange(_ES_GRID, dtype=np.float64) + 0.5) / _ES_GRID * alpha
        values = np.asarray(distribution.ppf(grid), dtype=np.float64)
        return float(np.mean(values))

    # --- Monte-Carlo simulation ---------------------------------------------

    def _simulate_future_returns(
        self,
        n_sims: int,
        horizon: int,
        seed: int | None,
    ) -> NDArray[np.float64]:
        """Simulate future returns from the fitted model.

        The paths start from the end of the estimation sample: the one-step
        conditional variance comes from the model's own multi-step recursion
        (``VolatilityModel.forecast_variance``) and the innovations are drawn
        from the *fitted* conditional distribution (Student-t, GED, skewed-t,
        ... - not necessarily N(0, 1)).

        For ``horizon == 1`` the whole computation is vectorised over paths
        (the one-step-ahead variance is deterministic given the sample). For
        multi-step horizons each path iterates the model's own simulation
        recursion (``_simulate_next_variance``), so the variance is
        path-dependent instead of collapsing onto its conditional expectation.

        Parameters
        ----------
        n_sims : int
            Number of simulated paths.
        horizon : int
            Number of steps ahead.
        seed : int, optional
            Random seed.

        Returns
        -------
        NDArray[np.float64]
            Simulated returns, shape ``(n_sims, horizon)``, on the return scale
            (the mean ``mu`` is included).

        Raises
        ------
        TypeError
            If the results do not come from a fitted archbox volatility model.
        ValueError
            If ``n_sims`` or ``horizon`` is not a positive integer.
        """
        from archbox.core.volatility_model import VolatilityModel

        n_sims = int(n_sims)
        horizon = int(horizon)
        if n_sims < 1:
            msg = f"n_sims must be a positive integer, got {n_sims}"
            raise ValueError(msg)
        if horizon < 1:
            msg = f"horizon must be a positive integer, got {horizon}"
            raise ValueError(msg)

        model = getattr(self.results, "_model", None)
        if not isinstance(model, VolatilityModel):
            msg = (
                f"monte_carlo requires results from a fitted archbox volatility model "
                f"(ArchResults returned by model.fit()); got {type(self.results).__name__}."
            )
            raise TypeError(msg)

        params = np.asarray(self.results.params, dtype=np.float64).ravel()
        var_params = np.asarray(
            getattr(self.results, "_var_params", params[: model.num_params]),
            dtype=np.float64,
        )
        shape_params = getattr(self.results, "_shape_params", None)
        if shape_params is not None:
            shape_params = np.asarray(shape_params, dtype=np.float64).ravel()
            if shape_params.size == 0:
                shape_params = None

        sigma2_hist = np.asarray(
            getattr(self.results, "_sigma2", self.conditional_volatility**2),
            dtype=np.float64,
        ).ravel()

        rng = np.random.default_rng(seed)
        z = model._simulate_innovations(n_sims * horizon, rng, shape_params)
        z = np.asarray(z, dtype=np.float64).reshape(n_sims, horizon)

        sigma2 = np.empty((n_sims, horizon), dtype=np.float64)
        eps = np.empty((n_sims, horizon), dtype=np.float64)

        if horizon == 1:
            # The one-step-ahead variance is known at T: no path recursion.
            sigma2_next = float(
                model.forecast_variance(var_params, self.resid, sigma2_hist, 1, shape_params)[0]
            )
            sigma2[:, 0] = sigma2_next
            eps[:, 0] = np.sqrt(max(sigma2_next, 1e-12)) * z[:, 0]
        else:
            self._simulate_variance_paths(model, var_params, sigma2_hist, z, sigma2, eps)

        offsets = self._mean_offsets(model, var_params, sigma2)
        return self.mu + eps + offsets

    def _simulate_variance_paths(
        self,
        model: Any,
        var_params: NDArray[np.float64],
        sigma2_hist: NDArray[np.float64],
        z: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        eps: NDArray[np.float64],
    ) -> None:
        """Iterate the model's simulation recursion path by path (in place).

        The recursion is seeded with the tail of the in-sample residual and
        variance path, so the first simulated step continues the fitted
        history instead of restarting from the unconditional variance.

        Parameters
        ----------
        model : VolatilityModel
            The fitted model (supplies the recursion).
        var_params : ndarray
            Variance block of the fitted parameters.
        sigma2_hist : ndarray
            In-sample conditional variance path.
        z : ndarray
            Innovations, shape ``(n_sims, horizon)``.
        sigma2 : ndarray
            Output buffer for the simulated variances, shape ``(n_sims, horizon)``.
        eps : ndarray
            Output buffer for the simulated shocks, shape ``(n_sims, horizon)``.
        """
        n_sims, horizon = z.shape
        backcast = float(sigma2_hist[-1])

        # Lags of the in-sample history the recursion may reach back into.
        needed = 1
        for attr in ("p", "q", "truncation_lag"):
            value = getattr(model, attr, 0)
            if isinstance(value, (int, np.integer)):
                needed = max(needed, int(value))
        n_hist = int(min(len(self.resid), needed))

        buf_eps = np.empty(n_hist + horizon, dtype=np.float64)
        buf_s2 = np.empty(n_hist + horizon, dtype=np.float64)
        buf_eps[:n_hist] = self.resid[len(self.resid) - n_hist :]
        buf_s2[:n_hist] = sigma2_hist[len(sigma2_hist) - n_hist :]

        for i in range(n_sims):
            state = model._simulate_state(var_params, backcast)
            for h in range(horizon):
                t = n_hist + h
                s2 = float(
                    model._simulate_next_variance(var_params, buf_eps, buf_s2, t, backcast, state)
                )
                shock = np.sqrt(max(s2, 1e-12)) * float(z[i, h])
                buf_s2[t] = s2
                buf_eps[t] = shock
                sigma2[i, h] = s2
                eps[i, h] = shock

    @staticmethod
    def _mean_offsets(
        model: Any,
        var_params: NDArray[np.float64],
        sigma2: NDArray[np.float64],
    ) -> NDArray[np.float64] | float:
        """In-mean contribution added to the simulated returns.

        Zero for every model except GARCH-M, where the return carries a risk
        premium that depends on the simulated conditional variance.

        Parameters
        ----------
        model : VolatilityModel
            The fitted model.
        var_params : ndarray
            Variance block of the fitted parameters.
        sigma2 : ndarray
            Simulated variances, shape ``(n_sims, horizon)``.

        Returns
        -------
        ndarray or float
            ``0.0`` when the model has no in-mean term, otherwise an array
            shaped like ``sigma2``.
        """
        from archbox.core.volatility_model import VolatilityModel

        if type(model)._simulate_mean_offset is VolatilityModel._simulate_mean_offset:
            return 0.0

        flat = sigma2.ravel()
        # The first column is constant across paths for horizon == 1; the
        # generic elementwise evaluation stays correct in every case.
        offsets = np.array(
            [model._simulate_mean_offset(var_params, float(value)) for value in flat],
            dtype=np.float64,
        )
        return offsets.reshape(sigma2.shape)
