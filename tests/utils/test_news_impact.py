"""Tests for news impact curve."""

from __future__ import annotations

import numpy as np
import pytest

from archbox.utils.news_impact import news_impact_curve


class TestNewsImpact:
    """Test news impact curve functionality."""

    def test_news_impact_garch_symmetric(self, sp500_returns: np.ndarray):
        """GARCH news impact curve should be symmetric."""
        from archbox.models.garch import GARCH

        model = GARCH(sp500_returns, p=1, q=1)
        results = model.fit(disp=False)
        eps_range, sigma2_response = news_impact_curve(model, results, n_points=101)

        assert len(eps_range) == 101
        assert len(sigma2_response) == 101
        assert np.all(np.isfinite(sigma2_response))
        assert np.all(sigma2_response > 0)

        # Check symmetry: f(eps) == f(-eps) for GARCH
        mid = len(eps_range) // 2
        for i in range(1, mid):
            np.testing.assert_allclose(
                sigma2_response[mid - i],
                sigma2_response[mid + i],
                rtol=0.01,
                err_msg=f"GARCH should be symmetric at offset {i}",
            )

    def test_news_impact_egarch_asymmetric(self, sp500_returns: np.ndarray):
        """EGARCH should show asymmetric response (negative > positive)."""
        from archbox.models.egarch import EGARCH

        model = EGARCH(sp500_returns, p=1, q=1)
        results = model.fit(disp=False)
        eps_range, sigma2_response = news_impact_curve(model, results, n_points=101)

        assert np.all(np.isfinite(sigma2_response))

        mid = len(eps_range) // 2
        # Compare equal-magnitude positive and negative shocks
        # For EGARCH with gamma < 0: negative shock should give higher sigma2
        neg_response = sigma2_response[mid - mid // 2]  # negative shock
        pos_response = sigma2_response[mid + mid // 2]  # positive shock of same magnitude

        assert neg_response > pos_response, (
            f"EGARCH: negative shock response ({neg_response:.6f}) "
            f"should exceed positive ({pos_response:.6f})"
        )

    def test_news_impact_gjr_asymmetric(self, sp500_returns: np.ndarray):
        """GJR-GARCH should show kink at eps=0 (asymmetric)."""
        from archbox.models.gjr_garch import GJRGARCH

        model = GJRGARCH(sp500_returns, p=1, q=1)
        results = model.fit(disp=False)
        eps_range, sigma2_response = news_impact_curve(model, results, n_points=101)

        assert np.all(np.isfinite(sigma2_response))
        assert np.all(sigma2_response > 0)

        mid = len(eps_range) // 2
        # Negative shock should produce higher variance
        neg_response = sigma2_response[mid - mid // 2]
        pos_response = sigma2_response[mid + mid // 2]

        assert neg_response > pos_response, (
            "GJR-GARCH: negative shock should produce higher variance"
        )

    def test_news_impact_returns_correct_shape(self, sp500_returns: np.ndarray):
        from archbox.models.garch import GARCH

        model = GARCH(sp500_returns, p=1, q=1)
        results = model.fit(disp=False)

        for n in [50, 100, 200]:
            eps, sig2 = news_impact_curve(model, results, n_points=n)
            assert len(eps) == n
            assert len(sig2) == n

    def test_news_impact_range(self, sp500_returns: np.ndarray):
        """eps_range should span -sigma_range*sigma to +sigma_range*sigma."""
        from archbox.models.garch import GARCH

        model = GARCH(sp500_returns, p=1, q=1)
        results = model.fit(disp=False)
        eps_range, _ = news_impact_curve(model, results, sigma_range=2.0)

        sigma = results.conditional_volatility.mean()
        assert eps_range[0] == pytest.approx(-2.0 * sigma, rel=0.01)
        assert eps_range[-1] == pytest.approx(2.0 * sigma, rel=0.01)


class TestIntegrationAllModels:
    """Integration test: fit all 8 models on SP500."""

    def test_all_models_fit_sp500(self, sp500_returns: np.ndarray):
        """All 8 GARCH-family models should fit SP500 without errors."""
        from archbox.models.aparch import APARCH
        from archbox.models.component_garch import ComponentGARCH
        from archbox.models.egarch import EGARCH
        from archbox.models.figarch import FIGARCH
        from archbox.models.garch import GARCH
        from archbox.models.garch_m import GARCHM
        from archbox.models.gjr_garch import GJRGARCH
        from archbox.models.igarch import IGARCH

        models_specs = [
            ("GARCH", lambda r: GARCH(r, p=1, q=1)),
            ("EGARCH", lambda r: EGARCH(r, p=1, q=1)),
            ("GJR-GARCH", lambda r: GJRGARCH(r, p=1, q=1)),
            ("APARCH", lambda r: APARCH(r, p=1, q=1)),
            ("IGARCH", lambda r: IGARCH(r)),
            ("FIGARCH", lambda r: FIGARCH(r, truncation_lag=100)),
            ("GARCH-M", lambda r: GARCHM(r, p=1, q=1)),
            ("Component GARCH", lambda r: ComponentGARCH(r)),
        ]

        results_list = []
        for name, model_fn in models_specs:
            model = model_fn(sp500_returns)
            results = model.fit(disp=False)
            assert results is not None, f"{name} fit returned None"
            assert np.isfinite(results.loglike), (
                f"{name} loglikelihood is not finite: {results.loglike}"
            )
            results_list.append((name, results))

        # All models should have fit successfully
        assert len(results_list) == 8

    def test_all_models_import_from_archbox(self):
        """All models should be importable from archbox submodules."""
        from archbox.models.garch import GARCH
        from archbox.models.egarch import EGARCH
        from archbox.models.gjr_garch import GJRGARCH
        from archbox.models.aparch import APARCH
        from archbox.models.igarch import IGARCH
        from archbox.models.figarch import FIGARCH
        from archbox.models.garch_m import GARCHM
        from archbox.models.component_garch import ComponentGARCH
        from archbox.models.har_rv import HARRV

        assert GARCH is not None
        assert EGARCH is not None
        assert GJRGARCH is not None
        assert APARCH is not None
        assert IGARCH is not None
        assert FIGARCH is not None
        assert GARCHM is not None
        assert ComponentGARCH is not None
        assert HARRV is not None

    def test_all_distributions_import(self):
        """All distributions should be importable."""
        from archbox.distributions import (
            GeneralizedError,
            MixtureNormal,
            Normal,
            SkewedT,
            StudentT,
        )

        assert Normal is not None
        assert StudentT is not None
        assert SkewedT is not None
        assert GeneralizedError is not None
        assert MixtureNormal is not None
