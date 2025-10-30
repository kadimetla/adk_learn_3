# adk_learn_3
google ADK here’s a tiny, runnable demo that shows how the agent graph can yield Events step-by-step (tool step → “writer” step → final), and how Runner.run_async(...) streams those events to your app.

```python

FastAPI / CLI
   │
   ▼
Runner.run_async(...)
   │
   ├─ loads SessionService (previous conversation)
   │
   ├─ builds InvocationContext (state, tools, memory)
   │
   ├─ invokes Agent._run_async_impl(ctx)
   │       └── yields Event 1 (start)
   │       └── yields Event 2 (tool call)
   │       └── yields Event 3 (tool result)
   │       └── yields Event 4 (final response)
   │
   ├─ for each Event:
   │     → streamed out to client (SSE/WebSocket)
   │     → logged/traced
   │
   └─ after final Event:
         → persist turn into SessionService
         → emit completion signal

