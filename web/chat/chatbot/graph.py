from langgraph.graph import START, MessagesState, StateGraph
from .schema import State
from .graph_node import call_model

# Define a new graph
workflow = StateGraph(state_schema=State)
# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
# memory = MemorySaver()
app = workflow.compile()