from app.llm import LLM
from app.state import CalculateState
from langgraph.graph import StateGraph,START,END

import os
from dotenv import load_dotenv
load_dotenv(verbose=True)

from app.tools import add,subtract,multiply,divide

tools = [add,subtract,multiply,divide]
def call_llm(state: CalculateState):
    """调用大模型"""
    mode = os.environ.get("MODEL_MODE")
    messages = state['messages']
    response = LLM(mode=mode).get_model().bind_tools(tools).invoke(messages)
    return {"messages": [response]}


def should_continue(state: CalculateState):
    last_message = state["messages"][-1]
    tool_calls = getattr(last_message,"tool_calls",[])
    print("====tool_calls:", tool_calls)
    if tool_calls:
        return "tools"
    else:
        return END

