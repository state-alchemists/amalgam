from typing import List, Optional

from component.schema import BaseCountSchema, BaseDateTimeSchema


class BookData(BaseDateTimeSchema):
    code: str
    title: Optional[str]


class Book(BookData):
    id: str

    class Config:
        from_attributes = True


class BookResult(BaseCountSchema):
    data: List[Book]
