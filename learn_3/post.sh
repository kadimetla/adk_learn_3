curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "session_id": "abc", "message": "Hello"}'
