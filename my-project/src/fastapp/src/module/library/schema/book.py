from typing import List
from core.schema import BaseDateTimeSchema, BaseCountSchema


class BookData(BaseDateTimeSchema):
    code: str
    title: str


class Book(BookData):
    id: str

    class Config:
        orm_mode = True


class BookResult(BaseCountSchema):
    data: List[Book]
