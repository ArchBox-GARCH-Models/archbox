"""Custom exceptions for archbox."""


class ArchBoxError(Exception):
    """Base exception for archbox."""


class ConvergenceError(ArchBoxError):
    """Raised when optimization fails to converge."""


class StationarityError(ArchBoxError):
    """Raised when stationarity constraint is violated."""


class ValidationError(ArchBoxError):
    """Raised when input validation fails."""
