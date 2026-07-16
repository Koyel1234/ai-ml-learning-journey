# in this file a new project will be generated, tags and metadata will also be traced
# rename the run name instead of default RunnabLeSequence

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


# here we are setting the project name; during running the script, python will fetch from .env file for project name, but when it will see in script it'll overwrite the .env file projevt name with name from here; otherwise we have to change from .env file, for good setup we can keep a demo nmae in .env file and for each run we can set project name via below ethod from script itself 
import os
os.environ["LANGCHAIN_PROJECT"] = "Sequential LLM App"

prompt1 = PromptTemplate(
    template = 'Generate a detailed report on {topic}',
    input_variable = ['topic']
)

prompt2 = PromptTemplate(
    template = 'Generate a 5 pointer summary from the following text \n {text}',
    input_variable = ['text']
)

model1 = ChatOpenAI(model = 'gpt-4o-mini', temperature = 0.7)
model2 = ChatOpenAI(model = 'gpt-4o', temperature = 0.5)


parser = StrOutputParser()

chain = prompt1 | model1 | parser | prompt2 | model2 | parser

# adding this config as we want to trace some tag and metadata
config = {
    'run_name': 'Sequential Chain',
    'tags': {'llm app', 'report generation', 'summarization'},
    'metadata': {'model1': 'gpt-4o-mini', 'model1_temp': 0.7, 'parser': 'stroutputparser'}
}

result = chain.invoke({'topic': 'Unemployment in India'}, config = config)

print(result)
