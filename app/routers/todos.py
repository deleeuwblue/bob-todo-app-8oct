from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Todo
from app.schemas import TodoCreate, TodoResponse, TodoUpdate

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("", response_model=list[TodoResponse])
def list_todos(db: Session = Depends(get_db)):
    """Return all todo items.

    Args:
        db: Database session injected by FastAPI's dependency system.

    Returns:
        List of TodoResponse objects.
    """
    return db.query(Todo).all()


@router.post("", response_model=TodoResponse, status_code=201)
def create_todo(payload: TodoCreate, db: Session = Depends(get_db)):
    """Create a new todo item.

    Args:
        payload: TodoCreate with title and optional due_date.
        db: Database session injected by FastAPI's dependency system.

    Returns:
        The newly created TodoResponse.
    """
    todo = Todo(title=payload.title, due_date=payload.due_date)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.patch("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, payload: TodoUpdate, db: Session = Depends(get_db)):
    """Toggle the completed state of a todo item.

    Args:
        todo_id: Path parameter identifying the todo.
        payload: TodoUpdate with the new completed value.
        db: Database session injected by FastAPI's dependency system.

    Returns:
        The updated TodoResponse.

    Raises:
        HTTPException: 404 if the todo does not exist.
    """
    todo = db.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Not found")
    todo.completed = payload.completed
    db.commit()
    db.refresh(todo)
    return todo


@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete a todo item by id.

    Args:
        todo_id: Path parameter identifying the todo to delete.
        db: Database session injected by FastAPI's dependency system.

    Raises:
        HTTPException: 404 if the todo does not exist.
    """
    todo = db.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(todo)
    db.commit()
    return Response(status_code=204)
