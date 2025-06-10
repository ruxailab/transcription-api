from pydantic import BaseModel, Field
from typing import Optional


class ErrorResponse(BaseModel):
    status: str = Field(..., example="error")
    message: str = Field(..., example="Something went wrong")
    details: Optional[str] = Field(
        None, example="Detailed error message or validation issues"
    )
