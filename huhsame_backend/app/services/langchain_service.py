from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableSequence
from langchain_core.messages import HumanMessage, AIMessage
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()


class LangChainService:
    def __init__(self):
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        # OpenAI 모델 설정
        self.llm = ChatOpenAI(temperature=0.7, openai_api_key=openai_api_key)

        # 대화 프롬프트 템플릿 설정
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a friendly AI assistant. Provide detailed responses and remember the context of the conversation.",
                ),
                ("human", "{input}"),
            ]
        )

        # 메모리 초기화: ConversationBufferMemory를 사용하여 모든 대화 내역 자동 저장
        self.memory = ConversationBufferMemory(return_messages=True)

        # 대화 체인 생성: 프롬프트 템플릿과 모델을 체인으로 연결
        self.chain = RunnableSequence(self.prompt | self.llm)

    async def get_response(self, user_input: str) -> str:
        # 사용자 입력을 메모리에 추가
        self.memory.chat_memory.add_message(HumanMessage(content=user_input))

        # 대화의 모든 메시지를 입력으로 사용하여 모델에 전달
        response = self.chain.invoke({"input": user_input})

        # 모델의 응답을 메모리에 추가
        self.memory.chat_memory.add_message(AIMessage(content=response.content))

        return response.content

    async def get_chat_history(self) -> List[Dict[str, str]]:
        # 대화 내역을 반환
        return [
            {
                "role": "human" if isinstance(msg, HumanMessage) else "ai",
                "content": msg.content,
            }
            for msg in self.memory.chat_memory.messages
        ]


langchain_service = LangChainService()
