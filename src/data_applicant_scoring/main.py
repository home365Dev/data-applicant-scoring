import json
import logging
import threading

import watchtower

from fastapi import Request, FastAPI, APIRouter

import src.data_applicant_scoring.db_handler as dbh
from src.data_applicant_scoring.app import execute

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
# logger.addHandler(watchtower.CloudWatchLogHandler())

router = APIRouter()

app = FastAPI(
    title="Home365",
    version="0.0.1",
)

@router.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

@router.post("/data_applicant_scoring")
async def data_applicant_scoring(request: Request):
    body = await request.json()
    response = execute(body)
    rsp = json.loads(response)
    thread = threading.Thread(target=dbh.execute_to_db, kwargs={'id': rsp["body"]["id"], 'data': rsp["body"]})
    thread.start()
    return response
    
app.include_router(router, prefix="/data-applicant-scoring")

logger.info("Starting up")

if __name__ == '__main__':
    jst = {"applicant_id": 'BC5T2A09-ELE2-4HG0-AE74-4E2DF78A3E1D',
            "credit_score": 678,
            "eviction": 2,
            "criminal": 1,
            "age": 28
    }
    body_json = json.dumps(jst)

    response, json_vendors, state = execute(jst)
    thread = threading.Thread(target=dbh.execute_to_db, kwargs={
        'jsono': response, 'jsoni': jst, 'output_vendors': json_vendors, 'state': state})
    thread.start()

    noam = "noam"