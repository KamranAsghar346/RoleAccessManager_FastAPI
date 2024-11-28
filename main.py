# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import models
from api.endpoints import auth, inventory

# Automatically create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Inventory Management System", version="1.0.0")

# CORS configuration (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific domains for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, tags=["Authentication"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])

# Root endpoint
@app.get("/", tags=["Root"])
async def read_root():
    """
    Welcome endpoint to confirm API is running.
    """
    return {"message": "Welcome to the Inventory Management System API!"}
