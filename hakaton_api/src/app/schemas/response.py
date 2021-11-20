from typing import Match
from pydantic import BaseModel, Field


class ResponseCategory(BaseModel):
    """
    Модель, описывающая структуру данных ответа
    """

    match: int = Field(description="Соответствует", example="")
