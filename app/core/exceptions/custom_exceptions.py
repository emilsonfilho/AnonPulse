class ResourceNotFoundException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class DomainValidationException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class SubjectAlreadyExistsException(Exception):
    def __init__(self, code: str) -> None:
        message = f"Já existe uma disciplina com o código {code}."
        super().__init__(message)
        self.message = message


class SubjectNotFoundException(Exception):
    def __init__(self) -> None:
        message = "Disciplina não encontrada."
        super().__init__(message)
        self.message = message


# Monitor Exceptions
class MonitorAlreadyExistsException(Exception):
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
class ProfessorNotFoundException(Exception):
    def __init__(self) -> None:
        message = "Professor(a) não encontrado(a)."
        super().__init__(message)
        self.message = message


class EnrollmentAlreadyExistsException(Exception):
    def __init__(self, id: int) -> None:
        message = f"Já existe uma matrícula com id {id}"
        super().__init__(message)
        self.message = message


class EnrollmentNotFoundException(Exception):
    def __init__(self) -> None:
        message = "Matrícula não encontrada."
        super().__init__(message)
        self.message = message


class ClassroomAlreadyExistsException(Exception):
    def __init__(self, cod: str) -> None:
        message = f"Já existe uma turma com o código {cod}"
        super().__init__(message)
        self.message = message


class ClassroomNotFoundException(Exception):
    def __init__(self) -> None:
        message = "Turma não encontrada."
        super().__init__(message)
        self.message = message


class ClassroomHasEnrollmentsException(Exception):
    def __init__(self, cod: str) -> None:
        message = f"Não é possível deletar a turma '{cod}' porque ela já possui alunos matriculados."
        super().__init__(message)
        self.message = message


class StudentAlreadyExistsException(Exception):
    def __init__(self, registration: str) -> None:
        message = f"Já existe um(a) aluno(a) com a matrícula {registration}"
        super().__init__(message)
        self.message = message


class StudentNotFoundException(Exception):
    def __init__(self) -> None:
        message = "Aluno(a) não encontrado(a)."
        super().__init__(message)
        self.message = message


class MonitorAssignmentAlreadyExistsException(Exception):
    def __init__(self, monitor_registration: str, classroom_cod: str) -> None:
        message = f"O monitor '{monitor_registration}' já está alocado na turma '{classroom_cod}'."
        super().__init__(message)
        self.message = message


class MonitorAssignmentHasFeedbackException(Exception):
    def __init__(self, assignment_id: int) -> None:
        message = f"Não é possível remover a alocação de ID {assignment_id} pois ela já possui feedbacks registrados."
        super().__init__(message)
        self.message = message


class MonitorAssignmentNotFoundException(Exception):
    def __init__(self) -> None:
        message = "Alocação não encontrada."
        super().__init__(message)
        self.message = message


class FeedbackNotFoundException(Exception):
    def __init__(self, id: int) -> None:
        message = f"Feedback com ID {id} não encontrado."
        super().__init__(message)
        self.message = message


class FeedbackAlreadyExistsException(Exception):
    def __init__(self, id: int) -> None:
        message = f"Já existe um feedback com ID {id}."
        super().__init__(message)
        self.message = message


class DocumentNotFoundException(Exception):
    def __init__(self, id: int) -> None:
        message = f"Documento com ID {id} não encontrado."
        super().__init__(message)
        self.message = message

class DocumentNotExistsException(Exception):
    def __init__(self) -> None:
        message = "Arquivo não encontrado no servidor."
        super().__init__(message)
        self.message = message