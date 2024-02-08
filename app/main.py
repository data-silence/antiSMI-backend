from fastapi import FastAPI
from app.news.router import router as router_news
from app.agencies.router import router as router_agencies

app = FastAPI()

app.include_router(router_news)
app.include_router(router_agencies)


# @app.get("/")
# async def root():
#     return {"message": "These are some test endpoints for a secret project"}
