from pydantic import BaseModel, Field
from typing import Optional


class ErrorResponse(BaseModel):
    status: str = Field(..., json_schema_extra={"example": "error"})
    message: str = Field(..., json_schema_extra={"example": "Something went wrong"})
    details: Optional[str] = Field(
        None, json_schema_extra={"Detailed error message or validation issues"}
    )
