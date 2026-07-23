import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatTongyi
from langchain_deepseek import ChatDeepSeek
load_dotenv()

class LLM:
    def __init__(self, mode:str = 'qwen'):
        self.model_mode = mode

    def get_model(self):
        if self.model_mode == "qwen":
            llm = self.qwen_llm()
        else:
            llm = self.deepseek_model()
        return llm

    def deepseek_model(self):
        deepseek_model = ChatDeepSeek(
            model=os.environ.get("DEEPSEEK_MODEL"),
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        return deepseek_model

    def qwen_llm(self):
        return ChatTongyi(
            model=os.environ.get("DASHSCOPE_MODEL"),
            api_key=os.environ.get("DASHSCOPE_API_KEY"),
            max_retries=2,
        )

