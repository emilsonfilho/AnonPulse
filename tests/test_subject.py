import pytest
from app.models.subject import Subject
from app.repositories.subject_repository import SubjectRepository


@pytest.mark.asyncio
async def test_insert_persiste_no_banco(subject):
    """Garante que o insert realmente salvou no MongoDB."""
    no_banco = await Subject.get(subject.id)
    assert no_banco is not None
    assert no_banco.id == subject.id
    assert no_banco.cod == "QXD0001-TEST"
    assert no_banco.name == "Computação Gráfica"


@pytest.mark.asyncio
async def test_get_por_id(subject, params):
    repo = SubjectRepository()
    result = await repo.get(subject.id)
    assert result is not None
    assert result.id == subject.id


@pytest.mark.asyncio
async def test_list_all_contem_subject(subject, params):
    repo = SubjectRepository()
    page = await repo.list_all(params)
    ids = [item.id for item in page.items]
    assert subject.id in ids


@pytest.mark.asyncio
async def test_count_maior_que_zero(subject, params):
    repo = SubjectRepository()
    total = await repo.count()
    assert total >= 1


@pytest.mark.asyncio
async def test_update_persiste_no_banco(subject, params):
    repo = SubjectRepository()
    await repo.update(subject.id, {"name": "CG Atualizado"})

    no_banco = await Subject.get(subject.id)
    assert no_banco.name == "CG Atualizado"
    assert no_banco.cod == "QXD0001-TEST"  # campo não atualizado permanece


@pytest.mark.asyncio
async def test_delete_remove_do_banco(params):
    """Cria e deleta um subject próprio para não interferir com outros testes."""
    doc = Subject(cod="QXD9999-DEL", name="Para Deletar")
    await doc.insert()

    no_banco = await Subject.get(doc.id)
    assert no_banco is not None

    repo = SubjectRepository()
    await repo.delete(doc.id)

    apos_delete = await Subject.get(doc.id)
    assert apos_delete is None
