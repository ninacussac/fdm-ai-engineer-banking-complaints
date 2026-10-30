from fastapi import FastAPI

from src.config import settings

from src.api.complaint_router import router as complaint_router
from src.api.customer_router import router as customer_router
from src.api.account_router import router as account_router
from src.api.complaint_status_event_router import router as complaint_status_event_router
from src.api.routers.health import router as health_router
from src.data.connection import engine
from src.data.base import Base
from src.models import models

# creer les tables
Base.metadata.create_all(bind=engine)

#run the app
app = FastAPI(title = settings.APP_NAME)

#include the routers
app.include_router(complaint_router)
app.include_router(customer_router)
app.include_router(account_router)
app.include_router(complaint_status_event_router)
app.include_router(health_router)

# create tables with metadada, Base.Metadata

@app.get("/health")
def health():
    return{"status":"healthy"}