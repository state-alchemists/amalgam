from sqlalchemy import MetaData

from myapp.schema.book import Book

metadata = MetaData()
Book.metadata = metadata
Book.__table__.tometadata(metadata)
