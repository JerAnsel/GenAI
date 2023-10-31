# GenAI

This repo contains a chatbot for a summercamp called GenAI and is capable of answering questions about the camp's details,
as well as "registering" participants. Registration is currently textual only and does not actually store any information.

## Setup

Create a .env file with your OpenAI key stored under the value OPENAI_KEY.

## Running the Chatbot

Run the main.py file as a regualar python file and chat away. The system will share the camp details and the user can begin the conversation. The conversation is displayed in the terminal and the user is prompted for each message.

### Open Question Answers

1. * First, I would remove the requirement for multiple prompts, especially the requirement for a "router". This needlessly complicates the system and reduces the quality of the chat, as the LLM is now receiving multiple instructions throughout the conversation. An LLM is perfectly capable of handling an entire conversation about camp details and registration with a single well written prompt given at the start of the conversation. Additionally, each call to OpenAI adds latency and so the routing prompt requirement slows down the system significantly.
    * Second, I would use a locally stored LLM so as to reduce latency.
    * Third, I might have GPT summarize the conversation history occasionally, to reduce the size of the input and avoid going over character limits.
    * Fourth, I could ask GPT to give a more succint, details only description of the camp, to be used internally, and then have it expand on each detail whenever the user asks for a description.
2. I would build a suite of sets of test questions to run automatically and then read through the assistant's responses to ensure the quality of the output.
3. Cases where the user tries to discuss unrelated topics could use additional handling. As the system is meant to be a chat, GPT does a good job of handling most edge cases on its own.