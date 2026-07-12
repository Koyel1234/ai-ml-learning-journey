from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import requests
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_classic import hub
from dotenv import load_dotenv

load_dotenv()


# set project name (here  set this name post load_dotenv() othersise this name will be overwritted by env file's project name)
# giving a new name for tracing this agent
import os
os.environ["LANGCHAIN_PROJECT"] = "LangChain Agent"

search_tool = DuckDuckGoSearchRun()

@tool
def get_weather_data(city: str) -> str:
  """
  This function fetches the current weather data for a given city
  """
  url = f'https://api.weatherstack.com/current?access_key=f07d9636974c4120025fadf60678771b&query={city}'

  response = requests.get(url)

  return response.json()

llm = ChatOpenAI()

# Step 2: Pull the ReAct prompt from LangChain Hub
from langsmith.client import Client
client = Client()
prompt = client.pull_prompt("hwchase17/react", dangerously_pull_public_prompt=True)  # pulls the standard ReAct agent prompt

# Step 3: Create the ReAct agent manually with the pulled prompt
agent = create_react_agent(
    llm=llm,
    tools=[search_tool, get_weather_data],
    prompt=prompt
)

# Step 4: Wrap it with AgentExecutor
agent_executor = AgentExecutor(
    agent=agent,
    tools=[search_tool, get_weather_data],
    verbose=True,
    max_iterations=5
)


# Step 5: Invoke
response = agent_executor.invoke({"input": "What is the current temp of gurgaon"})
print(response)

print(response['output'])

### Similar way ask these questions in chatbot and see how it got traced.
# What is the release date of Dhadak 2?
# What is the current temp of gurgaon
# Identify the birthplace city of Kalpana Chawla (search) and give its current temperature.
