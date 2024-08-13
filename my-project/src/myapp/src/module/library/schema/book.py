from datetime import date, datetime, time
from typing import Optional

from component.schema import BaseCountSchema, BaseDateTimeSchema


class BookData(BaseDateTimeSchema):
    code: str
    title: Optional[str]
    page_number: Optional[int]
    purchase_date: Optional[date]
    available: Optional[bool]
    synopsis: Optional[str]


class Book(BookData):
    id: str

    class Config:
        from_attributes = True


class BookResult(BaseCountSchema):
    data: list[Book]
