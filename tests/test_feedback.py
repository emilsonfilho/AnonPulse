import pytest
from datetime import datetime, timezone, timedelta
from app.models.feedback import Feedback
from app.repositories.feedback_repository import FeedbackRepository


@pytest.mark.asyncio
async def test_insert_persiste_no_banco(feedback):
    no_banco = await Feedback.get(feedback.id)
    assert no_banco is not None
    assert no_banco.registration == "hash_001"
    assert no_banco.text == "Monitor excelente, explicou muito bem o conteúdo."
    assert no_banco.rating == 5


@pytest.mark.asyncio
async def test_get_por_id(feedback, params):
    repo = FeedbackRepository()
    result = await repo.get(feedback.id)
    assert result is not None
    assert result.id == feedback.id


@pytest.mark.asyncio
async def test_list_all_contem_feedback(feedback, params):
    repo = FeedbackRepository()
    page = await repo.list_all(params)
    ids = [item.id for item in page.items]
    assert feedback.id in ids


@pytest.mark.asyncio
async def test_search_by_text_encontra_resultado(feedback, params):
    repo = FeedbackRepository()
    page = await repo.search_by_text("excelente", params)
    assert page.total >= 1
    textos = [item.text for item in page.items]
    assert any("excelente" in t.lower() for t in textos)


@pytest.mark.asyncio
async def test_search_by_text_case_insensitive(feedback, params):
    repo = FeedbackRepository()
    page = await repo.search_by_text("EXCELENTE", params)
    assert page.total >= 1


@pytest.mark.asyncio
async def test_search_by_text_sem_resultado(feedback, params):
    repo = FeedbackRepository()
    page = await repo.search_by_text("xyzabcnaoexiste123", params)
    assert page.total == 0


@pytest.mark.asyncio
async def test_list_by_date_range_start_date(feedback, params):
    repo = FeedbackRepository()
    inicio = datetime.now(timezone.utc) - timedelta(days=1)
    page = await repo.list_by_date_range(params, start_date=inicio)
    assert page.total >= 1
    ids = [item["_id"] for item in page.items]
    assert str(feedback.id) in [str(i) for i in ids]


@pytest.mark.asyncio
async def test_list_by_date_range_end_date(feedback, params):
    repo = FeedbackRepository()
    fim = datetime.now(timezone.utc) + timedelta(days=1)
    page = await repo.list_by_date_range(params, end_date=fim)
    assert page.total >= 1


@pytest.mark.asyncio
async def test_list_by_date_range_por_ano(feedback, params):
    repo = FeedbackRepository()
    ano = datetime.now(timezone.utc).year
    page = await repo.list_by_date_range(params, year=ano)
    assert page.total >= 1


@pytest.mark.asyncio
async def test_list_by_date_range_fora_do_intervalo(feedback, params):
    """Filtra por data futura — não deve retornar o feedback de hoje."""
    repo = FeedbackRepository()
    inicio = datetime.now(timezone.utc) + timedelta(days=10)
    page = await repo.list_by_date_range(params, start_date=inicio)
    ids = [str(item.get("_id", "")) for item in page.items]
    assert str(feedback.id) not in ids


@pytest.mark.asyncio
async def test_list_by_student_hash_encontra(feedback, params):
    repo = FeedbackRepository()
    page = await repo.list_by_student_hash("hash_001", params)
    assert page.total >= 1
    registrations = [item.registration for item in page.items]
    assert "hash_001" in registrations


@pytest.mark.asyncio
async def test_list_by_student_hash_inexistente_retorna_vazio(feedback, params):
    repo = FeedbackRepository()
    page = await repo.list_by_student_hash("hash_nao_existe_xyz", params)
    assert page.total == 0


@pytest.mark.asyncio
async def test_list_by_monitor_retorna_feedback(feedback, monitor, params):
    repo = FeedbackRepository()
    page = await repo.list_by_monitor(monitor.registration, params)
    assert page.total >= 1


@pytest.mark.asyncio
async def test_list_by_monitor_inexistente_levanta_excecao(params):
    from app.core.exceptions.custom_exceptions import MonitorNotFoundException
    repo = FeedbackRepository()
    with pytest.raises(MonitorNotFoundException):
        await repo.list_by_monitor("matricula_nao_existe", params)


@pytest.mark.asyncio
async def test_count_by_monitor_retorna_agregacao(feedback, params):
    repo = FeedbackRepository()
    page = await repo.count_by_monitor(params)
    assert page.total >= 1
    # verifica estrutura do item retornado
    primeiro = page.items[0]
    assert "monitor_registration" in primeiro
    assert "count" in primeiro
    assert primeiro["count"] >= 1


@pytest.mark.asyncio
async def test_count_by_subject_retorna_agregacao(feedback, params):
    repo = FeedbackRepository()
    page = await repo.count_by_subject(params)
    assert page.total >= 1
    primeiro = page.items[0]
    assert "subject_name" in primeiro
    assert "feedback_count" in primeiro
    assert primeiro["feedback_count"] >= 1


@pytest.mark.asyncio
async def test_delete_remove_do_banco(assignment):
    from app.core.enums import MessageType
    doc = Feedback(
        registration="hash_del",
        text="Será deletado.",
        rating=1,
        assignment=assignment,
        type=MessageType.SUGESTAO,
        created_at=datetime.now(timezone.utc),
    )
    await doc.insert()

    assert await Feedback.get(doc.id) is not None

    repo = FeedbackRepository()
    await repo.delete(doc.id)

    assert await Feedback.get(doc.id) is None
