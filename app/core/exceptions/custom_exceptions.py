class ResourceNotFoundException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class DomainValidationException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

class SubjectAlreadyExistsExcepion(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message