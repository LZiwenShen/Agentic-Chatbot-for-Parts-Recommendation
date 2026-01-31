
import os
from typing import Annotated, Literal, TypedDict
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

search_tool = TavilySearchResults(max_results=3)


tools = [search_tool]

llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_tools = llm.bind_tools(tools)


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

def agent_node(state: AgentState):
    messages = state["messages"]

    system_prompt = SystemMessage(content="""
            You are an expert parts specialist for PartSelect.com.

            RESPONSE FORMATTING RULES:
            1. **Structured Data**: When listing parts, ALWAYS use a Markdown Table (Part Name, Number, Price, Link).
            2. **Installation Instructions (CRITICAL)**: 
               - When asked how to install/fix, you MUST provide **BOTH** a written summary and a video if available.
               - **Step 1**: Summarize the installation steps in a clear **Numbered List** (e.g., 1. Unplug fridge, 2. Remove screws...).
               - **Step 2**: Provide the video link at the bottom: 📺 **[Watch Installation Video](URL)**.
            3. **Bold Key Info**: Always **bold** model numbers and part numbers.
            4. **Clear Links**: Use [Link Text](URL) format.

            Your Mission:
            1. Remember user context.
            2. Search proactively for "PartNumber installation guide" to find text steps AND videos.
            3. detailed steps are better than vague advice.
        """)

    if isinstance(messages[0], SystemMessage):
        pass
    else:
        messages = [system_prompt] + messages

    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


tool_node = ToolNode(tools)


def should_continue(state: AgentState) -> Literal["tools", END]:
    messages = state["messages"]
    last_message = messages[-1]

    if last_message.tool_calls:
        return "tools"
    return END


workflow = StateGraph(AgentState)

workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
)

workflow.add_edge("tools", "agent")
memory = MemorySaver()
app_graph = workflow.compile(checkpointer=memory)