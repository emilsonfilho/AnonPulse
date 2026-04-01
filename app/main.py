from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from api.routers.feedback import api_router as feedback_router
from api.routers.hash import api_router as hash_router
from api.core.exceptions.custom_exceptions import (
    ResourceNotFoundException,
    DomainValidationException,
)
from api.core.exceptions.handlers import (
    resource_not_found_handler,
    domain_validation_handler,
    http_handler,
    request_validation_handler,
    global_exception_handler,
)

tags_metadata = [
    {"name": "Feedbacks", "description": "Operações relacionadas a feedbacks"},
    {"name": "Hash", "description": "Operações relacionadas a geração de hash"},
]


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

app.include_router(feedback_router, prefix="/api")
app.include_router(hash_router, prefix="/api")
