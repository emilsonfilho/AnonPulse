import pytest
from app.models.classroom import Classroom
from app.repositories.classroom_repository import ClassroomRepository


@pytest.mark.asyncio
async def test_insert_persiste_no_banco(classroom):
    no_banco = await Classroom.get(classroom.id)
    assert no_banco is not None
    assert no_banco.cod == "T01-2025"


@pytest.mark.asyncio
async def test_get_por_id(classroom, params):
    repo = ClassroomRepository()
    result = await repo.get(classroom.id)
    assert result is not None
    assert result.id == classroom.id


@pytest.mark.asyncio
async def test_list_all_contem_classroom(classroom, params):
    repo = ClassroomRepository()
    page = await repo.list_all(params)
    ids = [item.id for item in page.items]
    assert classroom.id in ids


@pytest.mark.asyncio
async def test_list_by_professor_retorna_classroom(classroom, professor, params):
    repo = ClassroomRepository()
    page = await repo.list_by_professor(professor.id, params)
    ids = [item.id for item in page.items]
    assert classroom.id in ids


@pytest.mark.asyncio
async def test_list_by_subject_retorna_classroom(classroom, subject, params):
    repo = ClassroomRepository()
    page = await repo.list_by_subject(subject.cod, params)
    ids = [item.id for item in page.items]
    assert classroom.id in ids


@pytest.mark.asyncio
async def test_list_by_subject_cod_inexistente_levanta_excecao(params):
    repo = ClassroomRepository()
    from app.core.exceptions.custom_exceptions import SubjectNotFoundException

    with pytest.raises(SubjectNotFoundException):
        await repo.list_by_subject("COD-INEXISTENTE", params)
