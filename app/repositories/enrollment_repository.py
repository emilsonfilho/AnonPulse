from app.models.enrollment import Enrollment
from app.repositories.base_repository import BaseRepository

class EnrollmentRepository(BaseRepository[Enrollment]):
    """
    Repositório para gerenciar as operações de banco de dados da entidade Enrollment.

    Esta classe herda de BaseRepository e fornece a abstração necessária para
    realizar operações assíncronas de persistência e consulta associadas às
    matrículas de alunos (Enrollment) nas turmas.
    """

    def __init__(self) -> None:
        """
        Inicializa o repositório de matrículas.
        """
        super().__init__(model=Enrollment)