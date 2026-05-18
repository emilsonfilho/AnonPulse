from fastapi import APIRouter, Depends
from fastapi_pagination import Params, Page
from app.api.dependencies.services import get_feedback_type_service
from app.schemas.feedback_type_schema import FeedbackTypeResponse
from app.services.feedback_type_service import FeedbackTypeService

api_router = APIRouter(prefix="/v1/feedback-types", tags=["Feedback Types"])

@api_router.get("/", response_model=Page[FeedbackTypeResponse])
async def list_feedback_types(
    feedback_type_service: FeedbackTypeService = Depends(get_feedback_type_service),
    params: Params = Depends()
):
    return await feedback_type_service.list_all(params)