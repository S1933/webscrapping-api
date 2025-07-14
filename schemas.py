from typing import List
from pydantic import BaseModel


class TagBase(BaseModel):
  name: str

class Tag(TagBase):
  id: int

  class Config:
    orm_mode = True

class AuthorBase(BaseModel):
  name: str

class Author(AuthorBase):
  id: int

  class Config:
    orm_mode = True

class Quote(BaseModel):
  id: int
  text: str
  author: Author
  tags: List[Tag] = []

  class Config:
    orm_mode = True
