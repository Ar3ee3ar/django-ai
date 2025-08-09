from typing import Sequence, TypedDict
from typing_extensions import Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

# update application's state
class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    # language: str