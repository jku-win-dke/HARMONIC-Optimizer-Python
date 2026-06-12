from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse

from app.logger.logger_config import logger
from .routers import optimizations


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager to log the application's lifespan.
    """
    logger.info('Application started successfully.')
    yield
    logger.info('Application shutting down.')


# Create a FastAPI instance
app = FastAPI(
    title='HARMONIC-Optimizer',
    description='API for the HARMONIC-Optimizer',
    version='0.0.1',
    lifespan=lifespan
)


# Include the routers for the different endpoints
app.include_router(optimizations.router, tags=['optimization-endpoint'])


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handles and logs validation errors that occur during request processing.
    """
    logger.error(f'Validation error occurred for request: {request.url}. - Error: {exc}')
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.get(path='/', include_in_schema=False)
def root() -> RedirectResponse:
    """
    Redirects the user to the API documentation when starting the application.
    """
    return RedirectResponse(url='/docs')
