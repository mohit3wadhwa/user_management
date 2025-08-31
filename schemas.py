from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    age: int
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
