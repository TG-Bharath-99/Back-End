from fastapi import FastAPI
import models
from database import engine
from routers import blog, user


models.Base.metadata.create_all(engine)

app=FastAPI()

app.include_router(blog.router, prefix="/blog", tags=["blog"])
app.include_router(user.router, prefix="/user", tags=["user"])


@app.get("/")
def home():
    return {"Msg":"Everything is Fine , chill bro"}