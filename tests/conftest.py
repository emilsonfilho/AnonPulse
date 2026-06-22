import asyncio
import pytest
import pytest_asyncio
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

@pytest_asyncio.fixture(scope="session", autouse=True)
async def database():
    await init_db([
        Subject, Professor, Classroom, Student,
        Monitor, MonitorAssignment, Enrollment,
        Feedback, DocumentMetadata,
    ])
    yield
    await close_db()


@pytest_asyncio.fixture
async def subject():
    doc = Subject(cod="QXD0001-TEST", name="Computação Gráfica")
    await doc.insert()
    yield doc
    await Subject.find_one(Subject.id == doc.id).delete()


@pytest_asyncio.fixture
async def professor():
    doc = Professor(name="Prof. Silva", email="silva@ufc.br")
    await doc.insert()
    yield doc
    await Professor.find_one(Professor.id == doc.id).delete()


@pytest_asyncio.fixture
async def classroom(subject, professor):
    doc = Classroom(cod="T01-2025-TEST", subject=subject, professor=professor)
    await doc.insert()
    yield doc
    await Classroom.find_one(Classroom.id == doc.id).delete()


@pytest_asyncio.fixture
async def student():
    doc = Student(registration="2023001-TEST")
    await doc.insert()
    yield doc
    await Student.find_one(Student.id == doc.id).delete()


@pytest_asyncio.fixture
async def monitor():
    doc = Monitor(registration="2022001-TEST", name="Monitor João", email="joao@ufc.br")
    await doc.insert()
    yield doc
    await Monitor.find_one(Monitor.id == doc.id).delete()


@pytest_asyncio.fixture
async def assignment(monitor, classroom):
    doc = MonitorAssignment(weekly_hours=4, monitor=monitor, classroom=classroom)
    await doc.insert()
    yield doc
    await MonitorAssignment.find_one(MonitorAssignment.id == doc.id).delete()


@pytest_asyncio.fixture
async def enrollment(student, classroom):
    doc = Enrollment(student=student, classroom=classroom)
    await doc.insert()
    yield doc
    await Enrollment.find_one(Enrollment.id == doc.id).delete()


@pytest_asyncio.fixture
async def feedback(assignment):
    doc = Feedback(
        registration="hash_001",
        text="Monitor excelente, explicou muito bem o conteúdo.",
        rating=5,
        assignment=assignment,
        type=MessageType.ELOGIO,
        created_at=datetime.now(timezone.utc),
    )
    await doc.insert()
    yield doc
    await Feedback.find_one(Feedback.id == doc.id).delete()


@pytest_asyncio.fixture
async def feedback_antigo(assignment):
    doc = Feedback(
        registration="hash_002",
        text="Poderia melhorar a pontualidade nas sessões.",
        rating=3,
        assignment=assignment,
        type=MessageType.CRITICA,
        created_at=datetime.now(timezone.utc) - timedelta(days=10),
    )
    await doc.insert()
    yield doc
    await Feedback.find_one(Feedback.id == doc.id).delete()


@pytest_asyncio.fixture
async def documento(assignment):
    doc = DocumentMetadata(
        original_filename="relatorio.pdf",
        content_type="application/pdf",
        extension=".pdf",
        size_bytes=204800,
        assignment=assignment,
    )
    await doc.insert()
    yield doc
    await DocumentMetadata.find_one(DocumentMetadata.id == doc.id).delete()


@pytest.fixture
def params():
    return Params(page=1, size=10)
