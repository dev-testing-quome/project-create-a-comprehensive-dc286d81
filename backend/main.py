import uvicorn
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

from database import engine, Base
from routers import users, permits, taxes # Add other routers here

app = FastAPI(title="Citizen Services Portal", version="1.0.0", openapi_url="/openapi.json", docs_url="/docs")

# CORS Configuration
origins = ["*"]  # Update with your allowed origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Database Initialization
Base.metadata.create_all(bind=engine)

# Router Registration
app.include_router(users.router)
app.include_router(permits.router)
app.include_router(taxes.router) # Add other routers here

# Health Check
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Static File Serving
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

    @app.get("/{file_path:path}")
    async def serve_frontend(file_path: str):
        if file_path.startswith("api"):
            return None
        static_file = os.path.join("static", file_path)
        if os.path.isfile(static_file):
            return FileResponse(static_file)
        return FileResponse("static/index.html")

# Exception Handling
@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

# Start the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
