# graph_agent.py
import asyncio
from typing import AsyncGenerator, List
from google.genai import types
from google.adk.agents import BaseAgent
from google.adk.runners import InvocationContext
from google.adk.events import Event

# --- pretend "tool" (pure python) ---
async def fetch_facts(topic: str) -> List[str]:
    await asyncio.sleep(0.1)  # simulate latency
    return [f"Fact 1 about {topic}", f"Fact 2 about {topic}"]

# --- pretend "writer" sub-step ---
async def draft_answer(facts: List[str]) -> str:
    await asyncio.sleep(0.1)  # simulate latency
    return " • " + "\n • ".join(facts)

class CoordinatorAgent(BaseAgent):
    """A custom agent that orchestrates tool + writer and YIELDS events as it proceeds."""

    def __init__(self, name: str = "coordinator"):
        super().__init__(name=name)

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        # 1) announce start (event 1)
        yield Event(
            author=self.name,
            content=types.Content(
                role="assistant",
                parts=[types.Part.from_text(text="Step 1: Researching…")]
            )
        )

        # 2) "tool call" (event 2) — show tool start
        yield Event(
            author=self.name,
            content=types.Content(
                role="assistant",
                parts=[types.Part.from_text(text="Calling tool: fetch_facts(topic)")]
            )
        )

        # print(dir(ctx))
        # Execute the tool
        topic = ctx.user_content.parts[0].text if ctx.user_content.parts else "topic"
        facts = await fetch_facts(topic)

        # 3) "tool result" (event 3)
        yield Event(
            author=self.name,
            content=types.Content(
                role="assistant",
                parts=[types.Part.from_text(text=f"Tool result: {facts}")]
            )
        )

        # 4) "writer" step (event 4)
        yield Event(
            author=self.name,
            content=types.Content(
                role="assistant",
                parts=[types.Part.from_text(text="Composing final answer…")]
            )
        )

        # Compose final
        final_text = await draft_answer(facts)

        # 5) FINAL response (event 5) — exactly one per turn
        yield Event(
            author=self.name,
            content=types.Content(
                role="assistant",
                parts=[types.Part.from_text(text=f"Final:\n{final_text}")]
            )
        )

# export a root agent for convenience (works with adk web too)
root_agent = CoordinatorAgent()
