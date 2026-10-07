from datetime import date

from pydantic import BaseModel, ConfigDict


class TodoCreate(BaseModel):
    """Schema for creating a new todo item.

    Attributes:
        title: The text of the todo task.
        due_date: Optional date by which the task should be completed.
    """

    title: str
    due_date: date | None = None


class TodoUpdate(BaseModel):
    """Schema for updating an existing todo item.

    Attributes:
        completed: The new completion state for the todo.
    """

    completed: bool


class TodoResponse(BaseModel):
    """Schema for todo item responses returned by the API.

    Attributes:
        id: Unique identifier of the todo.
        title: The text of the todo task.
        completed: Whether the task has been completed.
        due_date: Optional date by which the task should be completed.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    completed: bool
    due_date: date | None = None
