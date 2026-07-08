## Virtual Environment
- Create a virtual environment via below command:<br>
    `python -m venv <venv_name>`
- It will create a folder of \<venv_name\> in current directory.
- Activate the virtual environemnt via below command:<br>
    `source <venv_name>/Scripts/Activate`
- This creation of virtual environment is one time activity.
- Virtual environemnt should be activated each time work IDE is closed.
- You can name the virtual environment `.venv` which will lead to create folder named `.venv` and put it in `.gitigore` file to make it gitignored dring file pushing.

## Required Libraries
- There is a requirement.txt file added with all necessary libraries needed for GenAI learning.
- Post creating the virtual environment install all libraries via below command:<br>
    `pip install -r requirements.txt`
- This requirements installation is one time activity.

## API Keys
- We need API keys for each provider to use their LLM/ChatModel via their API. 
- There are two ways of using it.
    - First way:<br>
    ```
    from dotenv import load_dotenv
    load_dotenv()
    ```

    This will fetch the API key from .env file. Create an .env file having keys following the naming convention as shown later and put the sceret key in a string.
    
    - Second way:<br>
    ```
    import os
    os.environ[<api-key-name>] = "<paste-your-api-key>"
    ```

- We will go here with first way, as this is common industry practice. In any dev, staging or production case .env file should be gitignored (should not be pushed anyways for security purposes). For personal usecase, this key should be hidden as it will cost if used in unauthorized way.

- API keys naming convention:</br>
Below are names of API keys which should be exactly as is shown.
<div align="center">
<table>
  <tr><th>Provider Name</th><th>API Key Name</th></tr>
  <tr><td>OpenAI</td><td>OPENAI_API_KEY</td></tr>
  <tr><td>Google</td><td>GOOGLE_API_KEY</td></tr>
  <tr><td>Anthropic</td><td>ANTHROPIC_API_KEY</td></tr>
  <tr><td>HuggingFace</td><td>HUGGINGFACEHUB_API_KEY</td></tr>
</table>
</div>
