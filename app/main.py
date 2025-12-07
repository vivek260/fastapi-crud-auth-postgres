from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from app.core.errors import AppError
from fastapi import Request
from fastapi.responses import JSONResponse

app = FastAPI(title="FastAPI CRUD Auth")

# Sending Custom Error in place of ValueError
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail["error"]}
    )


app.include_router(auth_router, prefix="/auth")
