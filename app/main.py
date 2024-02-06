from fastapi import FastAPI
from app.news.router import router as router_news

app = FastAPI()

app.include_router(router_news)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
