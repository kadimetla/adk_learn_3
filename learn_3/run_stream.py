# run_stream.py
import asyncio
from google.genai import types
from google.adk.runners import InMemoryRunner
from graph_agent import root_agent

APP = "graph_demo"
runner = InMemoryRunner(agent=root_agent, app_name=APP)

async def main():
    user_id, session_id = "u1", "s1"
    # ensure the session exists
    sess = await runner.session_service.get_session(app_name=APP, user_id=user_id, session_id=session_id)
    if not sess:
        await runner.session_service.create_session(app_name=APP, user_id=user_id, session_id=session_id)

    msg = types.Content(role="user", parts=[types.Part.from_text(text="Houston travel")])

    print("Streaming events:")
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=msg,
    ):
        # print every event as it streams
        text = "".join(getattr(p, "text", "") for p in event.content.parts) if event.content else ""
        marker = " (FINAL)" if event.is_final_response() else ""
        print(f"- {text}{marker}")

if __name__ == "__main__":
    asyncio.run(main())
