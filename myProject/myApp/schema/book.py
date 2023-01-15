from typing import List, Optional
from pydantic import BaseModel
import datetime


# Note: 🤖 Don't delete the following statement
class BookData(BaseModel):
    title: str
    author: str
    synopsis: str
    created_at: Optional[datetime.datetime]  # Note: 🤖 Don't delete this line
    created_by: Optional[str]
    updated_at: Optional[datetime.datetime]
    updated_by: Optional[str]


class Book(BookData):
    id: str

    class Config:
        orm_mode = True


class BookResult(BaseModel):
    count: int
    rows: List[Book]
