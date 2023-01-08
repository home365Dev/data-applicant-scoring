import json
import logging
import threading

import watchtower

from fastapi import Request, FastAPI, APIRouter

import src.data_applicant_scoring.db_handler as dbh
from src.data_applicant_scoring.app import execute

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.addHandler(watchtower.CloudWatchLogHandler())

router = APIRouter()

app = FastAPI(
    title="Home365",
    version="0.0.1",
)

@router.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

@app.post("/data_applicant_scoring")
async def data_applicant_scoring(request: Request):
    body = await request.json()
    response = execute(body)
    rsp = json.loads(response)
    thread = threading.Thread(target=dbh.execute_to_db, kwargs={'id': rsp["body"]["id"], 'data': rsp["body"]})
    thread.start()
    return response
    
app.include_router(router, prefix="/data_applicant_scoring")

logger.info("Starting up")
