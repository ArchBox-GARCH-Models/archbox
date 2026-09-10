"""Base class for volatility models."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

import numpy as np
from numpy.typing import NDArray

from archbox.utils.validation import validate_positive_integer, validate_returns

if TYPE_CHECKING:
    from archbox.distributions.base import Distribution


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
        Estimated mean (0 if mean='zero').
    """

    volatility_process: str = "Unknown"

    def __init__(
        self,
        endog: Any,
        mean: str = "constant",
        dist: str = "normal",
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
        self._dist_name = dist
        self.dist: Distribution = self._build_distribution(dist)
        self._is_fitted = False

    @staticmethod
    def _build_distribution(dist: str) -> Distribution:
        """Build a distribution instance from a (possibly aliased) name."""
        from archbox.distributions.ged import GeneralizedError
        from archbox.distributions.mixture_normal import MixtureNormal
        from archbox.distributions.normal import Normal
        from archbox.distributions.skewed_t import SkewedT
        from archbox.distributions.student_t import StudentT

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
        # Ensure positivity
        sigma2 = np.maximum(sigma2, 1e-12)
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
        sigma2 = np.maximum(sigma2, 1e-12)
        return self.dist.loglikelihood(self.endog, sigma2, dist_params)

    def simulate(
        self,
        n: int,
        params: NDArray[np.float64],
        seed: int | None = None,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Simulate returns and volatility from the model.

        Parameters
        ----------
        n : int
            Number of observations to simulate.
        params : ndarray
            Model parameters.
        seed : int, optional
            Random seed.

        Returns
        -------
        tuple[ndarray, ndarray]
            (returns, conditional_volatility) each shape (n,).
        """
        rng = np.random.default_rng(seed)
        nv = self.num_params
        var_params = params[:nv]
        dist_params = params[nv:]
        z = self.dist.simulate(n, rng, dist_params)

        backcast = var_params[0] / (1.0 - np.sum(var_params[1:]))  # unconditional variance
        if not np.isfinite(backcast) or backcast <= 0:
            backcast = np.var(self.endog) if len(self.endog) > 0 else 1.0

        sigma2 = np.empty(n)
        returns = np.empty(n)

        # First observation
        sigma2[0] = backcast
        returns[0] = np.sqrt(sigma2[0]) * z[0]

        for t in range(1, n):
            sigma2[t : t + 1] = self._variance_recursion(var_params, returns[:t], float(backcast))[
                -1:
            ]
            returns[t] = np.sqrt(max(sigma2[t], 1e-12)) * z[t]

        return returns, np.sqrt(sigma2)

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
