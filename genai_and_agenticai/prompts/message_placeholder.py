from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage

# chat template
# A MessagesPlaceholder in LangChain is a special placeholder used inside a ChatPromptTemplate to dynamically insert chat history or a list of messages at runtime
chat_template = ChatPromptTemplate([
    ('system', 'You are a helpful customer support agent.'),
    MessagesPlaceholder(variable_name = 'chat_history'),
    ('human', '{query}')
    ])

chat_history = []

# load chat history
# load chat history (in a text file/database load current all chats to use later, similarly today previous histories will be used)
with open('chat_history.txt') as f:
    chat_history.extend(f.readlines())

print(chat_history)

# create prompt
prompt = chat_template.invoke({'chat_history': chat_history, 'query':  'where is my refund?'}) # 'query': HumanMessage(content = 'where is my refund?')

print(prompt)
