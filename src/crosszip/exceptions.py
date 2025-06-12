"""Custom exceptions for the crosszip package."""


class CrosszipError(Exception):
    """Base exception class for crosszip package."""


class CrosszipTypeError(CrosszipError, TypeError):
    """Raised when there's a type-related error in crosszip operations."""


class CrosszipValueError(CrosszipError, ValueError):
    """Raised when there's a value-related error in crosszip operations."""


# Error messages for plugin validation
PARAMS_REQUIRED_ERROR: str = "Parameter names and values must be provided."
PARAMS_COUNT_MISMATCH_ERROR: str = (
    "Each parameter name must have a corresponding list of values."
)
PARAMS_NAME_TYPE_ERROR: str = "All parameter names must be strings."
PARAMS_VALUES_TYPE_ERROR: str = "All parameter values must be non-empty sequences."
