import pytest
from app.models.professor import Professor
from app.repositories.professor_repository import ProfessorRepository


@pytest.mark.asyncio
async def test_insert_persiste_no_banco(professor):
    no_banco = await Professor.get(professor.id)
    assert no_banco is not None
    assert no_banco.name == "Prof. Silva"
    assert no_banco.email == "silva@ufc.br"


@pytest.mark.asyncio
async def test_get_por_id(professor, params):
    repo = ProfessorRepository()
    result = await repo.get(professor.id)
    assert result is not None
    assert result.id == professor.id


@pytest.mark.asyncio
async def test_list_all_contem_professor(professor, params):
    repo = ProfessorRepository()
    page = await repo.list_all(params)
    ids = [item.id for item in page.items]
    assert professor.id in ids


@pytest.mark.asyncio
async def test_update_persiste_no_banco(professor):
    repo = ProfessorRepository()
    await repo.update(professor.id, {"name": "Prof. Silva Atualizado"})

    no_banco = await Professor.get(professor.id)
    assert no_banco.name == "Prof. Silva Atualizado"
    assert no_banco.email == "silva@ufc.br"  # campo não atualizado permanece


@pytest.mark.asyncio
async def test_delete_remove_do_banco():
    doc = Professor(name="Para Deletar", email="del@ufc.br")
    await doc.insert()

    assert await Professor.get(doc.id) is not None

    repo = ProfessorRepository()
    await repo.delete(doc.id)

    assert await Professor.get(doc.id) is None
