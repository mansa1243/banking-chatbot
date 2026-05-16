from fastapi import APIRouter
from backend.schemas import ChatRequest
from utils.intent_router import route_intent

router = APIRouter()


@router.post("/chat")
async def chat(request: ChatRequest):

    try:
        result = route_intent(request.message)

        return {
            "status": "success",
            "response": result
        }

    except Exception as e:

        return {
            "status": "error",
            "response": "❌ Something went wrong in backend",
            "details": str(e)
        }