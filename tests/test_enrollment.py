import pytest
from app.models.enrollment import Enrollment
from app.repositories.enrollment_repository import EnrollmentRepository


@pytest.mark.asyncio
async def test_insert_persiste_no_banco(enrollment):
    no_banco = await Enrollment.get(enrollment.id)
    assert no_banco is not None
    assert no_banco.is_active is True


@pytest.mark.asyncio
async def test_get_por_id(enrollment, params):
    repo = EnrollmentRepository()
    result = await repo.get(enrollment.id)
    assert result is not None
    assert result.id == enrollment.id


@pytest.mark.asyncio
async def test_list_all_contem_enrollment(enrollment, params):
    repo = EnrollmentRepository()
    page = await repo.list_all(params)
    ids = [item.id for item in page.items]
    assert enrollment.id in ids


@pytest.mark.asyncio
async def test_update_is_active_persiste_no_banco(enrollment):
    repo = EnrollmentRepository()
    await repo.update(enrollment.id, {"is_active": False})

    no_banco = await Enrollment.get(enrollment.id)
    assert no_banco.is_active is False


@pytest.mark.asyncio
async def test_delete_remove_do_banco(student, classroom):
    doc = Enrollment(student=student, classroom=classroom)
    await doc.insert()

    assert await Enrollment.get(doc.id) is not None

    repo = EnrollmentRepository()
    await repo.delete(doc.id)

    assert await Enrollment.get(doc.id) is None
