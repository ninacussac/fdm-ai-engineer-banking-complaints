from fastapi import FastAPI, Request
import time 
from uuid import uuid4, UUID


from src.config import settings
from src.api.complaint_router import router as complaint_router
from src.api.customer_router import router as customer_router
from src.api.account_router import router as account_router
from src.api.complaint_status_event_router import router as complaint_status_event_router
from src.api.routers.health import router as health_router
from src.data.connection import engine
from src.data.base import Base
from src.models import models
from src.api.error_handlers import AppError, app_error_handler, validation_error_handler
from fastapi.exceptions import RequestValidationError
from src.logging_config import log_request
from contextlib import asynccontextmanager




@asynccontextmanager
async def lifespan(app: FastAPI):
    if not app.state.testing:
        #creates the table
        Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
app.state.testing = False

#create middleware :
@app.middleware("http")
async def log_requests(request:Request, call_next):
    start_time = time.perf_counter()
    incoming_id = request.headers.get("X-Correlation-ID")
    if incoming_id:
        try:
            correlation_id=str(UUID(incoming_id))
        except ValueError:
            correlation_id=str(uuid4())
    else:
        correlation_id = str(uuid4())
    request.state.correlation_id = correlation_id

    response=await call_next(request)

    duration_ms = (time.perf_counter()-start_time)*1000
    outcome = "success" if response.status_code<400 else "error"

    route = request.scope.get("route")
    if route is not None:
        operation=f"{request.method} {route.path}"
    else:
        operation = f"{request.method} unknown"

    log_request(correlation_id=correlation_id, 
                operation=operation,
                outcome=outcome,
                duration_ms=duration_ms)
    response.headers["X-Correlation-ID"] = correlation_id

    return response
#Quand exception AppError, utilise app+error_handler pour construire la reponse 
app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)

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