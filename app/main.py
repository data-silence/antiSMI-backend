from fastapi import FastAPI
from app.news.router_main import router as router_news
from app.news.router_graphs import router as router_graphs
from app.agencies.router import router as router_agencies

app = FastAPI(title='AntiSMI backend')

app.include_router(router_news)
app.include_router(router_graphs)
app.include_router(router_agencies)


@app.get("/")
async def root():
    return {"message": "These are some test endpoints for some projects"}
