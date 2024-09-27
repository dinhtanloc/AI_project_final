from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.agent_toolkits import create_sql_agent
from autogen import RAGAgent
# from autogen.multi_agent import MultiAgent
from langchain.retrievers import ChromaRetriever
from langchain.embeddings import ChromaEmbedder
from langchain import LLMChain
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
import getpass
import os
from langchain.sql_database import SQLDatabase


os.environ["OPENAI_API_KEY"] = getpass.getpass()
db = SQLDatabase.from_uri(os.getenv('POSTGRESQL_DBMS_KEY'))


# Note that the docstrings here are crucial, as they will be passed along
# to the model along with the class name.
class add(BaseModel):
    """Add two integers together."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")


class multiply(BaseModel):
    """Multiply two integers together."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")


tools = [add, multiply]

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
llm_with_tools = llm.bind_tools(tools)
examples = [
    HumanMessage("What's the product of 317253 and 128472 plus four", name="example_user"),
    AIMessage("", name="example_assistant", tool_calls=[{"name": "multiply", "args": {"x": 317253, "y": 128472}, "id": "1"}]),
    ToolMessage("16505054784", tool_call_id="1"),
    AIMessage("", name="example_assistant", tool_calls=[{"name": "add", "args": {"x": 16505054784, "y": 4}, "id": "2"}]),
    ToolMessage("16505054788", tool_call_id="2"),
    AIMessage("The product of 317253 and 128472 plus four is 16505054788", name="example_assistant"),
]

system_prompt = "You are bad at math but are an expert at using a calculator. Use past tool usage as an example of how to correctly use the tools."

few_shot_prompt = ChatPromptTemplate.from_messages([("system", system_prompt), *examples, ("human", "{query}")])

agent1_chain = {"query": RunnablePassthrough()} | few_shot_prompt | llm_with_tools




# Giả sử bạn đã cấu hình LLM và cơ sở dữ liệu
agent2_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)





# Cấu hình Retriever với Chroma
chroma_retriever = ChromaRetriever(
    collection_name="my_collection",  # tên collection Chroma
    embedding_function=ChromaEmbedder().embed_text,  # Hàm embedding
    # Các tham số khác như top_k, search_type tùy chỉnh theo nhu cầu
)

# Cấu hình Reader (Language Model Chain)
llm_chain = LLMChain(
    prompt_template="Provide detailed information about the query: {query}",
    llm=llm_with_tools  # đây là LLM mà bạn đã cấu hình để tương tác với tools
)

# Cấu hình RAGAgent
agent3_rag = RAGAgent(
    retriever=chroma_retriever,  # Chroma Retriever
    reader=llm_chain,  # Reader đã cấu hình
    embedder=ChromaEmbedder()  # Embedder để chuyển đổi văn bản thành embeddings
)




# multi_agent = MultiAgent(
#     agent_map={
#         "agent1": agent1_chain,
#         "agent2": agent2_executor,
#         "agent3": agent3_rag
#     }
# )

# Hàm xử lý câu hỏi với cả 3 agent cùng tham gia
def handle_query_collaborative(query):
    responses = {}
    
    # Gọi từng agent và lưu kết quả
    responses["agent1"] = agent1_chain["query"].run(query)
    responses["agent2"] = agent2_executor(query)
    responses["agent3"] = agent3_rag.run(query)
    
    # Tổng hợp kết quả (ở đây chỉ đơn giản là in ra, có thể áp dụng logic khác để phân tích)
    print("Responses from all agents:")
    for agent_name, response in responses.items():
        print(f"{agent_name} response: {response}")
    
    # Ví dụ, bạn có thể chọn kết quả tốt nhất hoặc kết hợp các phản hồi này
    final_response = " | ".join([f"{agent_name}: {response}" for agent_name, response in responses.items()])
    return final_response

# Ví dụ xử lý một yêu cầu
final_response = handle_query_collaborative("What's 119 times 8 minus 20?")
print("Final collaborative response:", final_response)

