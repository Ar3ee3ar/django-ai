import os
import environ
from pathlib import Path
from openai import OpenAI
from langchain.chat_models import init_chat_model
from langchain_core.chat_history import InMemoryChatMessageHistory
from .schema import State
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import BaseMessage

chats_by_session_id = {}

env = environ.FileAwareEnv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR.parent, '.env'))

# Create your views here.
client = OpenAI(api_key=env("OPEN_API_KEY"))
os.environ['OPENAI_API_KEY'] = env("OPEN_API_KEY")
os.environ['LANGSMITH_TRACING'] = "true"
os.environ['LANGSMITH_API_KEY'] = env('LANGSMITH_API_KEY')
model = init_chat_model("gpt-4o-mini", model_provider="openai")

def get_chat_history(session_id: str) -> InMemoryChatMessageHistory:
    chat_history = chats_by_session_id.get(session_id)
    print(f"chat history: {chat_history}")
    if chat_history is None:
        chat_history = InMemoryChatMessageHistory()
        chats_by_session_id[session_id] = chat_history
    return chat_history

# Define the function that calls the model
def call_model(state: State, config: RunnableConfig) -> list[BaseMessage]:
    # Make sure that config is populated with the session id
    if "configurable" not in config or "session_id" not in config["configurable"]:
        raise ValueError(
            "Make sure that the config includes the following information: {'configurable': {'session_id': 'some_value'}}"
        )
    # Fetch the history of messages and append to it any new messages.
    chat_history = get_chat_history(config["configurable"]["session_id"])
    messages = list(chat_history.messages) + state["messages"]
    ai_message = model.invoke(messages)
    # Finally, update the chat message history to include
    # the new input message from the user together with the
    # response from the model.
    chat_history.add_messages(state["messages"] + [ai_message])
    print(chat_history)
    return {"messages": ai_message}