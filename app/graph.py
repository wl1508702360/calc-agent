from langchain_community.tools import human
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph,START,END
from langgraph.prebuilt import ToolNode

from app.node import call_llm,should_continue
from app.state import CalculateState
from app.tools import add,subtract,multiply,divide

tools = [add,subtract,multiply,divide]
tool_node = ToolNode(tools)


# def call_llm(state: CalculateState):
#     """调用大模型"""
#     mode = os.environ.get("MODEL_MODE")
#     messages = state['messages']
#     response = LLM(mode=mode).get_model().bind_tools(tools).invoke(messages)
#     return {"messages": [response]}

graph = StateGraph(CalculateState)

graph.add_node("agent", call_llm)
graph.add_node("tools", tool_node)

graph.add_edge(START,"agent")
graph.add_conditional_edges("agent", should_continue, ["tools", END])
graph.add_edge("tools","agent")

app = graph.compile()

def get_result(input: str):
    prompt = """你是一位数学计算助手
    规则：
    1、非数学问题不在职责范围内
    2、数学计算必须调用本地工具
    3、获得工具结果后输出最终答案
    """.strip()

    messages = {
        "messages": [
            SystemMessage(content=prompt),
            HumanMessage(content=input),
        ]
    }

    config = {
        "configurable": {
            "thread_id": "1"
        }
    }

    chunks = app.stream(messages, config=config, stream_mode="messages")
    for chunk,meta in chunks:
        if chunk.content:
            print(chunk.content,end="|", flush=True)

