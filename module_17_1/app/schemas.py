from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int
    slug: str


class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    age: int


class CreateTask(BaseModel):
    title: str
    content: str
    priority: int
    completed: bool
    slug: str


class UpdateTask(BaseModel):
    content: str
    priority: int
    completed: bool
