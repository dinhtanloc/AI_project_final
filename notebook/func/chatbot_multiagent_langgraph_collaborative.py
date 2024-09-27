import functools
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage
from langchain_community.agent_toolkits import create_sql_agent
from autogen import RAGAgent
from langchain_core.prompts import ChatPromptTemplate

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

examples = [
    HumanMessage("What's the product of 317253 and 128472 plus four", name="example_user"),
    AIMessage("", name="example_assistant", tool_calls=[{"name": "multiply", "args": {"x": 317253, "y": 128472}, "id": "1"}]),
    ToolMessage("16505054784", tool_call_id="1"),
    AIMessage("", name="example_assistant", tool_calls=[{"name": "add", "args": {"x": 16505054784, "y": 4}, "id": "2"}]),
    ToolMessage("16505054788", tool_call_id="2"),
    AIMessage("The product of 317253 and 128472 plus four is 16505054788", name="example_assistant"),
]


# Create language model
llm = ChatOpenAI(model="gpt-4-1106-preview")
llm_with_tools = llm.bind_tools(tools)

# Define few-shot prompt template
system = """You are bad at math but are an expert at using a calculator. 
Use past tool usage as an example of how to correctly use the tools."""

few_shot_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        *examples,
        ("human", "{query}"),
    ]
)

# Define RAGAgent
chroma_retriever = ChromaRetriever(
    collection_name="my_collection",  # Replace with actual collection name
    embedding_function=ChromaEmbedder().embed_text
)
# llm_chain = LLMChain(
#     prompt_template="Provide detailed information about the query: {query}",
#     llm=llm
# )

llm_chain = LLMChain(
    prompt_template=few_shot_prompt,
    llm=llm
)

# chain = {"query": RunnablePassthrough()} | few_shot_prompt | llm_with_tools


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
