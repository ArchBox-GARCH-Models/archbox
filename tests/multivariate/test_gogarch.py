"""Tests for GO-GARCH model."""

from __future__ import annotations

import numpy as np

from archbox.multivariate.gogarch import GOGARCH
from archbox.multivariate.utils import is_positive_definite


class TestGOGARCH:
    """Test GO-GARCH model."""

    def test_gogarch_factors_independent(self, synthetic_returns):
        """Factors should be approximately independent (low correlation)."""
        model = GOGARCH(synthetic_returns)
        _ = model.fit(disp=False)

        factors = model.factors
        assert factors is not None

        # Correlation between factors should be close to 0
        corr = np.corrcoef(factors.T)
        k = factors.shape[1]

        for i in range(k):
            for j in range(i + 1, k):
                assert abs(corr[i, j]) < 0.3, (
                    f"Factor correlation ({i},{j}) = {corr[i, j]:.3f}, expected ~0"
                )

    def test_gogarch_reconstruction(self, synthetic_returns):
        """H_t = Z * diag(h_t) * Z' should reconstruct correctly."""
        model = GOGARCH(synthetic_returns)
        results = model.fit(disp=False)

        Z = model.mixing_matrix
        assert Z is not None

        # Verify H_t is consistent with Z and factor variances
        H_t = results.dynamic_covariance
        T = H_t.shape[0]

        # H_t should be symmetric
        for t in range(0, T, 50):
            np.testing.assert_array_almost_equal(
                H_t[t],
                H_t[t].T,
                decimal=8,
                err_msg=f"H_t not symmetric at t={t}",
            )

    def test_gogarch_positive_definite(self, synthetic_returns):
        """H_t should be positive definite for all t."""
        model = GOGARCH(synthetic_returns)
        results = model.fit(disp=False)

        H_t = results.dynamic_covariance
        T = H_t.shape[0]

        for t in range(0, T, 50):
            assert is_positive_definite(H_t[t]), f"H_t not PD at t={t}"

    def test_gogarch_mixing_matrix_shape(self, synthetic_returns):
        """Mixing matrix Z should be (k, k)."""
        model = GOGARCH(synthetic_returns)
        _ = model.fit(disp=False)

        Z = model.mixing_matrix
        assert Z is not None
        k = synthetic_returns.shape[1]
        assert Z.shape == (k, k)

    def test_gogarch_loglike_finite(self, synthetic_returns):
        """Log-likelihood should be finite."""
        model = GOGARCH(synthetic_returns)
        results = model.fit(disp=False)

        assert np.isfinite(results.loglike)

    def test_gogarch_summary(self, synthetic_returns):
        """summary() should return a non-empty string."""
        model = GOGARCH(synthetic_returns)
        results = model.fit(disp=False)
        s = results.summary()
        assert isinstance(s, str)
        assert "GO-GARCH" in s

    def test_gogarch_no_correlation_params(self, synthetic_returns):
        """GO-GARCH has no separate correlation parameters."""
        model = GOGARCH(synthetic_returns)
        results = model.fit(disp=False)

        assert len(results.params) == 0

    def test_gogarch_forecast(self, synthetic_returns):
        """Forecast should return correct shapes."""
        model = GOGARCH(synthetic_returns)
        results = model.fit(disp=False)

        fcast = model.forecast(results, horizon=10)
        k = synthetic_returns.shape[1]

        assert fcast["covariance"].shape == (10, k, k)
        assert fcast["correlation"].shape == (10, k, k)

    def test_gogarch_with_fx_data(self, fx_returns):
        """GO-GARCH should work with FX data."""
        model = GOGARCH(fx_returns)
        results = model.fit(disp=False)

        assert results.dynamic_covariance.shape == (2000, 3, 3)
        assert np.isfinite(results.loglike)


class TestGOGARCHNoSklearn:
    """GO-GARCH must not depend on scikit-learn (not a declared dependency)."""

    def test_module_source_has_no_sklearn(self):
        """The module must not reference sklearn at all."""
        import inspect

        from archbox.multivariate import gogarch

        assert "sklearn" not in inspect.getsource(gogarch)

    def test_fit_does_not_import_sklearn(self, synthetic_returns):
        """Fitting must not pull sklearn into sys.modules."""
        import subprocess
        import sys
        from pathlib import Path

        root = Path(__file__).resolve().parents[2]
        code = (
            "import sys, numpy as np\n"
            "from archbox.multivariate import GOGARCH\n"
            "rng = np.random.default_rng(0)\n"
            "x = rng.standard_normal((300, 3)) * 0.01\n"
            "GOGARCH(x).fit(disp=False)\n"
            "assert 'sklearn' not in sys.modules, 'sklearn was imported'\n"
            "print('OK')\n"
        )
        out = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            cwd=str(root),
            check=False,
        )
        assert out.returncode == 0, out.stderr
        assert "OK" in out.stdout


class TestGOGARCHComponents:
    """n_components < k must work (the loops used to run over range(k))."""

    def test_reduced_components_fit(self, synthetic_returns):
        """A reduced-rank GO-GARCH fits and yields a PD covariance path."""
        model = GOGARCH(synthetic_returns, n_components=2)
        results = model.fit(disp=False)

        assert model.mixing_matrix is not None
        assert model.mixing_matrix.shape == (3, 2)
        assert model.factors is not None
        assert model.factors.shape == (synthetic_returns.shape[0], 2)
        assert len(results.univariate_results) == 2
        assert np.isfinite(results.loglike)
        for t in range(0, results.dynamic_covariance.shape[0], 50):
            assert is_positive_definite(results.dynamic_covariance[t])

    def test_single_component_fit(self, synthetic_returns):
        """Even a one-factor model stays positive definite via psi."""
        model = GOGARCH(synthetic_returns, n_components=1)
        results = model.fit(disp=False)
        assert results.dynamic_covariance.shape == (synthetic_returns.shape[0], 3, 3)
        assert np.all(np.isfinite(results.dynamic_covariance))
        assert is_positive_definite(results.dynamic_covariance[-1])

    def test_idiosyncratic_variance_is_negligible_at_full_rank(self, synthetic_returns):
        """With m = k the factors span everything, so psi is ~0."""
        model = GOGARCH(synthetic_returns)
        model.fit(disp=False)
        psi = model.idiosyncratic_variance
        assert psi is not None
        assert np.all(psi < 1e-10 * np.var(synthetic_returns))

    def test_invalid_n_components(self, synthetic_returns):
        """n_components outside [1, k] is rejected."""
        import pytest

        with pytest.raises(ValueError, match="n_components"):
            GOGARCH(synthetic_returns, n_components=0)
        with pytest.raises(ValueError, match="n_components"):
            GOGARCH(synthetic_returns, n_components=4)

    def test_reduced_forecast_shapes(self, synthetic_returns):
        """Forecasting works for a reduced-rank model too."""
        model = GOGARCH(synthetic_returns, n_components=2)
        results = model.fit(disp=False)
        fcast = model.forecast(results, horizon=4)
        assert fcast["covariance"].shape == (4, 3, 3)
        assert is_positive_definite(fcast["covariance"][0])


class TestGOGARCHDeterminism:
    """Results must be reproducible from an explicit seed."""

    def test_same_seed_same_result(self, synthetic_returns):
        """Two fits with the same seed give identical mixing matrices."""
        a = GOGARCH(synthetic_returns, seed=11).fit(disp=False)
        b = GOGARCH(synthetic_returns, seed=11).fit(disp=False)
        np.testing.assert_allclose(a.dynamic_covariance, b.dynamic_covariance)
        assert a.loglike == b.loglike

    def test_seed_is_configurable(self, synthetic_returns):
        """The seed is a parameter, not a hard-coded random_state."""
        model = GOGARCH(synthetic_returns, seed=123)
        assert model.seed == 123


class TestFactorExtraction:
    """The numpy PCA/ICA replacements behave like their sklearn counterparts."""

    def test_pca_whiten_gives_identity_covariance(self, rng):
        """The whitened data has an identity sample covariance."""
        from archbox.multivariate import pca_whiten

        x = rng.standard_normal((500, 4)) @ rng.standard_normal((4, 4))
        x = x - x.mean(axis=0)
        whitened, whitening, dewhitening = pca_whiten(x, 4)
        cov = whitened.T @ whitened / whitened.shape[0]
        np.testing.assert_allclose(cov, np.eye(4), atol=1e-8)
        np.testing.assert_allclose(x, whitened @ dewhitening.T, atol=1e-8)
        assert whitening.shape == (4, 4)

    def test_pca_whiten_reduced_rank(self, rng):
        """Requesting m < k keeps the m leading components."""
        from archbox.multivariate import pca_whiten

        x = rng.standard_normal((400, 5)) @ rng.standard_normal((5, 5))
        x = x - x.mean(axis=0)
        whitened, whitening, dewhitening = pca_whiten(x, 2)
        assert whitened.shape == (400, 2)
        assert whitening.shape == (2, 5)
        assert dewhitening.shape == (5, 2)
        cov = whitened.T @ whitened / whitened.shape[0]
        np.testing.assert_allclose(cov, np.eye(2), atol=1e-8)

    def test_fast_ica_returns_orthogonal_rotation(self, rng):
        """FastICA returns an orthogonal rotation and separates the sources."""
        from archbox.multivariate import fast_ica, pca_whiten

        n = 2000
        s1 = rng.uniform(-1.0, 1.0, n)
        s2 = np.sign(rng.standard_normal(n)) * rng.uniform(0.5, 1.0, n)
        sources = np.column_stack([s1, s2])
        mixing = np.array([[1.0, 0.6], [-0.4, 1.2]])
        x = sources @ mixing.T
        x = x - x.mean(axis=0)

        whitened, _w, _dw = pca_whiten(x, 2)
        rotation, converged = fast_ica(whitened, seed=0)

        assert converged
        np.testing.assert_allclose(rotation @ rotation.T, np.eye(2), atol=1e-8)

        recovered = whitened @ rotation.T
        # Each recovered component matches one source up to sign and scale.
        corr = np.corrcoef(recovered.T, sources.T)[:2, 2:]
        assert np.max(np.abs(corr), axis=1).min() > 0.9

    def test_fast_ica_is_deterministic(self, rng):
        """Same seed, same rotation."""
        from archbox.multivariate import fast_ica

        x = rng.standard_normal((500, 3))
        r1, _ = fast_ica(x, seed=5)
        r2, _ = fast_ica(x, seed=5)
        np.testing.assert_allclose(r1, r2)


class TestGOGARCHForecast:
    """Forecasts must use the factor variance forecasts."""

    def test_forecast_uses_factor_variance_forecast(self, synthetic_returns):
        """H_{T+h} rebuilds from ArchResults.forecast of every factor."""
        from archbox.multivariate.utils import cov_to_corr

        model = GOGARCH(synthetic_returns)
        results = model.fit(disp=False)
        horizon = 5
        fcast = model.forecast(results, horizon=horizon)

        z = results.extras["mixing_matrix"]
        psi = results.extras["idiosyncratic"]
        var = np.column_stack(
            [r.forecast(horizon=horizon)["variance"] for r in results.univariate_results]
        )
        expected = np.einsum("ki,hi,li->hkl", z, var, z)
        expected[:, np.arange(3), np.arange(3)] += psi
        np.testing.assert_allclose(fcast["covariance"], expected, rtol=1e-10)
        np.testing.assert_allclose(fcast["correlation"], cov_to_corr(expected), rtol=1e-10)

    def test_forecast_is_not_flat(self, synthetic_returns):
        """The old implementation repeated the last in-sample variance."""
        model = GOGARCH(synthetic_returns)
        results = model.fit(disp=False)
        fcast = model.forecast(results, horizon=25)
        diag = np.diagonal(fcast["covariance"], axis1=1, axis2=2)
        assert np.max(np.std(diag, axis=0)) > 0
