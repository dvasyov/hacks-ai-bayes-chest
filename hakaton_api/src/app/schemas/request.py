from pydantic import BaseModel, Field


class RequestSample(BaseModel):
    """
    Модель, описывающая структуру данных сэмпла запроса
    """

    production_description: str = Field(description="Описание продукции", example="")
