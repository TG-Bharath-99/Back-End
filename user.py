from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import myFun
import models
import schemas

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/signup", response_model=schemas.User)
def create_user(request: schemas.UserCreate, db: Session = Depends(myFun)):
    existing_user = db.query(models.User).filter(models.User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = models.User(
        name=request.name,
        email=request.email,
        password=request.password,
        course=request.course.value
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(login: schemas.Login, db: Session = Depends(myFun)):
    user = db.query(models.User).filter(models.User.email == login.email).first()
    if not user or user.password != login.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": f"Welcome {user.name}"}


@router.get("/all", response_model=list[schemas.User])
def get_all_users(db: Session = Depends(myFun)):
    users = db.query(models.User).all()
    return users


@router.put("/update/{user_id}", response_model=schemas.User)
def update_user(user_id: int, request: schemas.UserCreate, db: Session = Depends(myFun)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = request.name
    user.email = request.email
    user.password = request.password
    user.course = request.course.value

    db.commit()
    db.refresh(user)
    return user


@router.delete("/delete/{email}")
def delete_user(email: str, db: Session = Depends(myFun)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": f"User with email {email} deleted successfully"}


@router.get("/courses")
def get_courses():
    return [course.value for course in schemas.CourseName]


@router.get("/course-topics/{course}", response_model=schemas.CourseTopics)
def get_course_topics(course: schemas.CourseName):
    data = {
        schemas.CourseName.python: [
            {
                "name": "Basics and Syntax",
                "links": [
                    {
                        "title": "Python Basic Syntax – W3Schools",
                        "url": "https://www.w3schools.com/python/python_syntax.asp"
                    }
                ]
            },
            {
                "name": "Loops",
                "links": [
                    {
                        "title": "Python For Loops – W3Schools",
                        "url": "https://www.w3schools.com/python/python_for_loops.asp"
                    }
                ]
            },
            {
                "name": "Conditional Statements",
                "links": [
                    {
                        "title": "Python If Else – W3Schools",
                        "url": "https://www.w3schools.com/python/python_conditions.asp"
                    }
                ]
            },
            {
                "name": "Functions",
                "links": [
                    {
                        "title": "Python Functions – W3Schools",
                        "url": "https://www.w3schools.com/python/python_functions.asp"
                    }
                ]
            }
        ],
        schemas.CourseName.java: [
            {
                "name": "Java Basics",
                "links": [
                    {
                        "title": "Java Tutorial – W3Schools",
                        "url": "https://www.w3schools.com/java/"
                    }
                ]
            },
            {
                "name": "OOP Concepts",
                "links": [
                    {
                        "title": "Java OOP – W3Schools",
                        "url": "https://www.w3schools.com/java/java_oop.asp"
                    }
                ]
            }
        ],
        schemas.CourseName.dsa: [
            {
                "name": "Arrays",
                "links": [
                    {
                        "title": "DSA Arrays – GeeksforGeeks",
                        "url": "https://www.geeksforgeeks.org/array-data-structure/"
                    }
                ]
            },
            {
                "name": "Linked Lists",
                "links": [
                    {
                        "title": "Linked List – GeeksforGeeks",
                        "url": "https://www.geeksforgeeks.org/data-structures/linked-list/"
                    }
                ]
            }
        ],
        schemas.CourseName.ml: [
            {
                "name": "Introduction to ML",
                "links": [
                    {
                        "title": "Machine Learning Crash Course – Google",
                        "url": "https://developers.google.com/machine-learning/crash-course"
                    }
                ]
            },
            {
                "name": "Supervised Learning",
                "links": [
                    {
                        "title": "Supervised Learning – Wikipedia",
                        "url": "https://en.wikipedia.org/wiki/Supervised_learning"
                    }
                ]
            }
        ],
        schemas.CourseName.stl: [
            {
                "name": "Vectors",
                "links": [
                    {
                        "title": "C++ Vectors – cppreference",
                        "url": "https://en.cppreference.com/w/cpp/container/vector"
                    }
                ]
            },
            {
                "name": "Maps",
                "links": [
                    {
                        "title": "C++ Maps – cppreference",
                        "url": "https://en.cppreference.com/w/cpp/container/map"
                    }
                ]
            }
        ],
    }

    topic_dicts = data.get(course, [])
    topics = [
        schemas.CourseTopic(
            id=i + 1,
            name=t["name"],
            links=[schemas.CourseLink(**link) for link in t["links"]]
        )
        for i, t in enumerate(topic_dicts)
    ]
    return schemas.CourseTopics(course=course, topics=topics)


    topic_names = data.get(course, [])
    topics = [
        schemas.CourseTopic(id=i + 1, name=name)
        for i, name in enumerate(topic_names)
    ]
    return schemas.CourseTopics(course=course, topics=topics)

@router.get("/profile/{email}", response_model=schemas.Profile)
def get_profile(email: str, db: Session = Depends(myFun)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/about")
def about():
    return {
        "app": "Learning Platform",
        "version": "1.0",
        "description": "This app helps users learn different courses with topics and tracking."
    }

@router.get("/contact")
def contact():
    return {
        "email": "bharathummadi4@gmail.com",
        "phone": "8019704685"
    }
