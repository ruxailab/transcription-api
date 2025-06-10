from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    # status: str = Field(..., example="ok")
    status: str = Field(..., json_schema_extra={"example": "ok"})  # ✅ correct
    message: str = Field(..., json_schema_extra={"example": "Service is running"})
