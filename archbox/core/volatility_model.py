"""Base class for volatility models."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, NamedTuple

import numpy as np
from numpy.typing import NDArray

from archbox.utils.validation import validate_positive_integer, validate_returns

if TYPE_CHECKING:
    from archbox.distributions.base import Distribution


class SimulationResult(NamedTuple):
    """Output of :meth:`VolatilityModel.simulate`.

    A plain 2-tuple ``(returns, variance)``, so ``r, s2 = model.simulate(...)``
    and ``result[0]`` keep working; ``.volatility`` is offered as a convenience
    for the square root.

    Attributes
    ----------
    returns : ndarray
        Simulated returns, shape (n,).
    variance : ndarray
        Simulated conditional variance sigma^2_t, shape (n,).
    """

    returns: NDArray[np.float64]
    variance: NDArray[np.float64]

    @property
    def volatility(self) -> NDArray[np.float64]:
        """Conditional volatility sigma_t (square root of ``variance``)."""
        return np.sqrt(self.variance)


class VolatilityModel(ABC):
    """Abstract base class for volatility models.

    All volatility models (GARCH, EGARCH, GJR-GARCH, etc.) inherit from this class.

    Parameters
    ----------
    endog : array-like
        Time series of returns.
    mean : str
        Mean model: 'constant' (demean) or 'zero'.
    dist : str
        Conditional distribution: 'normal', 'studentt', 'skewt'.

    Attributes
    ----------
    endog : NDArray[np.float64]
        Returns (demeaned if mean='constant').
    nobs : int
        Number of observations.
    dist : Distribution
        Conditional distribution instance.
    volatility_process : str
        Name of the volatility process.
    mu : float
        Mean removed from the returns before the variance recursion
        (0 if mean='zero').

    Notes
    -----
    The constant mean is handled in two steps: ``mu`` is the **sample mean** of
    the returns and only the variance (and distribution) parameters enter the
    likelihood maximised by :meth:`fit`. R's ``rugarch`` instead estimates
    ``mu`` jointly with the variance parameters, which effectively weights each
    observation by ``1 / sigma_t^2``. On a series whose mean is close to zero
    the two estimators can disagree by more than their own magnitude - on the
    bundled ``sp500`` series ``mu`` is ``-1.32e-4`` here against ``4e-4`` in the
    rugarch reference - while the variance parameters, the persistence and the
    log-likelihood still agree to well within the validation tolerances (see
    ``tests/validation/test_vs_rugarch.py``). ``ArchResults.resid`` is always
    ``endog``, i.e. the returns with this ``mu`` already removed.
    """

    volatility_process: str = "Unknown"

    #: Whether ``fit(variance_targeting=True)`` is supported. Targeting rebuilds
    #: ``omega`` from ``var * (1 - persistence)``, which assumes the plain GARCH
    #: layout ``[omega, alpha_1..q, beta_1..p]``; models with any other layout
    #: must leave this ``False`` so the estimator raises instead of silently
    #: reconstructing a meaningless ``omega``.
    supports_variance_targeting: bool = False

    def __init__(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str | Distribution = "normal",
    ) -> None:
        """Initialize the volatility model with returns and options."""
        raw = validate_returns(endog)

        self.mean_model = mean
        if mean == "constant":
            self.mu = float(np.mean(raw))
            self.endog = raw - self.mu
        elif mean == "zero":
            self.mu = 0.0
            self.endog = raw.copy()
        else:
            msg = f"Unknown mean model: {mean}. Use 'constant' or 'zero'."
            raise ValueError(msg)

        self.nobs = len(self.endog)
        self.dist: Distribution = self._build_distribution(dist)
        self._dist_name = dist if isinstance(dist, str) else self.dist.name
        self._is_fitted = False

    @staticmethod
    def _build_distribution(dist: str | Distribution) -> Distribution:
        """Build a distribution instance from a name or an existing instance.

        Parameters
        ----------
        dist : str or Distribution
            Either a (possibly aliased) distribution name such as ``'studentt'``
            or an already-constructed :class:`~archbox.distributions.base.Distribution`
            (e.g. ``StudentT(nu=5.0)`` to fix the shape parameter).

        Returns
        -------
        Distribution
            The distribution instance to use for the likelihood.
        """
        from archbox.distributions.base import Distribution as _Distribution
        from archbox.distributions.ged import GeneralizedError
        from archbox.distributions.mixture_normal import MixtureNormal
        from archbox.distributions.normal import Normal
        from archbox.distributions.skewed_t import SkewedT
        from archbox.distributions.student_t import StudentT

        if isinstance(dist, _Distribution):
            return dist

        normalized = dist.strip().lower().replace("_", "-").replace(" ", "-")

        mapping: dict[str, type[Distribution]] = {
            "normal": Normal,
            "gaussian": Normal,
            "norm": Normal,
            "student-t": StudentT,
            "studentt": StudentT,
            "student": StudentT,
            "t": StudentT,
            "std": StudentT,
            "skewed-t": SkewedT,
            "skewt": SkewedT,
            "skew-t": SkewedT,
            "skewstudent": SkewedT,
            "sstd": SkewedT,
            "ged": GeneralizedError,
            "generalized-error": GeneralizedError,
            "generalised-error": GeneralizedError,
            "mixture-normal": MixtureNormal,
            "mixture": MixtureNormal,
            "normalmix": MixtureNormal,
            "mixturenormal": MixtureNormal,
        }

        cls = mapping.get(normalized)
        if cls is None:
            canonical = "normal, student-t, skewed-t, ged, mixture-normal"
            msg = f"Unknown distribution: {dist!r}. Available: {canonical}."
            raise ValueError(msg)
        return cls()

    # --- Abstract methods (subclass MUST implement) ---

    @abstractmethod
    def _variance_recursion(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series.

        Parameters
        ----------
        params : ndarray
            Model parameters (omega, alpha, beta, ...).
        resids : ndarray
            Residuals (eps_t = r_t - mu).
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance series sigma^2_t, shape (T,).
        """

    @property
    @abstractmethod
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values for optimization."""

    @property
    @abstractmethod
    def param_names(self) -> list[str]:
        """Parameter names."""

    @abstractmethod
    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform unconstrained parameters to constrained space."""

    @abstractmethod
    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform constrained parameters to unconstrained space."""

    @abstractmethod
    def bounds(self) -> list[tuple[float, float]]:
        """Parameter bounds for optimizer [(lower, upper), ...]."""

    @property
    @abstractmethod
    def num_params(self) -> int:
        """Number of model parameters."""

    # --- Composite (variance + distribution) parameter helpers ---

    @property
    def n_total_params(self) -> int:
        """Total number of free parameters (variance + distribution)."""
        return self.num_params + self.dist.num_params

    def full_start_params(self) -> NDArray[np.float64]:
        """Starting values for the combined [variance, dist] vector."""
        return np.concatenate([self.start_params, self.dist.start_params()])

    def full_param_names(self) -> list[str]:
        """Combined [variance, dist] parameter names."""
        return list(self.param_names) + list(self.dist.param_names)

    def full_bounds(self) -> list[tuple[float, float]]:
        """Combined [variance, dist] parameter bounds."""
        return list(self.bounds()) + list(self.dist.bounds())

    def full_transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform combined [variance, dist] params to constrained space."""
        nv = self.num_params
        return np.concatenate(
            [
                self.transform_params(unconstrained[:nv]),
                self.dist.transform_params(unconstrained[nv:]),
            ]
        )

    def full_untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform combined [variance, dist] params to unconstrained space."""
        nv = self.num_params
        return np.concatenate(
            [
                self.untransform_params(constrained[:nv]),
                self.dist.untransform_params(constrained[nv:]),
            ]
        )

    # --- Model-level moments and forecasts ---
    #
    # These four methods form the public model-level API that ``ArchResults``
    # delegates to.  ``var_params`` is always the *leading* block of the fitted
    # parameter vector (length ``self.num_params``); distribution shape
    # parameters are passed separately as ``dist_params``.
    #
    # The defaults below implement the plain GARCH(p, q) layout
    # ``[omega, alpha_1..alpha_q, beta_1..beta_p]``.  Models with a different
    # layout or different dynamics override the relevant pieces.

    def _arch_garch_blocks(
        self, var_params: NDArray[np.float64]
    ) -> tuple[float, NDArray[np.float64], NDArray[np.float64]]:
        """Split a GARCH-layout parameter vector into (omega, alphas, betas).

        Parameters
        ----------
        var_params : ndarray
            Leading (variance) block of the parameter vector.

        Returns
        -------
        tuple
            ``(omega, alphas, betas)``.
        """
        nv = self.num_params
        q = int(getattr(self, "q", 1))
        omega = float(var_params[0])
        alphas = np.asarray(var_params[1 : 1 + q], dtype=np.float64)
        betas = np.asarray(var_params[1 + q : nv], dtype=np.float64)
        return omega, alphas, betas

    def persistence(
        self,
        var_params: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> float:
        """Variance persistence implied by ``var_params``.

        The default is the GARCH measure ``sum(alpha) + sum(beta)``.

        Parameters
        ----------
        var_params : ndarray
            Leading (variance) block of the parameter vector.
        dist_params : ndarray, optional
            Fitted distribution shape parameters. Only used by models whose
            persistence depends on the innovation law (e.g. APARCH).

        Returns
        -------
        float
            Persistence. Values >= 1 indicate a non-stationary variance process.
        """
        del dist_params
        params = np.asarray(var_params, dtype=np.float64)
        _, alphas, betas = self._arch_garch_blocks(params)
        return float(np.sum(alphas) + np.sum(betas))

    def unconditional_variance(
        self,
        var_params: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> float:
        """Long-run (unconditional) variance implied by ``var_params``.

        Parameters
        ----------
        var_params : ndarray
            Leading (variance) block of the parameter vector.
        dist_params : ndarray, optional
            Fitted distribution shape parameters (see ``persistence``).

        Returns
        -------
        float
            ``omega / (1 - persistence)``, or ``inf`` when persistence >= 1.
        """
        params = np.asarray(var_params, dtype=np.float64)
        pers = self.persistence(params, dist_params)
        if not np.isfinite(pers) or pers >= 1.0:
            return float("inf")
        omega, _, _ = self._arch_garch_blocks(params)
        return float(omega / (1.0 - pers))

    def conditional_variance(
        self,
        params: NDArray[np.float64],
        backcast: float | None = None,
    ) -> NDArray[np.float64]:
        """Conditional variance path consistent with the log-likelihood.

        Parameters
        ----------
        params : ndarray
            Full or variance-only parameter vector; only the leading
            ``num_params`` entries are used.
        backcast : float, optional
            Initial variance. Computed from the data when omitted.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t, shape (T,).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        var_params = np.asarray(params, dtype=np.float64)[: self.num_params]
        sigma2 = self._variance_recursion(var_params, self.endog, float(backcast))
        return np.maximum(np.asarray(sigma2, dtype=np.float64), 1e-12)

    def forecast_variance(
        self,
        var_params: NDArray[np.float64],
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        horizon: int = 1,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Multi-step conditional variance forecast.

        The default implements the exact GARCH(p, q) recursion, replacing
        unobserved future squared shocks by their conditional expectation
        ``E[eps^2_{T+k}] = sigma^2_{T+k}``.

        Parameters
        ----------
        var_params : ndarray
            Leading (variance) block of the parameter vector.
        resids : ndarray
            In-sample residuals used to seed the recursion.
        sigma2 : ndarray
            In-sample conditional variance path.
        horizon : int
            Number of steps ahead (>= 1).
        dist_params : ndarray, optional
            Fitted distribution shape parameters (unused by the GARCH default).

        Returns
        -------
        ndarray
            Forecast variances, shape ``(horizon,)``, strictly positive.
        """
        h_max = validate_positive_integer(horizon, "horizon")
        params = np.asarray(var_params, dtype=np.float64)
        omega, alphas, betas = self._arch_garch_blocks(params)
        q = len(alphas)
        p = len(betas)

        sigma2_arr = np.asarray(sigma2, dtype=np.float64).ravel()
        resid_arr = np.asarray(resids, dtype=np.float64).ravel()
        fill = float(sigma2_arr[-1]) if sigma2_arr.size else self._backcast(self.endog)

        eps2_hist = list(self._tail(resid_arr**2, q, fill))
        s2_hist = list(self._tail(sigma2_arr, p, fill))

        out = np.empty(h_max, dtype=np.float64)
        for h in range(h_max):
            value = omega
            for i in range(q):
                value += alphas[i] * eps2_hist[-1 - i]
            for j in range(p):
                value += betas[j] * s2_hist[-1 - j]
            value = max(float(value), 1e-12)
            out[h] = value
            # E[eps^2_{T+h}] = sigma^2_{T+h} for the next iteration.
            eps2_hist.append(value)
            s2_hist.append(value)
        return out

    # --- Forecast helpers shared by subclasses ---

    @staticmethod
    def _tail(values: NDArray[np.float64], n: int, fill: float) -> NDArray[np.float64]:
        """Last ``n`` entries of ``values``, left-padded with ``fill``.

        Parameters
        ----------
        values : ndarray
            Source series.
        n : int
            Number of trailing entries required.
        fill : float
            Padding value used when ``values`` is shorter than ``n``.

        Returns
        -------
        ndarray
            Array of length ``max(n, 0)``, oldest entry first.
        """
        arr = np.asarray(values, dtype=np.float64).ravel()
        if n <= 0:
            return np.empty(0, dtype=np.float64)
        if len(arr) >= n:
            return np.array(arr[-n:], dtype=np.float64)
        pad = np.full(n - len(arr), float(fill), dtype=np.float64)
        return np.concatenate([pad, arr])

    def _simulate_innovations(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Draw ``n`` standardized innovations from the fitted distribution.

        Parameters
        ----------
        n : int
            Number of draws.
        rng : numpy.random.Generator
            Random generator (seeded by the caller for reproducibility).
        dist_params : ndarray, optional
            Fitted shape parameters; ``None`` uses the distribution defaults.

        Returns
        -------
        ndarray
            Draws z_t with mean 0 and variance 1, shape (n,).
        """
        shape: NDArray[np.float64] | None = None
        if dist_params is not None:
            arr = np.asarray(dist_params, dtype=np.float64).ravel()
            if arr.size:
                shape = arr
        return np.asarray(self.dist.simulate(n, rng, shape), dtype=np.float64)

    # --- Concrete methods ---

    def fit(
        self,
        method: str = "mle",
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        disp: bool = True,
    ) -> Any:
        """Fit the model via Maximum Likelihood Estimation.

        Parameters
        ----------
        method : str
            Estimation method. Currently only 'mle'.
        starting_values : ndarray, optional
            Custom starting values. If None, uses self.start_params.
        variance_targeting : bool
            If True, fix omega = var * (1 - persistence).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ArchResults
            Fitted model results.
        """
        from archbox.estimation.mle import MLEstimator

        estimator = MLEstimator()
        results = estimator.fit(
            model=self,
            starting_values=starting_values,
            variance_targeting=variance_targeting,
            disp=disp,
        )
        self._is_fitted = True
        return results

    def loglike(self, params: NDArray[np.float64], backcast: float | None = None) -> float:
        """Compute log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance. If None, computed from data.

        Returns
        -------
        float
            Total log-likelihood.
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        nv = self.num_params
        var_params = params[:nv]
        dist_params = params[nv:]
        sigma2 = self._variance_recursion(var_params, self.endog, backcast)
        # Ensure positivity. `_variance_recursion` always returns a freshly
        # allocated array, so the floor is applied in place: this is the hot
        # path of every fit and the copy is pure overhead.
        np.maximum(sigma2, 1e-12, out=sigma2)
        ll_per_obs = self.dist.loglikelihood(self.endog, sigma2, dist_params)
        return float(np.sum(ll_per_obs))

    def loglike_per_obs(
        self, params: NDArray[np.float64], backcast: float | None = None
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        backcast : float, optional
            Initial variance.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        if backcast is None:
            backcast = self._backcast(self.endog)
        nv = self.num_params
        var_params = params[:nv]
        dist_params = params[nv:]
        sigma2 = self._variance_recursion(var_params, self.endog, backcast)
        np.maximum(sigma2, 1e-12, out=sigma2)
        return self.dist.loglikelihood(self.endog, sigma2, dist_params)

    # --- Simulation hooks -------------------------------------------------
    #
    # ``simulate`` runs a single O(n) forward pass: at date ``t`` it asks the
    # model for sigma^2_t given the shocks and variances already generated for
    # dates < t.  Models whose recursion is not the plain GARCH(p, q) one
    # override ``_simulate_next_variance`` (and, when the recursion carries
    # extra state such as the Component-GARCH q_t/h_t split, ``_simulate_state``).

    def _simulate_state(
        self,
        var_params: NDArray[np.float64],
        backcast: float,
    ) -> dict[str, Any]:
        """Mutable state carried across simulation steps.

        Parameters
        ----------
        var_params : ndarray
            Variance block of the parameter vector.
        backcast : float
            Initial variance used for date 0 and for pre-sample lags.

        Returns
        -------
        dict
            Empty by default; models with hidden state override this.
        """
        del var_params, backcast
        return {}

    def _simulate_next_variance(
        self,
        var_params: NDArray[np.float64],
        eps: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        t: int,
        backcast: float,
        state: dict[str, Any],
    ) -> float:
        """One simulation step: sigma^2_t from the already-simulated history.

        The default implements the GARCH(p, q) recursion
        ``sigma^2_t = omega + sum_i alpha_i eps^2_{t-i} + sum_j beta_j sigma^2_{t-j}``
        with pre-sample lags replaced by ``backcast``.

        Parameters
        ----------
        var_params : ndarray
            Variance block of the parameter vector.
        eps : ndarray
            Full shock array; entries ``0..t-1`` are filled.
        sigma2 : ndarray
            Full variance array; entries ``0..t-1`` are filled.
        t : int
            Current date (>= 1).
        backcast : float
            Pre-sample variance.
        state : dict
            Mutable per-model state (see ``_simulate_state``).

        Returns
        -------
        float
            sigma^2_t, strictly positive.
        """
        del state
        omega, alphas, betas = self._arch_garch_blocks(var_params)
        value = float(omega)
        for i in range(len(alphas)):
            lag = t - 1 - i
            value += float(alphas[i]) * (float(eps[lag]) ** 2 if lag >= 0 else backcast)
        for j in range(len(betas)):
            lag = t - 1 - j
            value += float(betas[j]) * (float(sigma2[lag]) if lag >= 0 else backcast)
        return max(value, 1e-12)

    def _simulate_mean_offset(
        self,
        var_params: NDArray[np.float64],
        sigma2_t: float,
    ) -> float:
        """In-mean contribution added to the simulated return at date ``t``.

        Zero for every model except GARCH-M, where the return carries the risk
        premium ``lambda f(sigma^2_t)`` on top of the shock.

        Parameters
        ----------
        var_params : ndarray
            Variance block of the parameter vector.
        sigma2_t : float
            Conditional variance at date ``t``.

        Returns
        -------
        float
            Mean offset (0.0 by default).
        """
        del var_params, sigma2_t
        return 0.0

    def simulate(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> SimulationResult:
        """Simulate returns and conditional variance from the model.

        A single O(n) forward pass: ``sigma^2_t`` is built from the shocks and
        variances simulated for earlier dates (see ``_simulate_next_variance``),
        then ``eps_t = sigma_t z_t`` with ``z_t`` drawn from the model's own
        conditional distribution using the shape parameters in ``params``
        (Student-t, GED, skewed-t, ... - not always N(0, 1)).

        Date 0 is initialised at the unconditional variance implied by
        ``params`` when it exists, otherwise at the sample variance.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Full parameter vector ``[variance block, distribution block]``.
            A variance-only vector is also accepted.
        seed : int, optional
            Random seed.

        Returns
        -------
        SimulationResult
            Named 2-tuple ``(returns, variance)``, each of shape (n,); the
            variance is the sigma^2_t path that generated the returns
            (``result.volatility`` gives sigma_t).
        """
        n_obs = validate_positive_integer(n, "n")
        rng = np.random.default_rng(seed)

        all_params = np.asarray(params, dtype=np.float64).ravel()
        nv = self.num_params
        var_params = all_params[:nv]
        dist_block = all_params[nv:]
        shape_params = dist_block if dist_block.size else None
        z = self._simulate_innovations(n_obs, rng, shape_params)

        backcast = self.unconditional_variance(var_params, shape_params)
        if not np.isfinite(backcast) or backcast <= 0.0:
            backcast = float(np.var(self.endog)) if self.nobs > 0 else 1.0
        if not np.isfinite(backcast) or backcast <= 0.0:
            backcast = 1.0

        sigma2 = np.empty(n_obs, dtype=np.float64)
        eps = np.empty(n_obs, dtype=np.float64)
        returns = np.empty(n_obs, dtype=np.float64)
        state = self._simulate_state(var_params, backcast)

        for t in range(n_obs):
            if t == 0:
                sigma2[0] = backcast
            else:
                sigma2[t] = self._simulate_next_variance(
                    var_params, eps, sigma2, t, backcast, state
                )
            eps[t] = np.sqrt(max(float(sigma2[t]), 1e-12)) * z[t]
            returns[t] = eps[t] + self._simulate_mean_offset(var_params, float(sigma2[t]))

        return SimulationResult(returns, sigma2)

    def _backcast(self, resids: NDArray[np.float64]) -> float:
        """Compute backcast value for variance initialization.

        Uses exponential weighted moving average of squared residuals.

        Parameters
        ----------
        resids : ndarray
            Residuals.

        Returns
        -------
        float
            Backcast variance value.
        """
        t = len(resids)
        span = min(75, t)
        # EWM decay factor
        alpha = 2.0 / (span + 1.0)
        resids2 = resids**2
        weights = (1 - alpha) ** np.arange(t - 1, -1, -1)
        backcast = float(np.sum(weights * resids2) / np.sum(weights))
        return max(backcast, 1e-12)
