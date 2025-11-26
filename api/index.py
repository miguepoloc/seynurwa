"""FastAPI application for Vercel serverless deployment."""

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.infrastructure.api.routes import router as auth_router
from emotions.infrastructure.api.routes import router as emotions_router

# Create FastAPI app
app = FastAPI(
    title="Simple Auth API",
    description="User authentication with registration and login",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(emotions_router, prefix="/api/emotions", tags=["emotions"])
@app.get("/")
async def root():
    """Root endpoint."""
    return {"status": "ok", "message": "Auth API is running"}

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
