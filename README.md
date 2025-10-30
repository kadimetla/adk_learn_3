# adk_learn_3
google ADK here’s a tiny, runnable demo that shows how the agent graph can yield Events step-by-step (tool step → “writer” step → final), and how Runner.run_async(...) streams those events to your app.


```mermaid
graph TD
    A[FastAPI / CLI]
    A --> B(Runner.run_async(...))
    B --> C[loads SessionService (previous conversation)]
    B --> D[builds InvocationContext (state, tools, memory)]
    B --> E[invokes Agent._run_async_impl(ctx)]
    E --> E1[Event 1 (start)]
    E --> E2[Event 2 (tool call)]
    E --> E3[Event 3 (tool result)]
    E --> E4[Event 4 (final response)]
    B --> F[for each Event]
    F --> F1[streamed out to client (SSE/WebSocket)]
    F --> F2[logged/traced]
    B --> G[after final Event]
    G --> G1[persist turn into SessionService]
    G --> G2[emit completion signal]

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

