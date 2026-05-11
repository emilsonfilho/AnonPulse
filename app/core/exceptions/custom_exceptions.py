class ResourceNotFoundException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class DomainValidationException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

class SubjectAlreadyExistsExcepion(Exception):
    def __init__(self, code: str) -> None:
        message = f"Já existe uma disciplina com o código {code}."
        super().__init__(message)
        self.message = message

class SubjectNotFoundException(Exception):
    def __init__(self) -> None:
        message = "Disciplina não enconotrada."
        super().__init__(message)
        self.message = message