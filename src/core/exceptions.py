"""Common exceptions for the core module."""


class RequestFailedError(ValueError):
    """Exception raised when a request fails."""

    def __init__(self, message: str, status: int):
        """Initialize the exception."""
        super().__init__(message)
        self.status = status
