"""Custom exceptions for archbox."""


class ArchBoxError(Exception):
    """Base exception for archbox."""


class ConvergenceError(ArchBoxError):
    """Raised when optimization fails to converge."""


class StationarityError(ArchBoxError):
    """Raised when stationarity constraint is violated."""


class ValidationError(ArchBoxError):
    """Raised when input validation fails."""


class ArchBoxWarning(UserWarning):
    """Base warning for archbox."""


class ConvergenceWarning(ArchBoxWarning):
    """Warned when optimization does not converge (estimates may be unreliable)."""


class StandardErrorWarning(ArchBoxWarning):
    """Warned when standard errors cannot be computed (non-PD Hessian)."""
