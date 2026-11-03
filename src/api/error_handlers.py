from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# AppError permet de représenter une erreur, mais ne définit pas encore à lui seul le JSON retourné au client :
class AppError(HTTPException):
    def __init__(self, code: str, message: str, status_code: int):
        super().__init__(status_code=status_code, detail=message)
        self.code = code

#gestionnaire d'exception : transforme objet AppError en reponse HTTP
def app_error_handler(request: Request, exception: AppError):
    return JSONResponse(
        status_code=exception.status_code,
        content={"code": exception.code,
                "message": exception.detail,
                "correlation_id": getattr(request.state, "correlation_id", None)}
    )

def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "code": "VALIDATION_ERROR",
            "message": "Invalid request data",
            "correlation_id": getattr(request.state, "correlation_id", None)
        }
    )