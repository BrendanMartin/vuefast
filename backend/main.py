import uuid
from datetime import datetime
from enum import StrEnum

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from pydantic import BaseModel

app = FastAPI(
        title="vuefast-backend",
        servers=[{"url": "http://localhost:8000"}]
)

app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)


class Priority(StrEnum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


class Todo(BaseModel):
    id: str
    title: str
    created: int
    priority: Priority | None = None
    completed: bool = False


class CreateTodoRequest(BaseModel):
    title: str
    priority: Priority | None = None


todos: dict[str, Todo] = {}

todos.update({
    '1': Todo(id='1', title='this is a todo from FastAPI', created=1, priority=Priority.LOW, completed=False),
    '2': Todo(id='2', title='this is another one 😄', created=2, priority=Priority.MEDIUM, completed=False)
})

@app.post('/todos', status_code=201)
async def create_todo(req: CreateTodoRequest) -> Todo:
    new_id = str(uuid.uuid4())
    created = int(datetime.timestamp(datetime.now()))
    new_todo = Todo(id=new_id, created=created, **req.dict())
    todos[new_id] = new_todo
    return new_todo


@app.get('/todos')
async def list_todos() -> list[Todo]:
    return [t for t in todos.values() if not t.completed]


@app.put('/todos/{todo_id}/complete')
async def complete_todo(todo_id: str) -> Todo:
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail='Todo not found')

    todos[todo_id].completed = True
    return todos[todo_id]


def setup_openapi(app: FastAPI) -> None:
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


setup_openapi(app)
