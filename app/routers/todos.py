from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Todo
from app.schemas import TodoCreate, TodoResponse, TodoUpdate

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("", response_model=list[TodoResponse])
def list_todos(db: Session = Depends(get_db)) -> list[Todo]:
    """Retrieve all todo items.

    Args:
        db: Database session dependency.

    Returns:
        List of all Todo items.
    """
    return db.query(Todo).all()


@router.post("", response_model=TodoResponse, status_code=201)
def create_todo(payload: TodoCreate, db: Session = Depends(get_db)) -> Todo:
    """Create a new todo item.

    Args:
        payload: Todo creation payload containing title and optional due_date.
        db: Database session dependency.

    Returns:
        The newly created Todo item.
    """
    todo = Todo(title=payload.title, due_date=payload.due_date)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.patch("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, payload: TodoUpdate, db: Session = Depends(get_db)) -> Todo:
    """Update an existing todo item's status or details.

    Args:
        todo_id: Integer identifier of the todo item.
        payload: Update payload containing optional completion state or due_date.
        db: Database session dependency.

    Returns:
        The updated Todo item.

    Raises:
        HTTPException: 404 if the todo item does not exist.
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
def delete_todo(todo_id: int, db: Session = Depends(get_db)) -> Response:
    """Delete a todo item by ID.

    Args:
        todo_id: Integer identifier of the todo item to delete.
        db: Database session dependency.

    Returns:
        Empty 204 No Content response.

    Raises:
        HTTPException: 404 if the todo item does not exist.
    """
    todo = db.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(todo)
    db.commit()
    return Response(status_code=204)
