"""schema for mysql"""
from pydantic import BaseModel, Field
from typing import Optional


class InsertionDBError(Exception):
    """Cannnot insert data into mysql"""

class Record(BaseModel):
    """record data"""

    id: int = Field(..., description="id")
    name: str = Field(..., description="name")
    category_id: int = Field(..., description="category id")
    subcategory_id: Optional[int] = Field(None, description="subcategory id")
    amount: int = Field(..., description="amount")
    description: str = Field(..., description="description")
    is_spending: bool = Field(..., description="is_spending")
    repeat_frequency: Optional[str] = Field(
        None, description="frequency of repeated record in {daily, weekly, monthly, None}"
    )
    date: str = Field(..., description="date")
    is_deleted: bool = Field(..., description="is_deleted")
