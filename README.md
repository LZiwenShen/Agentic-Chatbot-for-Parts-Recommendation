# PartSelect Intelligent Assistant

A full-stack agentic chatbot designed to assist PartSelect customers with refrigerator and dishwasher parts. Built with **LangGraph** (Stateful Agent), **FastAPI** (Backend), and **React** (Frontend).

## Quick Start

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
# Ensure your .env file has OPENAI_API_KEY and TAVILY_API_KEY
python main.py
```
Server will start at http://localhost:8000

### 2. Frontend Setup
```bash
cd frontend
npm install  # <--- CRITICAL: Restores dependencies
npm start
```
App will open at http://localhost:3000

### Architecture & Features
Agentic Framework (LangGraph): Implements a ReAct (Reason + Act) pattern with persistent memory.

MemorySaver: Maintains conversation context (e.g., remembering "Ice Maker" issues when later provided with a "Model Number").

Looping Logic: Think -> Search -> Observe -> Answer.

Search Integration: Uses Tavily API to fetch real-time compatibility data and installation videos.

Frontend: Custom React interface with Markdown rendering for structured tables and deep links.

### Design Decisions
Reliability over Images: The agent prioritizes structured Markdown tables and direct product links over embedding web-scraped images. This decision ensures 100% link validity and prevents "broken image" UX issues common with general search tools.

Anti-Hallucination: Strict system prompts are implemented to verify Part Name vs. Part ID (e.g., distinguishing Door Bins from Water Filters).

Extensibility: The backend graph is modular; adding a "Order Status" tool or "Human Handoff" node would only require adding a new node to the StateGraph.

### Project Structure
/backend: FastAPI server, Agent logic (agent.py), Entry point (main.py).

/frontend: React application, API integration (src/api).
