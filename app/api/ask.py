from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.schemas import AskRequest, AskResponse
from app.services.ransomware_service import get_recent_victims
from app.services.groq_service import ask_llm, ask_llm_stream
import json

router = APIRouter(prefix="/ask", tags=["ask"])

@router.post("", response_model=AskResponse, responses={
    200: {"description": "Streaming SSE", "content": {"text/event-stream": {}}}
})
async def ask(req: AskRequest):
    victims = await get_recent_victims(req.limit)
    context = json.dumps(victims, ensure_ascii=False, separators=(",", ":"))[:4000]

    if req.stream:
        headers = {"Cache-Control": "no-cache", "Connection": "keep-alive"}
        return StreamingResponse(
            ask_llm_stream(context, req.query),
            media_type="text/event-stream",
            headers=headers
        )

    answer = await ask_llm(context, req.query)
    return AskResponse(answer=answer, model=settings.model_id)