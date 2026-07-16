# Need to clean
# the way we are asking for different options from user, this is dynamic prompt, we have a static part with placeholders, users input will fill those placeholders so, prompt will be dynamically chnaging for each query asked.
# In promptmplate we have default validation - if we will pass less or more input, code will throw error - advantage of using promptemplate over fstring. Whatever will happen that will  happen during dev time, in prod it will be safe.
# Using PrompTemplate prompts are reusable, in f-string it's not. Can store this dynamic prompt with placeholders in json format, import it where needed.

# loading prompts in a JSON file to reuse
# here in one file we took all user input and from that file prompt will be generated, and then generated prompts will be used in multiple other places
# create prompt_generator.py file
from langchain_core.prompts import PromptTemplate
# write the full template
template.save('template.json')
# import in the file where this prompt will be required
template = load_prompt('template.json')

# basic cli chatbot
# keeping memory
# to understand which is from user, which is from AI
# learn doff msg types
# add this in prev one

A MessagesPlaceholder in LangChain is a special placeholder used inside a ChatPromptTemplate to dynamically insert chat history or a list of messages at runtime.

ChatPromptTemplate is used for multi turn messsages, Promptemplate used for single turn messages.

Here we used chat_history.txt to store older chats, ideally in prod setup is should be loaded and fetched from database.


video link - https://www.youtube.com/watch?v=3TGqlQxpuU0&list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0&index=6