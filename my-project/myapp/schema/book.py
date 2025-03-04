import datetime

import ulid
from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class BookBase(SQLModel):
    isbn: str
    title: str = ""
    author: str = ""


class BookCreate(BookBase):
    def with_audit(self, created_by: str) -> "BookCreateWithAudit":
        return BookCreateWithAudit(**self.model_dump(), created_by=created_by)


class BookCreateWithAudit(BookCreate):
    created_by: str


class BookUpdate(SQLModel):
    isbn: str | None = None
    title: str | None = None
    author: str | None = None

    def with_audit(self, updated_by: str) -> "BookUpdateWithAudit":
        return BookUpdateWithAudit(**self.model_dump(), updated_by=updated_by)


class BookUpdateWithAudit(BookUpdate):
    updated_by: str


class BookResponse(BookBase):
    id: str


class MultipleBookResponse(BaseModel):
    data: list[BookResponse]
    count: int


class Book(SQLModel, table=True):
    __tablename__ = "books"
    id: str = Field(default_factory=lambda: ulid.new().str, primary_key=True)
    created_at: datetime.datetime = Field(index=True)
    created_by: str = Field(index=True)
    updated_at: datetime.datetime | None = Field(index=True)
    updated_by: str | None = Field(index=True)
    isbn: str = Field(index=True)
    title: str | None = Field(index=False)
    author: str | None = Field(index=False)
