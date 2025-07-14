
from sqlalchemy import Table, Text, create_engine, Column, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

DATABASE_URL = "sqlite:///quotes.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

quote_tag_association = Table('quote_tag', Base.metadata,
  Column('quote_id', Integer, ForeignKey('quotes.id')),
  Column('tag_id', Integer, ForeignKey('tags.id')),
)

class Author(Base):
  __tablename__ = 'authors'
  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  name = Column(Integer, index=True)

  quotes = relationship("Quote", back_populates="author")

class Tag(Base):
  __tablename__ = 'tags'
  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  name = Column(Integer, index=True)

  quotes = relationship("Quote", secondary=quote_tag_association, back_populates="tags")

class Quote(Base):
  __tablename__ = 'quotes'
  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  text = Column(Text, nullable=True)
  author_id = Column(Integer, ForeignKey('authors.id'))
  author = relationship("Author", back_populates="quotes")
  tags = relationship("Tag", secondary=quote_tag_association, back_populates="quotes")

def create_db_tables():
  Base.metadata.create_all(bind=engine)
