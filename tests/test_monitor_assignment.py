import pytest
from app.models.monitor_assignment import MonitorAssignment
from app.repositories.monitor_assignment_repository import MonitorAssignmentRepository


@pytest.mark.asyncio
async def test_insert_persiste_no_banco(assignment):
    no_banco = await MonitorAssignment.get(assignment.id)
    assert no_banco is not None
    assert no_banco.weekly_hours == 4


@pytest.mark.asyncio
async def test_get_por_id(assignment, params):
    repo = MonitorAssignmentRepository()
    result = await repo.get(assignment.id)
    assert result is not None
    assert result.id == assignment.id


@pytest.mark.asyncio
async def test_list_all_contem_assignment(assignment, params):
    repo = MonitorAssignmentRepository()
    page = await repo.list_all(params)
    ids = [item.id for item in page.items]
    assert assignment.id in ids


@pytest.mark.asyncio
async def test_update_weekly_hours_persiste_no_banco(assignment):
    repo = MonitorAssignmentRepository()
    await repo.update(assignment.id, {"weekly_hours": 8})

    no_banco = await MonitorAssignment.get(assignment.id)
    assert no_banco.weekly_hours == 8
