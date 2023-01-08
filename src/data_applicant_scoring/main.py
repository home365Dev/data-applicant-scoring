import logging
import watchtower

from fastapi import Request, FastAPI, APIRouter


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

@app.post("/data-applicant-scoring")
async def data_applicant_scoring(request: Request):
    body = await request.json()
    return execute(body)
    
app.include_router(router, prefix="/data-applicant-scoring")

logger.info("Starting up")
