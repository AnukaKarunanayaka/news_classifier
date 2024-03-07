from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from app.model.classification_model import ClassificationModel
from app.model.generic_response import GenericResponse
from app.service.classification_service import ClassificationService

router = APIRouter(
    prefix="/v1/api/classification",
    tags=["Dashboard"]
)
classification_service = ClassificationService()


@router.post("/", status_code=status.HTTP_200_OK)
async def start_classification(classification_model: ClassificationModel):
    try:
        classification = classification_service.get_classification(classification_model.content)

        return GenericResponse.success("Classification Process Success", classification)
    except Exception as ex:
        return JSONResponse(status_code=400,
                            content=GenericResponse.failed(f"Classification Process Error: {str(ex)}", []))
