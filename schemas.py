from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum
import re


class BlogBase(BaseModel):
    age: int
    name: str


class Blog(BlogBase):
    class Config:
        from_attributes = True


class CourseName(str, Enum):
    ml = "Machine Learning"
    dsa = "DSA"
    java = "Java"
    python = "Python"
    stl = "STL"


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    course: CourseName

    @validator("email")
    def email_must_be_gmail(cls, v):
        pattern = r"^[A-Za-z0-9._%+-]+@gmail\.com$"
        if not re.match(pattern, v):
            raise ValueError("Email must be a valid Gmail address")
        return v


class User(BaseModel):
    id: int
    name: str
    email: str
    course: CourseName

    class Config:
        from_attributes = True


class showUser(BaseModel):
    id: int
    name: str
    email: str
    course: CourseName
    lazy: List[Blog] = Field(default_factory=list)

    class Config:
        from_attributes = True


class ShowBlog(BaseModel):
    name: str
    creator: showUser

    class Config:
        from_attributes = True


class Login(BaseModel):
    email: str
    password: str


class CourseLogin(BaseModel):
    email: str
    password: str
    course: CourseName


class CourseStatus(BaseModel):
    course: CourseName
    is_new: bool
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
