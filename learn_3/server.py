# server.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from google.genai import types
from google.adk.runners import InMemoryRunner
from graph_agent import root_agent


app = FastAPI(title="ADK event-stream sample")
APP = "graph_demo"
runner = InMemoryRunner(agent=root_agent, app_name=APP)

class ChatReq(BaseModel):
    user_id: str
    session_id: str
    message: str

@app.post("/chat/stream")
async def chat_stream(req: ChatReq):
    # ensure session exists
    sess = await runner.session_service.get_session(app_name=APP, user_id=req.user_id, session_id=req.session_id)
    if not sess:
        await runner.session_service.create_session(app_name=APP, user_id=req.user_id, session_id=req.session_id)

    msg = types.Content(role="user", parts=[types.Part.from_text(text=req.message)])

    async def gen():
        async for event in runner.run_async(
            user_id=req.user_id,
            session_id=req.session_id,
            new_message=msg,
        ):
            text = "".join(getattr(p, "text", "") for p in (event.content.parts if event.content else []))
            # Stream every event line-by-line; the client can show a live transcript
            yield f"data: {text}\n\n".encode()

    return StreamingResponse(gen(), media_type="text/event-stream")
