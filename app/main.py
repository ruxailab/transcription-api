from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

# Schemas
from fastapi.responses import JSONResponse
from app.schemas.common import ErrorResponse

# Routes
from app.api.v1 import health
from app.api.v1 import transcribe


from dotenv import load_dotenv

load_dotenv()  # <-- This loads the environment variables from .env file

# Initialize FastAPI application
app = FastAPI(
    title="Transcription Backend",
    description="API for audio transcription and health monitoring",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # or ["*"] for all origins during dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    print(f"[Validation Error] Path: {request.url.path} | Errors: {exc.errors()}")

    # Build user-friendly field-level messages
    field_errors = []
    for err in exc.errors():
        field = " -> ".join(str(loc) for loc in err["loc"])
        msg = err["msg"]
        field_errors.append(f"{field}: {msg}")

    # Customize the top-level message
    summary_message = "Some required fields are missing or invalid."

    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            status="error",
            message=summary_message,
            details="; ".join(field_errors),
        ).model_dump(),
    )


# Exception handler for 500 Internal Server Error
@app.exception_handler(Exception)
async def internal_error_handler(request: Request, exc: Exception):
    # Optional: log the full traceback for debugging
    print(f"[Internal Error] Path: {request.url.path} | Exception: {exc}")

    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            status="error",
            message="Something went wrong on our side. Please try again later.",
        ).model_dump(),
    )


app.include_router(health.router, prefix="/api/v1")
app.include_router(transcribe.router, prefix="/api/v1")


# Example of how to access settings in the app
# from app.core.config import settings  # or from config import settings if in same file
# print("OPENAI_API_KEY =", settings.openai_api_key)
