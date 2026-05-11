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

class SubjectNotFoundException(Exception):
    def __init__(self) -> None:
        message = "Disciplina não enconotrada."
        super().__init__(message)
        self.message = message

# Monitor Exceptions
class MonitorAlreadyExistsExcepion(Exception):
    def __init__(self, registration: str) -> None:
        message = f"Já existe um monitor(a) com a matrícula {registration}"
        super().__init__(message)
        self.message = message

class MonitorNotFoundException(Exception):
    def __init__(self) -> None:
        message = "Monitor(a) não encontrado(a)."
        super().__init__(message)
        self.message = message

# Professor Exceptions
class ProfessorAlreadyExistsExcepion(Exception):
    def __init__(self, id: int) -> None:
        message = f"Já existe um professor com id {id}"
        super().__init__(message)
        self.message = message

class ProfessorNotFoundException(Exception):
    def __init__(self) -> None:
        message = "Disciplina não enconotrada."
        super().__init__(message)
        self.message = message
