# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from agent import app_graph
from langchain_core.messages import HumanMessage

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserRequest(BaseModel):
    message: str




@app.post("/chat")
async def chat(req: UserRequest):
    print(f"User Query: {req.message}")

    config = {"configurable": {"thread_id": "demo_user_1"}}

    inputs = {"messages": [HumanMessage(content=req.message)]}

    result = app_graph.invoke(inputs, config=config)

    last_message = result["messages"][-1]
    response_text = last_message.content

    print(f"Agent Reply: {response_text}")

    return {"response": response_text}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)