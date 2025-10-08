from pydantic import BaseModel,Field
from typing import List,Optional

class BlogBase(BaseModel):
    age:int
    name:str

class Blog(BlogBase):
    class Config:
        from_attributes=True    

class User(BaseModel):
    name:str
    email:str
    password:str        

class showUser(BaseModel):
    name:str
    email:str
    lazy:List[Blog]=Field(default_factory=list)
    class Config:
        from_attributes=True

class ShowBlog(BaseModel):
    name:str
    creator:showUser
    class Config:
        from_attributes=True

class Login(BaseModel):
    username:str
    password:str        

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    email:Optional[str]=None 