from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from models.nlp import IntentParser

router = APIRouter()
parser = IntentParser()  # Load spaCy model

class NLPRequest(BaseModel):
    query: str

@router.post("/parse")
def parse_user_query(request: NLPRequest):
    query = request.query.strip()

    if not query:
        raise HTTPException(status_code=400, detail="Query is empty")

    intent, entities = parser.parse(query)

    return {
        "query": query,
        "intent": intent,
        "entities": entities
    }
