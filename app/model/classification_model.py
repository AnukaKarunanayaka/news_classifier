from pydantic import BaseModel


class ClassificationModel(BaseModel):
    content: str
    category_count: int
