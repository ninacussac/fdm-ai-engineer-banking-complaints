from fastapi import FastAPI

from src.config import settings

from src.api.complaint_router import router as complaint_router
from src.api.customer_router import router as customer_router
from src.api.account_router import router as account_router
from src.api.complaint_status_event_router import router as complaint_status_event_router
from src.api.routers.health import router as health_router

app = FastAPI(title = settings.APP_NAME)

app.include_router(complaint_router)
app.include_router(customer_router)
app.include_router(account_router)
app.include_router(complaint_status_event_router)
app.include_router(health_router)

@app.get("/health")
def health():
    return{"status":"healthy"}