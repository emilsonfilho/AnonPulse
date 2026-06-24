import uuid

import pytest
from beanie import PydanticObjectId

from app.repositories.classroom_repository import ClassroomRepository
from app.services.classroom_service import ClassroomService
from app.schemas.classroom_schema import CreateClassroomRequest
from app.core.exceptions.custom_exceptions import (
    ClassroomAlreadyExistsException,
    ClassroomHasEnrollmentsException,
    ClassroomNotFoundException,
)


@pytest.mark.asyncio
@pytest.mark.asyncio
async def test_create_classroom_success(subject, professor):
    repo = ClassroomRepository()
    service = ClassroomService(repo)

    # Gera um código aleatório com o prefixo para nunca colidir em execuções repetidas
    random_cod = f"QXD-{str(uuid.uuid4())[:4].upper()}"

    req = CreateClassroomRequest(
        cod=random_cod, subject_cod=subject.cod, professor_id=professor.id
    )

    nova_turma = await service.create(req)
    assert nova_turma.cod == random_cod
    assert nova_turma.subject.cod == subject.cod


@pytest.mark.asyncio
async def test_create_classroom_already_exists_raises_exception(
    classroom, subject, professor
):
    repo = ClassroomRepository()
    service = ClassroomService(repo)

    req = CreateClassroomRequest(
        cod=classroom.cod, subject_cod=subject.cod, professor_id=professor.id
    )

    with pytest.raises(ClassroomAlreadyExistsException):
        await service.create(req)


@pytest.mark.asyncio
async def test_list_by_professor_retorna_pagina_correta(classroom, professor, params):
    repo = ClassroomRepository()
    service = ClassroomService(repo)
    pagina = await service.list_by_professor(professor.id, params)
    assert pagina.total >= 1


@pytest.mark.asyncio
async def test_list_by_subject_retorna_pagina_correta(classroom, subject, params):
    repo = ClassroomRepository()
    service = ClassroomService(repo)
    pagina = await service.list_by_subject(subject.cod, params)
    assert pagina.total >= 1


@pytest.mark.asyncio
async def test_get_or_raise_inexistente_raises_not_found():
    repo = ClassroomRepository()
    service = ClassroomService(repo)

    with pytest.raises(ClassroomNotFoundException):
        # Passando um ObjectId válido mas que não existe no banco
        await service.get_or_raise(PydanticObjectId())


@pytest.mark.asyncio
async def test_delete_classroom_with_enrollment_raises_exception(classroom, enrollment):
    from app.models.classroom import Classroom

    print(await Classroom.find_all().to_list())

    turma_db = await Classroom.get(classroom.id)

    if turma_db is None:
        raise ClassroomNotFoundException()

    if turma_db.enrollments is None:
        turma_db.enrollments = []

    turma_db.enrollments.append(enrollment)
    await turma_db.save()

    repo = ClassroomRepository()
    service = ClassroomService(repo)

    with pytest.raises(ClassroomHasEnrollmentsException):
        await service.delete(turma_db.cod)


@pytest.mark.asyncio
async def test_delete_classroom_success(subject, professor):
    repo = ClassroomRepository()
    service = ClassroomService(repo)

    req = CreateClassroomRequest(
        cod="VAZIA", subject_cod=subject.cod, professor_id=professor.id
    )
    turma_vazia = await service.create(req)

    await service.delete(turma_vazia.cod)
