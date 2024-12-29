from fastapi import FastAPI
from module_17_1.app.routers import user
from module_17_1.app.routers import task

app = FastAPI()


@app.get('/')
async def welcome() -> dict:
    return {'message': 'Welcome to Taskmanager'}

app.include_router(task.router)
app.include_router(user.router)
