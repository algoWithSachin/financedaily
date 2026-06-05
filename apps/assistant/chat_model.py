import os

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from .tool import get_last_records



model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0,
    max_tokens=100,
    google_api_key=os.environ["GOOGLE_API_KEY"]
)
tools = [get_last_records]
llm_with_tools = model.bind_tools(tools)


def res(query):

    

    messages = [
        SystemMessage(content="You are Cortexa AI, a smart finance assistant."),
        HumanMessage(content=query)
    ]
    output = llm_with_tools.invoke(messages)

    tool_calls = output.tool_calls


    if tool_calls:

        tool_call = tool_calls[0]

        tool_name = tool_call["name"]
        

        tool_args = tool_call["args"]
      

        if tool_name == "get_last_records":

            result = get_last_records.invoke(tool_args)

            return result

    return output.content



