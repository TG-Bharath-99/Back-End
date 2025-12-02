from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Table(Base):
    __tablename__ = "Blog_Table"
    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("User_Table.id"))
    creator = relationship("User", back_populates="lazy")


class User(Base):
    __tablename__ = "User_Table"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    course = Column(String)
    lazy = relationship("Table", back_populates="creator")
    courses = relationship("UserCourse", back_populates="user")


class UserCourse(Base):
    __tablename__ = "User_Course"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User_Table.id"))
    course = Column(String)
    user = relationship("User", back_populates="courses")
