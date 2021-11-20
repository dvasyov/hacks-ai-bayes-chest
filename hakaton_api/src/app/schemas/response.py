from pydantic import BaseModel, Field


class ResponseCategory(BaseModel):
    """
    Модель, описывающая структуру данных ответа
    """

    subcategory: str = Field(description="Категория продукции", example="")
    subcategory_code: str = Field(description="Код продукции", example="")
