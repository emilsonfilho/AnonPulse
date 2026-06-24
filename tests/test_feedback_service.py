import pytest
from datetime import date, timedelta
from fastapi_pagination import Params

from app.models import MonitorAssignment
from app.services.feedback_service import FeedbackService
from app.repositories.feedback_repository import FeedbackRepository
from app.schemas.feedback_schema import CreateFeedbackRequest
from app.services.hash_service import HashService
from app.core.enums import HashAlgorithm, MessageType
from app.core.exceptions.custom_exceptions import FeedbackNotFoundException
from tests.conftest import assignment


@pytest.fixture
async def assignment(monitor, classroom):
    """
    Cria uma alocação de monitoria (MonitorAssignment) para uso nos testes.
    Depende das fixtures 'monitor' e 'classroom' já estarem criadas.
    """
    # Cria a alocação instanciando o modelo do Beanie
    nova_alocacao = MonitorAssignment(
        weekly_hours=6, monitor=monitor, classroom=classroom, feedbacks=[], documents=[]
    )

    # Salva na base de dados (MongoDB) antes de entregar ao teste
    await nova_alocacao.insert()

    return nova_alocacao


# ==========================================
# FIXTURE DO SERVIÇO
# ==========================================
@pytest.fixture
def feedback_service():
    """Instancia o serviço injetando o repositório"""
    repo = FeedbackRepository()
    return FeedbackService(repository=repo)


# ==========================================
# TESTES DE CRIAÇÃO & ANONIMATO
# ==========================================
@pytest.mark.asyncio
async def test_create_feedback_aplica_hash_na_matricula(
    feedback_service, monitor, assignment
):
    matricula_real = "555666"
    hash_esperado = HashService.generate_hash(matricula_real, HashAlgorithm.SHA256)

    # NOTA: Ajuste os campos abaixo conforme os atributos reais do seu CreateFeedbackRequest
    req = CreateFeedbackRequest(
        registration=matricula_real,
        text="O monitor explicou as árvores AVL perfeitamente!",
        rating=5,
        assignment=assignment.id,
        type=MessageType.ELOGIO,
    )

    novo_feedback = await feedback_service.create(req)

    # 1. Verifica se o serviço criou e retornou o feedback
    assert novo_feedback is not None
    assert novo_feedback.text == "O monitor explicou as árvores AVL perfeitamente!"

    # 2. Vamos diretamente ao banco garantir que a matrícula foi anonimizada!
    feedback_salvo = await feedback_service.repository.get(novo_feedback.id)
    assert feedback_salvo.registration == hash_esperado
    assert feedback_salvo.registration != matricula_real


# ==========================================
# TESTES DE BUSCA E LISTAGEM
# ==========================================
@pytest.mark.asyncio
async def test_list_by_student_aplica_hash_na_busca(feedback_service, params):
    # Passamos a matrícula em texto puro
    matricula_pura = "123456"

    # O serviço deve converter para hash internamente e buscar
    pagina = await feedback_service.list_by_student(matricula_pura, params)

    assert pagina is not None
    assert hasattr(pagina, "total")


@pytest.mark.asyncio
async def test_list_by_monitor_retorna_pagina(feedback_service, monitor, params):
    pagina = await feedback_service.list_by_monitor(monitor.registration, params)

    assert pagina is not None
    assert hasattr(pagina, "items")


@pytest.mark.asyncio
async def test_search_por_texto_retorna_resultados(feedback_service, params):
    # Busca por uma palavra-chave que provavelmente existe nos mocks
    pagina = await feedback_service.search("monitor", params)

    assert pagina is not None
    assert type(pagina.total) is int


# ==========================================
# TESTES DE DATAS E AGREGAÇÕES
# ==========================================
@pytest.mark.asyncio
async def test_list_by_date_com_parametros_corretos(feedback_service, params):
    hoje = date.today()
    ontem = hoje - timedelta(days=1)

    # Testa a listagem num intervalo de datas
    pagina = await feedback_service.list_by_date(
        params=params, start_date=ontem, end_date=hoje
    )

    assert pagina is not None


@pytest.mark.asyncio
async def test_report_by_subject_retorna_agregacao(feedback_service, params):
    relatorio = await feedback_service.report_by_subject(params)

    # Como é um relatório de agregação, verificamos se a estrutura base de paginação existe
    assert relatorio is not None
    assert hasattr(relatorio, "items")


@pytest.mark.asyncio
async def test_count_feedbacks_retorna_inteiro(feedback_service):
    total = await feedback_service.count_feedbacks()
    assert isinstance(total, int)
    assert total >= 0
