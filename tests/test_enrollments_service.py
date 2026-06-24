import pytest
from beanie import PydanticObjectId

from app.services.enrollment_service import EnrollmentService
from app.repositories.enrollment_repository import EnrollmentRepository
from app.schemas.enrollment_schema import CreateEnrollmentRequest
from app.models.enrollment import Enrollment
from app.core.exceptions.custom_exceptions import (
    EnrollmentAlreadyExistsException,
    EnrollmentNotFoundException,
)


# Criamos uma fixture para injetar o serviço nos testes facilmente
@pytest.fixture
def enrollment_service():
    repo = EnrollmentRepository()
    return EnrollmentService(repo)


@pytest.mark.asyncio
async def test_create_enrollment_success(enrollment_service, student, classroom):
    """Testa se uma inscrição é criada com sucesso e salva no banco de dados."""

    # NOTA: Adapte os parâmetros de CreateEnrollmentRequest dependendo de como
    # o seu schema foi construído. Se ele esperar IDs em vez do objeto inteiro,
    # troque para student_id=student.id, classroom_id=classroom.id
    request = CreateEnrollmentRequest(
        student_id=student.id, classroom_cod=classroom.cod
    )

    response = await enrollment_service.create(request)

    # Verificações na resposta mapeada
    assert response is not None
    assert response.id is not None

    # Verifica se os dados realmente foram persistidos e se o status inicial é ativo
    db_enrollment = await Enrollment.get(response.id)
    assert db_enrollment is not None
    assert db_enrollment.is_active is True


@pytest.mark.asyncio
async def test_create_enrollment_already_exists(
    enrollment_service, enrollment, student, classroom
):
    """Testa se o serviço impede a criação de uma inscrição duplicada."""

    # A fixture 'enrollment' (injetada nos parâmetros) já criou uma inscrição
    # para este 'student' e 'classroom' no banco de dados.

    request = CreateEnrollmentRequest(
        student_id=student.id,
        classroom_cod=classroom.cod,
    )

    # Ao tentar criar exatamente a mesma inscrição, deve levantar a exceção
    with pytest.raises(EnrollmentAlreadyExistsException):
        await enrollment_service.create(request)


@pytest.mark.asyncio
async def test_delete_enrollment_success(enrollment_service, enrollment):
    """Testa a exclusão lógica (soft delete) de uma inscrição."""

    # Executa o método de exclusão usando o ID da inscrição fornecida pela fixture
    await enrollment_service.delete(enrollment.id)

    # Busca o documento diretamente no banco de dados para confirmar a alteração
    db_enrollment = await Enrollment.get(enrollment.id)

    # O documento ainda deve existir, mas seu status 'is_active' deve ser False
    assert db_enrollment is not None
    assert db_enrollment.is_active is False


@pytest.mark.asyncio
async def test_delete_enrollment_not_found(enrollment_service):
    """Testa a tentativa de deletar uma inscrição que não existe."""

    # Gera um ObjectId aleatório válido, mas que não está no banco
    random_id = PydanticObjectId()

    # Deve lançar a exceção de Não Encontrado
    with pytest.raises(EnrollmentNotFoundException):
        await enrollment_service.delete(random_id)
