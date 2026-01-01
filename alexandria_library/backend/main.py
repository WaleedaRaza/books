"""
Alexandria Library Backend API
FastAPI server for the Alexandria Library application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="Alexandria Library API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Alexandria Library API", "status": "running"}


@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/api/books")
async def get_books():
    """Get all books"""
    # TODO: Implement book retrieval from database
    return {"books": [], "count": 0}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)







