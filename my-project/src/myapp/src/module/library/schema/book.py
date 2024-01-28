from typing import List

from core.schema import BaseCountSchema, BaseDateTimeSchema


class BookData(BaseDateTimeSchema):
    code: str
    title: str


class Book(BookData):
    id: str

    class Config:
        orm_mode = True
        from_attributes = True


class BookResult(BaseCountSchema):
    data: List[Book]
