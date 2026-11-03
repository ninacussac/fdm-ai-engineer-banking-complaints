from fastapi import FastAPI
from src.data.connection import engine
from src.data.base import Base
from src.api.complaint_router import router as complaint_router
from src.api.customer_router import router as customer_router
from src.api.account_router import router as account_router
from src.api.complaint_status_event_router import router as complaint_status_event_router

app = FastAPI(title = "Banking Complaint App")
Base.metadata.create_all(bind=engine)
app.include_router(complaint_router)
app.include_router(customer_router)
app.include_router(account_router)
app.include_router(complaint_status_event_router)

@app.get("/health")
def health():
    return{"status":"healthy"}