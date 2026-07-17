## Virtual Environment
- Create a virtual environment using the following command:
  `python -m venv <venv_name>`
- This creates a folder named `<venv_name>` in the current directory.
- Activate it with:
  `source <venv_name>/Scripts/Activate`
- Creating the environment is typically a one-time setup step.
- Activate it again whenever you reopen your workspace or IDE.
- A common choice is `.venv`, which can be added to `.gitignore` to keep it out of version control.

## Required Libraries
- A `requirements.txt` file is included with the libraries needed for this GenAI learning path.
- After creating the virtual environment, install the dependencies with:
  `pip install -r requirements.txt`
- This installation step is usually done once unless dependencies change.

## API Keys
- We need API keys for each provider to use their LLM/ChatModel via their API. 
- There are two ways of using it.
    - First way:<br>
    ```
    from dotenv import load_dotenv
    load_dotenv()
    ```

    This will fetch the API key from `.env` file. Create an `.env` file having keys following the naming convention as shown later and put the sceret key in a string.
    
    - Second way:<br>
    ```
    import os
    os.environ[<api-key-name>] = "<paste-your-api-key>"
    ```

- We will go here with first way, as this is common industry practice. In any dev, staging or production case `.env` file should be gitignored (should not be pushed anyways for security purposes). For personal usecase, this key should be hidden as it will cost if used in unauthorized way.

- Refer [.env.example](.env.example) file to get understanding of `.env` file. Copy content from this file to an `.env` file and place keys as instructed.

- API keys naming convention:</br>
Below are names of `.env` keys which should be exactly as is shown. Also find descriptions of keys present.
<div align="center">
<table>
  <tr><th>Key Name</th><th>Key Description</th></tr>
  <tr><td>OPENAI_API_KEY</td><td>API key for OpenAI API</td></tr>
  <tr><td>GOOGLE_API_KEY</td><td>API key for Google API</td></tr>
  <tr><td>ANTHROPIC_API_KEY</td><td>API key for Anthropic API</td></tr>
  <tr><td>HUGGINGFACEHUB_API_TOKEN</td><td>API key for HuggingFce API</td></tr>
  <tr><td>EXCHANGERATE_API_KEY</td><td>API key for exchange rate API</td></tr>
  <tr><td>WEATHERSTACK_API_KEY</td><td>API key for weather API</td></tr>
  <tr><td>STOCKPRICE_API_KEY</td><td>API key for stock price API</td></tr>
  <tr><td>LANGCHAIN_TRACING_V2</td><td>Boolean parameter to decide trace in LangSmath</td></tr>
  <tr><td>LANGCHAIN_ENDPOINT</td><td>Engpoint used to log GenAI solution in LangSmith</td></tr>
  <tr><td>LANGCHAIN_API_KEY</td><td>API key for tracing in langSmith</td></tr>
  <tr><td>LANGCHAIN_PROJECT</td><td>Project name to log in LangSmith for your project</td></tr>
</table>
</div>

## What This Repository Covers
Here we will learn about core concepts of agentic solutions and the LangGraph framework. The repository includes notebooks, scripts, and examples covering prompts, workflows, retrieval, tools, memory, and observability.

## Key Folders and Topics
- [models](models): Model-related concepts, embeddings, and similarity search.
- [runnables](runnables): Runnable chains and composable execution patterns.
- [document_loaders](document_loaders): Loading data from PDFs, text, CSV, and other formats.
- [text_splitters](text_splitters): Chunking and text splitting techniques.
- [vector_stores](vector_stores): Vector database and retrieval store examples.
- [retrievers](retrievers): Retrieval strategies and search examples.
- [structured_output](structured_output): Structured generation and schema-based outputs.
- [output_parsers](output_parsers): Parsing model output into structured formats.
- [prompts](prompts): Prompt engineering, templates, and dynamic prompt examples.
- [rag](rag): Foundational RAG examples and implementations.
- [advanced_rag](advanced_rag): Advanced retrieval-augmented generation techniques such as Corrective RAG and Self-RAG.
- [hitl](hitl): Human-in-the-loop interaction examples.
- [subgraph](subgraph): Subgraph and shared-state workflow examples.
- [tools](tools): Tool calling and tool-augmented agent patterns.
- [workflows](workflows): Sequential, parallel, conditional, and iterative workflow examples.
- [ai_agents](ai_agents): Agent design patterns and LangChain-based agent examples.
- [persistance](persistance): Persistence and memory-related concepts.
- [chatbot](chatbot): CLI and UI-based chatbot implementations.
- [observability](observability): LangSmith and logging/monitoring examples.
- [mcp_integration](mcp_integration): Model Context Protocol client/server examples.
- [evaluation](evaluation): Evaluation approaches for prompts and model outputs.

## Referred YouTube Playlists
- CampusX LangChain playlist: https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0
- CampusX LangGraph playlist: https://www.youtube.com/playlist?list=PLKnIA16_RmvYsvB8qkUQuJmJNuiCUJFPL

## LangSmith Note
We set `LangSmith` parameter `LANGCHAIN_TRACING_V2` as `false` while working through other topics, since that setup requires some extra code change. We will set it `true` to use them when learning observability and LangSmith.

## Points to Remember
- These notebooks are not exact copy paste of notebooks/scripts shared by creators though heavily inspired.
- Here necessary changes has been done wherever required.
- At few places scripts or notebooks are splitted or merged as I felt is helping in better understanding.
- As this is my personal learning material, so necessary observations has been added from my side.
- At some places my self understanding is mentioned in code or writing format.
- At few places contents of more than one creator are merged. References are mentioned in detail for each part.
- At few parts there is additional codes added to get better understanding at any specific topic.
- There is no copyright claim on any material from any creator, whatever material is noted here though not copy paste, was originally publically published.