from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.tools import tool
from agent_graph.load_tools_config import LoadToolsConfig

# Load cấu hình từ file config
TOOLS_CFG = LoadToolsConfig()

class UserDocumentRAGTool:
    """
    Một công cụ để truy xuất các tài liệu liên quan được tải lên bởi người dùng, sử dụng phương pháp Tạo Dữ Liệu Tăng Cường Truy Xuất (RAG) với các vector embeddings.

    Công cụ này sử dụng một mô hình embedding của OpenAI đã được huấn luyện trước để chuyển đổi các truy vấn thành các biểu diễn dạng vector. Các vector này sau đó được sử dụng để truy vấn cơ sở dữ liệu vector Chroma (được lưu trữ trên đĩa) nhằm truy xuất top-k tài liệu hoặc mục nhập có liên quan nhất từ một bộ sưu tập cụ thể.

    Các thuộc tính:
    embedding_model (str): Tên của mô hình embedding OpenAI được sử dụng để tạo ra các biểu diễn vector của các truy vấn.
    vectordb_dir (str): Thư mục nơi cơ sở dữ liệu vector Chroma được lưu trữ trên đĩa.
    k (int): Số lượng tài liệu lân cận gần nhất (tài liệu có liên quan nhất) sẽ được truy xuất từ cơ sở dữ liệu vector.
    vectordb (Chroma): Thể hiện cơ sở dữ liệu vector Chroma được kết nối với bộ sưu tập và mô hình embedding đã chỉ định.
    Các phương thức:
    __init__: Khởi tạo công cụ bằng cách thiết lập mô hình embedding, cơ sở dữ liệu vector, và các tham số truy xuất.
    """

    def __init__(self, embedding_model: str, vectordb_dir: str, k: int, collection_name: str) -> None:
        """
        Khởi tạo công cụ UserDocumentRAGTool với cấu hình cần thiết.

        Tham số:
        embedding_model (str): Tên của mô hình embedding (ví dụ: "text-embedding-ada-002") được sử dụng để chuyển đổi các truy vấn thành biểu diễn vector.
        vectordb_dir (str): Đường dẫn thư mục nơi cơ sở dữ liệu vector Chroma được lưu trữ và bảo quản trên đĩa.
        k (int): Số lượng tài liệu lân cận gần nhất sẽ được truy xuất dựa trên sự tương đồng của truy vấn.
        collection_name (str): Tên của bộ sưu tập trong cơ sở dữ liệu vector chứa các tài liệu do người dùng tải lên.
        """
        self.embedding_model = embedding_model
        self.vectordb_dir = vectordb_dir
        self.k = k
        self.vectordb = Chroma(
            collection_name=collection_name,
            persist_directory=self.vectordb_dir,
            embedding_function=OpenAIEmbeddings(model=self.embedding_model)
        )
        print("Number of vectors in vectordb: ", self.vectordb._collection.count(), "\n\n")


@tool
def lookup_user_document(query: str) -> str:
    """Tìm kiếm các tài liệu đã tải lên của người dùng để tìm thông tin liên quan dựa trên truy vấn."""
    rag_tool = UserDocumentRAGTool(
        embedding_model=TOOLS_CFG.user_doc_rag_embedding_model,
        vectordb_dir=TOOLS_CFG.user_doc_rag_vectordb_directory,
        k=TOOLS_CFG.user_doc_rag_k,
        collection_name=TOOLS_CFG.user_doc_rag_collection_name
    )
    # Thực hiện tìm kiếm tài liệu tương tự bằng cách sử dụng query
    docs = rag_tool.vectordb.similarity_search(query, k=rag_tool.k)
    # Trả về nội dung của các tài liệu phù hợp
    return "\n\n".join([doc.page_content for doc in docs])
