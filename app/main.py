from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi_pagination import add_pagination
from scalar_fastapi import get_scalar_api_reference

from app.api.routers.classroom import api_router as classroom_router
from app.api.routers.document import api_router as document_router
from app.api.routers.enrollment import api_router as enrollment_router
from app.api.routers.feedback import api_router as feedback_router
from app.api.routers.feedback_type import api_router as feedback_type_router
from app.api.routers.hash import api_router as hash_router
from app.api.routers.monitor import api_router as monitor_router
from app.api.routers.monitor_assignment import api_router as monitor_assignment_router
from app.api.routers.professor import api_router as professor_router
from app.api.routers.student import api_router as student_router
from app.api.routers.subject import api_router as subject_router
from app.core.exceptions.custom_exceptions import (
    ClassroomAlreadyExistsException,
    ClassroomHasEnrollmentsException,
    ClassroomNotFoundException,
    DomainValidationException,
    EnrollmentAlreadyExistsException,
    EnrollmentNotFoundException,
    FeedbackAlreadyExistsException,
    FeedbackNotFoundException,
    MonitorAlreadyExistsException,
    MonitorAssignmentAlreadyExistsException,
    MonitorAssignmentHasFeedbackException,
    MonitorAssignmentNotFoundException,
    MonitorNotFoundException,
    ProfessorNotFoundException,
    ResourceNotFoundException,
    StudentAlreadyExistsException,
    StudentNotFoundException,
    SubjectAlreadyExistsException,
    SubjectNotFoundException,
)
from app.core.exceptions.handlers import (
    custom_conflict_handler,
    custom_not_found_handler,
    domain_validation_handler,
    global_exception_handler,
    http_handler,
    request_validation_handler,
    resource_not_found_handler,
    sqlaclgemy_integrity_handler,
)

tags_metadata = [
    {"name": "Feedbacks", "description": "Operações relacionadas a feedbacks"},
    {"name": "Hash", "description": "Operações relacionadas a geração de hash"},
    {"name": "Professores", "description": "Operações relacionadas a professores"},
    {"name": "Turmas", "description": "Operações relacionadas a turmas"},
    {"name": "Disciplinas", "description": "Operações relacionadas a disciplinas"},
    {"name": "Matrículas", "description": "Operações relacionadas a matrículas"},
    {"name": "Alunos", "description": "Operações relacionadas a alunos"},
    {"name": "Monitores", "description": "Operações relacionadas a monitores"},
    {"name": "Monitorias", "description": "Operações relacionadas a monitorias"},
    {"name": "Documentos", "description": "Operações relacionadas a documentos"},
    {
        "name": "Tipos de Feedback",
        "description": "Operações relacionadas a tipos de feedback",
    },
]

PREFIX = "/api"

app = FastAPI(
    title="AnonPulse",
    summary="O AnonPulse é uma plataforma desenvolvida para gerenciar feedbacks anônimos de alunos para monitores da UFC Quixadá",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    contact={
        "name": "Emilson Filho",
        "url": "https://github.com/emilsonfilho",
        "email": "email@faltacolocar.com",
    },
    tags=tags_metadata,
)

app.add_exception_handler(DomainValidationException, domain_validation_handler)  # type: ignore
app.add_exception_handler(ResourceNotFoundException, resource_not_found_handler)  # type: ignore
app.add_exception_handler(HTTPException, http_handler)  # type: ignore
app.add_exception_handler(RequestValidationError, request_validation_handler)  # type: ignore
app.add_exception_handler(Exception, global_exception_handler)

for exc in [
    SubjectNotFoundException,
    MonitorNotFoundException,
    ProfessorNotFoundException,
    EnrollmentNotFoundException,
    ClassroomNotFoundException,
    StudentNotFoundException,
    MonitorAssignmentNotFoundException,
    FeedbackNotFoundException,
]:
    app.add_exception_handler(exc, custom_not_found_handler)  # type: ignore

for exc in [
    SubjectAlreadyExistsException,
    MonitorAlreadyExistsException,
    EnrollmentAlreadyExistsException,
    ClassroomAlreadyExistsException,
    ClassroomHasEnrollmentsException,
    StudentAlreadyExistsException,
    MonitorAssignmentAlreadyExistsException,
    MonitorAssignmentHasFeedbackException,
    FeedbackAlreadyExistsException,
]:
    app.add_exception_handler(exc, custom_conflict_handler)  # type: ignore

app.include_router(subject_router, prefix=PREFIX)
app.include_router(professor_router, prefix=PREFIX)
app.include_router(classroom_router, prefix=PREFIX)
app.include_router(enrollment_router, prefix=PREFIX)
app.include_router(student_router, prefix=PREFIX)
app.include_router(monitor_router, prefix=PREFIX)
app.include_router(monitor_assignment_router, prefix=PREFIX)
app.include_router(feedback_type_router, prefix=PREFIX)
app.include_router(feedback_router, prefix=PREFIX)
app.include_router(hash_router, prefix=PREFIX)
app.include_router(document_router, prefix=PREFIX)


@app.get(f"{PREFIX}/scalar", include_in_schema=False)
async def scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)


add_pagination(app)
