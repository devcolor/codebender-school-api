from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import al, csusb, kctcs, ky, oh, upload
from db_operations.connection import test_all_connections

app = FastAPI(
    title="DevColor Backend API",
    description="Unified API for accessing 5 educational institution databases",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with clear prefixes and tags
app.include_router(
    al.router, 
    prefix="/al", 
    tags=["AL - Bishop State Community College"]
)
app.include_router(
    csusb.router, 
    prefix="/csusb", 
    tags=["CSUSB - California State University San Bernardino"]
)
app.include_router(
    kctcs.router, 
    prefix="/kctcs", 
    tags=["KCTCS - Kentucky Community and Technical College System"]
)
app.include_router(
    ky.router, 
    prefix="/ky", 
    tags=["KY - Thomas More University"]
)
app.include_router(
    oh.router, 
    prefix="/oh", 
    tags=["OH - University of Akron"]
)
app.include_router(
    upload.router,
    prefix="/upload",
    tags=["Data Upload"]
)

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "DevColor Backend API",
        "version": "1.0.0",
        "available_databases": ["AL", "CSUSB", "KCTCS", "KY", "OH"],
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "endpoints": {
            "health": "/health",
            "upload": "/upload/",
            "databases": {
                "AL": "/al/",
                "CSUSB": "/csusb/", 
                "KCTCS": "/kctcs/",
                "KY": "/ky/",
                "OH": "/oh/"
            }
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for all databases."""
    return await test_all_connections()

