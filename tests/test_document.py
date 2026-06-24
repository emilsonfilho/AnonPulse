import pytest
from app.models.document_metadata import DocumentMetadata
from app.repositories.document_repository import DocumentRepository


@pytest.mark.asyncio
async def test_insert_persiste_no_banco(documento):
    no_banco = await DocumentMetadata.get(documento.id)
    assert no_banco is not None
    assert no_banco.original_filename == "relatorio.pdf"
    assert no_banco.content_type == "application/pdf"
    assert no_banco.extension == ".pdf"
    assert no_banco.size_bytes == 204800


@pytest.mark.asyncio
async def test_get_por_id(documento, params):
    repo = DocumentRepository()
    result = await repo.get(documento.id)
    assert result is not None
    assert result.id == documento.id


@pytest.mark.asyncio
async def test_list_all_contem_documento(documento, params):
    repo = DocumentRepository()
    page = await repo.list_all(params)
    ids = [item.id for item in page.items]
    assert documento.id in ids


@pytest.mark.asyncio
async def test_list_by_assignment_retorna_documento(documento, assignment, params):
    repo = DocumentRepository()
    page = await repo.list_by_assignment(assignment.id, params)
    ids = [item.id for item in page.items]
    assert documento.id in ids


@pytest.mark.asyncio
async def test_list_by_assignment_id_errado_retorna_vazio(params):
    from beanie import PydanticObjectId

    repo = DocumentRepository()
    id_falso = PydanticObjectId()
    page = await repo.list_by_assignment(id_falso, params)
    assert page.total == 0
