from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlmodel import select
from sqlalchemy import func
from typing import Any
from datetime import datetime

from app.repositories.base_repository import BaseRepository
from app.models.feedback import Feedback
from app.models.subject import Subject
from app.models.classroom import Classroom
from app.models.monitor_assignment import MonitorAssignment


class FeedbackRepository(BaseRepository[Feedback]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Feedback, session=session)

    async def search_by_text(self, term: str, params: Params) -> Page[Feedback]:
        search_term = f"%{term}%"

        query = (
            select(self.model)
            .where(self.model.text.ilike(search_term))
            .order_by(self.model.createdAt.desc())
        )

        return await paginate(self.session, query, params)

    async def list_by_monitor(
        self, monitor_registration: str, params: Params
    ) -> Page[Feedback]:
        query = (
            select(self.model)
            .join(MonitorAssignment)
            .where(MonitorAssignment.monitor_registration == monitor_registration)
        )

        return await paginate(self.session, query, params)

    async def count_by_monitor(self, params: Params) -> Page[Any]:
        query = (
            select(MonitorAssignment.monitor_registration, func.count(self.model.id))
            .join(MonitorAssignment)
            .group_by(MonitorAssignment.monitor_registration)
        )

        return await paginate(self.session, query, params)

    async def count_by_subject(self, params: Params) -> Page[Any]:
        query = (
            select(Subject.name, func.count(self.model.id))
            .select_from(self.model)
            .join(MonitorAssignment)
            .join(Classroom)
            .join(Subject)
            .group_by(Subject.name)
        )

        return await paginate(self.session, query, params)

    async def list_by_date_range(
        self,
        params: Params,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> Page[Feedback]:

        query = select(self.model).order_by(self.model.createdAt.desc())

        if start_date:
            query = query.where(self.model.createdAt >= start_date)

        if end_date:
            query = query.where(self.model.createdAt <= end_date)

        return await paginate(self.session, query, params)
