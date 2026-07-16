from langchain_core.messages import SystemMessage, HumanMessage, AIMessage 
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI()

#systemmsg is always added at top and `you are a helpful...` -this is system msg
# adding message sender tag to differentiate who sends which message
messages = [
    SystemMessage(content='You are a helpful assistant'), 
    HumanMessage(content = 'Tell me about LangChain')
]


result = model.invoke(messages)
messages.append(AIMessage(content = result.content))
print(messages)
