import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger("banking_api") # cree ou recupere un logger appele banking_api
logger.setLevel(logging.INFO)# enregistre les messages de niveaux INFO et superieur

if not logger.handlers:
    handler = logging.StreamHandler()#permet d'afficher les logs dans le terminal
    logger.addHandler(handler)

def log_request(correlation_id, operation, outcome, duration_ms):

    level="INFO" if outcome == "success" else "ERROR"
    log_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "correlation_id": correlation_id,
        "operation": operation,
        "outcome": outcome,
        "duration_ms": round(duration_ms, 2)
    }
    if outcome=="success":
        logger.info(json.dumps(log_data))#transforme dictionnaire python en chaine JSON qui est ensuite envoye au logger
    else:
        logger.error(json.dumps(log_data))
