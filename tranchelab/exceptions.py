class TranceLabError(Exception):
    """Base exception for TrancheLab API errors."""
    def __init__(self, message: str, status_code: int = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class AuthenticationError(TranceLabError):
    """Raised when the API key is missing or invalid."""
    pass

class ExtractionError(TranceLabError):
    """Raised when an extraction fails or returns an error."""
    pass

class NotFoundError(TranceLabError):
    """Raised when a requested resource is not found."""
    pass
