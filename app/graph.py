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
    prompt = """你是一位数学专家，可以根据客户的需求计算相对应的数的处理，如果不是数学问题，请给出不在职责范围内的回答,你的回答需要调用本地的tools工具"""
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
    # full_text = ""
    # full_reason = ""
    for chunk,meta in chunks:
        # print(chunk, end="|", flush=True)
        if chunk.content:
            print(chunk.content,end="|", flush=True)
        # messages = chunk["messages"]
        # msg = messages[-1]
        #
        # # 情况1：AI发起工具调用，content为空，跳过文本拼接
        # if hasattr(msg, "tool_calls") and msg.tool_calls:
        #     print("检测到工具调用，等待执行工具...")
        #     continue
        #
        # # 情况2：正常回答消息，拼接内容
        # if msg.content:
        #     full_text += msg.content
        #     # 提取思考过程
        #     think = msg.additional_kwargs.get("reasoning_content", "")
        #     full_reason += think

        # print("完整思考：", full_reason)
        # print("最终回答：", full_text)

