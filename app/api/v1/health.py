from fastapi import APIRouter, status

# Schemas
from app.schemas.common import ErrorResponse
from app.schemas.health import HealthResponse

router = APIRouter()


@router.get(
    "/health",
    tags=["Health"],  # ✅ Shows "Health" section in Swagger UI
    status_code=status.HTTP_200_OK,  # ✅ Explicit 200 code (optional, but clear)
    response_model=HealthResponse,  # ✅ Runtime validation + docs + schema
    responses={
        200: {
            "model": HealthResponse,
            "description": "Service is running",
            "content": {
                "application/json": {
                    "example": {
                        "status": "ok",
                        "message": "Service is running",
                    }
                }
            },
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Something went wrong on our side. Please try again later.",
                    }
                }
            },
        },
    },
)
def read_health():
    """
    Health check endpoint to verify if the service is running.
    Returns a simple JSON response indicating the service status.
    """
    return HealthResponse(status="ok", message="Service is running")
