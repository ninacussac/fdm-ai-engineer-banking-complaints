from fastapi import FastAPI
from src.data.connection import engine
from src.data.base import Base
from src.api.complaint_routers import router

app = FastAPI(title = "Banking Complaint App")
Base.metadata.create_all(bind=engine)
app.include_router(router)

@app.get("/health")
def health():
    return{"status":"healthy"}