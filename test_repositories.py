"""
Script de teste para todos os repositórios do AnonPulse.

Cobre:
  - CRUD básico (BaseRepository)
  - Métodos específicos de cada repositório
  - Consultas complexas e agregações do FeedbackRepository

Uso:
    python test_repositories.py
"""

import asyncio
import sys
from datetime import datetime, timezone, timedelta

from fastapi_pagination import Params

from app.core.database import init_db, close_db
from app.core.enums import MessageType

from app.models.subject import Subject
from app.models.professor import Professor
from app.models.classroom import Classroom
from app.models.student import Student
from app.models.monitor import Monitor
from app.models.monitor_assignment import MonitorAssignment
from app.models.enrollment import Enrollment
from app.models.feedback import Feedback
from app.models.document_metadata import DocumentMetadata

from app.repositories.subject_repository import SubjectRepository
from app.repositories.professor_repository import ProfessorRepository
from app.repositories.classroom_repository import ClassroomRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.monitor_repository import MonitorRepository
from app.repositories.monitor_assignment_repository import MonitorAssignmentRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.document_repository import DocumentRepository

# ── helpers ────────────────────────────────────────────────────────────────────

PARAMS = Params(page=1, size=10)
PASS   = "✅"
FAIL   = "❌"
SEP    = "─" * 60

results: list[tuple[str, bool, str]] = []


def ok(label: str) -> None:
    results.append((label, True, ""))
    print(f"  {PASS} {label}")


def fail(label: str, err: Exception) -> None:
    results.append((label, False, str(err)))
    print(f"  {FAIL} {label}: {err}")


async def run(label: str, coro) -> any:
    try:
        result = await coro
        ok(label)
        return result
    except Exception as e:
        fail(label, e)
        return None


def section(title: str) -> None:
    print(f"\n{SEP}\n  {title}\n{SEP}")


# ── fixtures ───────────────────────────────────────────────────────────────────

async def criar_fixtures() -> dict:
    """Cria e persiste dados mínimos interligados para os testes."""
    section("🔧 Criando fixtures")

    # Subject: cod (unique), name, classrooms
    subject = Subject(cod="QXD0001-TEST", name="Computação Gráfica")
    await subject.insert()
    ok("Subject inserido")

    # Professor: name, email, classrooms
    professor = Professor(name="Prof. Silva", email="silva@ufc.br")
    await professor.insert()
    ok("Professor inserido")

    # Classroom: cod (unique), subject (Link), professor (Link)
    classroom = Classroom(
        cod="T01-2025-TEST",
        subject=subject,
        professor=professor,
    )
    await classroom.insert()
    ok("Classroom inserido")

    # Student: registration (unique), enrollments
    student = Student(registration="2023001-TEST")
    await student.insert()
    ok("Student inserido")

    # Monitor: registration (unique), name, email, assignments
    monitor = Monitor(
        registration="2022001-TEST",
        name="Monitor João",
        email="joao@ufc.br",
    )
    await monitor.insert()
    ok("Monitor inserido")

    # MonitorAssignment: weekly_hours, monitor (Link), classroom (Link)
    assignment = MonitorAssignment(
        weekly_hours=4,
        monitor=monitor,
        classroom=classroom,
    )
    await assignment.insert()
    ok("MonitorAssignment inserido")

    # Enrollment: student (Link), classroom (Link), is_active, enrolled_at
    enrollment = Enrollment(
        student=student,
        classroom=classroom,
    )
    await enrollment.insert()
    ok("Enrollment inserido")

    now = datetime.now(timezone.utc)

    # Feedback: registration (hash), text, rating, assignment (Link), type
    feedback = Feedback(
        registration="hash_anonimo_001",
        text="Monitor excelente, explicou muito bem o conteúdo.",
        rating=5,
        assignment=assignment,
        type=MessageType.ELOGIO,
        created_at=now,
    )
    await feedback.insert()
    ok("Feedback inserido")

    feedback2 = Feedback(
        registration="hash_anonimo_002",
        text="Poderia melhorar a pontualidade nas sessões.",
        rating=3,
        assignment=assignment,
        type=MessageType.CRITICA,
        created_at=now - timedelta(days=10),
    )
    await feedback2.insert()
    ok("Feedback2 inserido")

    # DocumentMetadata: original_filename, content_type, extension, size_bytes, assignment (Link)
    doc = DocumentMetadata(
        original_filename="relatorio.pdf",
        content_type="application/pdf",
        extension=".pdf",
        size_bytes=204800,
        assignment=assignment,
    )
    await doc.insert()
    ok("DocumentMetadata inserido")

    return {
        "subject":    subject,
        "professor":  professor,
        "classroom":  classroom,
        "student":    student,
        "monitor":    monitor,
        "assignment": assignment,
        "enrollment": enrollment,
        "feedback":   feedback,
        "feedback2":  feedback2,
        "doc":        doc,
    }


# ── limpeza ────────────────────────────────────────────────────────────────────

async def limpar_fixtures(fx: dict) -> None:
    section("🧹 Limpando fixtures")
    # ordem inversa respeita dependências (filho antes do pai)
    for nome, obj in reversed(list(fx.items())):
        try:
            await obj.delete()
            ok(f"{nome} deletado")
        except Exception as e:
            fail(f"{nome} delete", e)


# ── testes por repositório ─────────────────────────────────────────────────────

async def testar_subject(fx: dict) -> None:
    section("📚 SubjectRepository")
    repo = SubjectRepository()

    await run("list_all",    repo.list_all(PARAMS))
    await run("get por id",  repo.get(fx["subject"].id))
    await run("count",       repo.count())
    await run("update name", repo.update(fx["subject"].id, {"name": "CG Atualizado"}))


async def testar_professor(fx: dict) -> None:
    section("🧑‍🏫 ProfessorRepository")
    repo = ProfessorRepository()

    await run("list_all",    repo.list_all(PARAMS))
    await run("get por id",  repo.get(fx["professor"].id))
    await run("count",       repo.count())
    await run("update name", repo.update(fx["professor"].id, {"name": "Prof. Silva Atualizado"}))


async def testar_classroom(fx: dict) -> None:
    section("🏫 ClassroomRepository")
    repo = ClassroomRepository()

    await run("list_all",          repo.list_all(PARAMS))
    await run("get por id",        repo.get(fx["classroom"].id))
    await run("list_by_professor", repo.list_by_professor(fx["professor"].id, PARAMS))
    await run("list_by_subject",   ClassroomRepository.list_by_subject(fx["subject"].cod, PARAMS))


async def testar_student(fx: dict) -> None:
    section("🎓 StudentRepository")
    repo = StudentRepository()

    await run("list_all",   repo.list_all(PARAMS))
    await run("get por id", repo.get(fx["student"].id))
    await run("count",      repo.count())


async def testar_monitor(fx: dict) -> None:
    section("🧑‍💻 MonitorRepository")
    repo = MonitorRepository()

    await run("list_all",    repo.list_all(PARAMS))
    await run("get por id",  repo.get(fx["monitor"].id))
    await run("count",       repo.count())
    await run("update name", repo.update(fx["monitor"].id, {"name": "Monitor João Atualizado"}))


async def testar_assignment(fx: dict) -> None:
    section("📋 MonitorAssignmentRepository")
    repo = MonitorAssignmentRepository()

    await run("list_all",        repo.list_all(PARAMS))
    await run("get por id",      repo.get(fx["assignment"].id))
    await run("count",           repo.count())
    await run("update hours",    repo.update(fx["assignment"].id, {"weekly_hours": 6}))


async def testar_enrollment(fx: dict) -> None:
    section("📝 EnrollmentRepository")
    repo = EnrollmentRepository()

    await run("list_all",        repo.list_all(PARAMS))
    await run("get por id",      repo.get(fx["enrollment"].id))
    await run("count",           repo.count())
    await run("update is_active",repo.update(fx["enrollment"].id, {"is_active": False}))


async def testar_document(fx: dict) -> None:
    section("📄 DocumentRepository")
    repo = DocumentRepository()

    await run("list_all",          repo.list_all(PARAMS))
    await run("get por id",        repo.get(fx["doc"].id))
    await run("list_by_assignment",repo.list_by_assignment(fx["assignment"].id, PARAMS))


async def testar_feedback(fx: dict) -> None:
    section("💬 FeedbackRepository")
    repo = FeedbackRepository()

    # CRUD básico
    await run("list_all",   repo.list_all(PARAMS))
    await run("get por id", repo.get(fx["feedback"].id))
    await run("count",      repo.count())

    # Busca textual (regex)
    await run("search_by_text ('monitor')", repo.search_by_text("monitor", PARAMS))
    await run("search_by_text ('pontual')", repo.search_by_text("pontual", PARAMS))

    # Filtro por data
    now = datetime.now(timezone.utc)
    await run(
        "list_by_date_range (start_date)",
        repo.list_by_date_range(PARAMS, start_date=now - timedelta(days=30))
    )
    await run(
        "list_by_date_range (end_date)",
        repo.list_by_date_range(PARAMS, end_date=now)
    )
    await run(
        "list_by_date_range (intervalo completo)",
        repo.list_by_date_range(
            PARAMS,
            start_date=now - timedelta(days=30),
            end_date=now
        )
    )
    await run(
        "list_by_date_range (por ano)",
        repo.list_by_date_range(PARAMS, year=now.year)
    )

    # Por hash do aluno (anonimato)
    await run(
        "list_by_student_hash (hash_001)",
        repo.list_by_student_hash("hash_anonimo_001", PARAMS)
    )
    await run(
        "list_by_student_hash (hash inexistente)",
        repo.list_by_student_hash("hash_nao_existe", PARAMS)
    )

    # Por monitor (pipeline com $lookup duplo)
    await run(
        "list_by_monitor",
        repo.list_by_monitor(fx["monitor"].registration, PARAMS)
    )

    # Agregações
    await run("count_by_monitor", repo.count_by_monitor(PARAMS))
    await run("count_by_subject", repo.count_by_subject(PARAMS))


# ── sumário final ──────────────────────────────────────────────────────────────

def imprimir_sumario() -> None:
    section("📊 Sumário")
    passou = [r for r in results if r[1]]
    falhou = [r for r in results if not r[1]]

    print(f"  Total  : {len(results)}")
    print(f"  {PASS} Passou: {len(passou)}")
    print(f"  {FAIL} Falhou: {len(falhou)}")

    if falhou:
        print("\n  Falhas:")
        for label, _, err in falhou:
            print(f"    • {label}: {err}")

    print()


# ── entry point ────────────────────────────────────────────────────────────────

async def main() -> None:
    print("\n🚀 Iniciando testes dos repositórios AnonPulse\n")

    await init_db([
        Subject,
        Professor,
        Classroom,
        Student,
        Monitor,
        MonitorAssignment,
        Enrollment,
        Feedback,
        DocumentMetadata,
    ])

    fx = await criar_fixtures()

    try:
        await testar_subject(fx)
        await testar_professor(fx)
        await testar_classroom(fx)
        await testar_student(fx)
        await testar_monitor(fx)
        await testar_assignment(fx)
        await testar_enrollment(fx)
        await testar_document(fx)
        await testar_feedback(fx)
    finally:
        await limpar_fixtures(fx)
        await close_db()

    imprimir_sumario()

    if any(not r[1] for r in results):
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
