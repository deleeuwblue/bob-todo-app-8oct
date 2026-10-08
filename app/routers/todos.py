from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Todo
from app.schemas import TodoCreate, TodoResponse, TodoUpdate

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("", response_model=list[TodoResponse])
def list_todos(db: Session = Depends(get_db)):
    """Retrieve all todo items.

    Args:
        db: Database session injected by FastAPI dependency.

    Returns:
        List of TodoResponse objects representing all todos.

    Response Shape:
        List of objects containing id (int), title (str), completed (bool), and due_date (date or null).
    """
    return db.query(Todo).all()


@router.post("", response_model=TodoResponse, status_code=201)
def create_todo(payload: TodoCreate, db: Session = Depends(get_db)):
    """Create a new todo item with an optional completion due date.

    Args:
        payload: TodoCreate object containing title and optional due_date.
        db: Database session injected by FastAPI dependency.

    Returns:
        The newly created Todo item.

    Request Body:
        title (str, required), due_date (date string YYYY-MM-DD, optional).

    Response Shape:
        TodoResponse containing id, title, completed, and due_date.
    """
    todo = Todo(title=payload.title, due_date=payload.due_date)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.patch("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, payload: TodoUpdate, db: Session = Depends(get_db)):
    """Update completion status or due date of an existing todo.

    Args:
        todo_id: Integer primary key identifier of the todo to update.
        payload: TodoUpdate object containing fields to modify.
        db: Database session injected by FastAPI dependency.

    Returns:
        The updated Todo item.

    Raises:
        HTTPException: 404 if the todo with the given id does not exist.

    Request Body:
        completed (bool, optional), due_date (date, optional).

    Response Shape:
        TodoResponse containing id, title, completed, and due_date.
    """
    todo = db.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Not found")
    if payload.completed is not None:
        todo.completed = payload.completed
    if payload.due_date is not None:
        todo.due_date = payload.due_date
    db.commit()
    db.refresh(todo)
    return todo


@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete a todo item by ID.

    Args:
        todo_id: Integer primary key identifier of the todo to remove.
        db: Database session injected by FastAPI dependency.

    Returns:
        Response with status code 204.

    Raises:
        HTTPException: 404 if the todo with the given id does not exist.

    Response Shape:
        Empty response body with HTTP 204 status.
    """
    todo = db.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(todo)
    db.commit()
    return Response(status_code=204)
