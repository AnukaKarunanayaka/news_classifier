from pydantic import BaseModel


class ClassificationModel(BaseModel):
    content: str
