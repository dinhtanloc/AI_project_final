import functools
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage
from langchain_community.agent_toolkits import create_sql_agent
from autogen import RAGAgent
from langchain.retrievers import ChromaRetriever
from langchain.embeddings import ChromaEmbedder
from langchain import LLMChain
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
import getpass
import os
from langchain.sql_database import SQLDatabase
from langgraph.prebuilt import ToolNode, StateGraph, AgentState
from typing import Literal

# Set environment variables
os.environ["OPENAI_API_KEY"] = getpass.getpass("Please provide your OPENAI_API_KEY:")
os.environ["POSTGRESQL_DBMS_KEY"] = getpass.getpass("Please provide your POSTGRESQL_DBMS_KEY:")

# Connect to the database
db = SQLDatabase.from_uri(os.getenv('POSTGRESQL_DBMS_KEY'))

# Define tool classes with docstrings for the model to use
class Add(BaseModel):
    """Add two integers together."""
    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")

class Multiply(BaseModel):
    """Multiply two integers together."""
    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")

# Initialize tools
tools = [Add, Multiply]

# Create language model
llm = ChatOpenAI(model="gpt-4-1106-preview")

# Define RAGAgent
chroma_retriever = ChromaRetriever(
    collection_name="my_collection",  # Replace with actual collection name
    embedding_function=ChromaEmbedder().embed_text
)
llm_chain = LLMChain(
    prompt_template="Provide detailed information about the query: {query}",
    llm=llm
)

def agent_node(state, agent, name):
    result = agent.invoke(state)
    # We convert the agent output into a format that is suitable to append to the global state
    if isinstance(result, ToolMessage):
        pass
    else:
        result = AIMessage(**result.dict(exclude={"type", "name"}), name=name)
    return {
        "messages": [result],
        # Since we have a strict workflow, we can
        # track the sender so we know who to pass to next.
        "sender": name,
    }

rag_agent = RAGAgent(
    retriever=chroma_retriever,
    reader=llm_chain,
    embedder=ChromaEmbedder()
)
rag_node = functools.partial(agent_node, agent=rag_agent, name="RAGResearcher")

# Define SQLAgent
sql_agent = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
sql_node = functools.partial(agent_node, agent=sql_agent, name="SQLResearcher")

# Define Chart Generator Agent
chart_agent = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
chart_node = functools.partial(agent_node, agent=chart_agent, name="ChartGenerator")

# ToolNode for handling tool calls
tool_node = ToolNode(tools)

# Define router function
def router(state) -> Literal["call_tool", "__end__", "continue"]:
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "call_tool"
    if "FINAL ANSWER" in last_message.content:
        return "__end__"
    return "continue"

# Create and configure workflow
workflow = StateGraph(AgentState)
workflow.add_node("RAGResearcher", rag_node)
workflow.add_node("SQLResearcher", sql_node)
workflow.add_node("ChartGenerator", chart_node)
workflow.add_node("call_tool", tool_node)

workflow.add_conditional_edges(
    "RAGResearcher",
    router,
    {"continue": "SQLResearcher", "call_tool": "call_tool", "__end__": "__end__"}
)
workflow.add_conditional_edges(
    "SQLResearcher",
    router,
    {"continue": "ChartGenerator", "call_tool": "call_tool", "__end__": "__end__"}
)
workflow.add_conditional_edges(
    "ChartGenerator",
    router,
    {"continue": "RAGResearcher", "call_tool": "call_tool", "__end__": "__end__"}
)
workflow.add_conditional_edges(
    "call_tool",
    lambda x: x["sender"],
    {
        "RAGResearcher": "RAGResearcher",
        "SQLResearcher": "SQLResearcher",
        "ChartGenerator": "ChartGenerator",
    },
)
workflow.add_edge("__start__", "RAGResearcher")
graph = workflow.compile()

# Function to handle query with the workflow
def handle_query_collaborative(query):
    initial_state = {
        "messages": [HumanMessage(query, name="user")],
        "sender": "user"
    }
    final_state = graph.run(initial_state)
    responses = [msg.content for msg in final_state["messages"]]
    final_response = " | ".join(responses)
    return final_response

# Example usage
final_response = handle_query_collaborative("What's 119 times 8 minus 20?")
print("Final collaborative response:", final_response)
