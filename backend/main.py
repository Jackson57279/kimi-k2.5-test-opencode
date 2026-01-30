"""
Railway PaaS Clone - FastAPI Application Entry Point
"""

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.config import settings
from backend.database import init_db, close_db
from backend.api import auth_router
from backend.middleware.exception_handlers import add_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


# Create FastAPI application
app = FastAPI(
    title="Railway PaaS Clone API",
    description="A full-stack PaaS platform inspired by Railway.app",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handlers
add_exception_handlers(app)


# Health check endpoint
@app.get("/", tags=["health"])
async def root():
    """Root endpoint - API information"""
    return {
        "message": "Welcome to Railway PaaS Clone API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "environment": settings.environment,
    }


@app.get("/hello", tags=["health"])
async def hello():
    """Hello world endpoint"""
    return {"message": "Hello, World!"}


@app.get("/version", tags=["health"])
async def version():
    """Version information"""
    import fastapi
    import sqlalchemy

    return {
        "api_version": "0.1.0",
        "fastapi_version": fastapi.__version__,
        "sqlalchemy_version": sqlalchemy.__version__,
    }


# Include API routers
app.include_router(auth_router, prefix="/auth", tags=["authentication"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "development",
    )
