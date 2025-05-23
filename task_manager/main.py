import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
import os

from app.database import engine, Base
from .routers import auth, users, tasks
from app.middleware import setup_middleware

# Load environment variables
load_dotenv()

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Attach middleware
setup_middleware(app)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/")
async def read_root():
    return {"message": "API is working!!"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("RELOAD", "True").lower() == "true",
        ssl_certfile=os.getenv("SSL_CERTFILE", None),
        ssl_keyfile=os.getenv("SSL_KEYFILE", None),
    )