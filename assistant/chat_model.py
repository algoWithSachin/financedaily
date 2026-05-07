import os

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0,
    max_tokens=100,
    google_api_key=os.environ["GOOGLE_API_KEY"]
)

def res(query):
    messages = [
        SystemMessage(content="You are Cortexa AI, a smart finance assistant."),
        HumanMessage(content=query)
    ]
    output = model.invoke(messages)
    return output.content