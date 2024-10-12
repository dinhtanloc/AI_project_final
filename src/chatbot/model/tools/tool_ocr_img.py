from langchain_openai import OpenAIEmbeddings
from langchain_core.tools import tool
from model.tools.load_tools_config import LoadToolsConfig
import pytesseract
from PIL import Image
import io

TOOLS_CFG = LoadToolsConfig()


class OCRTool:
    """
    Công cụ để thực hiện OCR trên hình ảnh được tải lên và chuẩn bị thông tin cho RAG.

    Các thuộc tính:
    embedding_model (str): Tên của mô hình embedding OpenAI để tạo ra các biểu diễn vector của văn bản đã trích xuất.
    """

    def __init__(self, embedding_model: str, k:int) -> None:
        """
        Khởi tạo công cụ OCRTool với cấu hình cần thiết.

        Tham số:
        embedding_model (str): Tên của mô hình embedding OpenAI được sử dụng để chuyển đổi các văn bản đã trích xuất thành biểu diễn vector.
        """
        self.embedding_model = embedding_model
        self.embedding_model_instance = OpenAIEmbeddings(model=self.embedding_model)
        self.k=k

    def perform_ocr(self, image_data: bytes) -> str:
        """
        Thực hiện OCR trên hình ảnh và trả về văn bản đã trích xuất.

        Tham số:
        image_data (bytes): Dữ liệu hình ảnh dưới dạng byte.

        Trả về:
        str: Văn bản đã trích xuất từ hình ảnh.
        """
        image = Image.open(io.BytesIO(image_data))
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text

    def embed_text(self, text: str):
        """
        Nhúng văn bản đã trích xuất thành vector.

        Tham số:
        text (str): Văn bản đã trích xuất.

        Trả về:
        list: Vector của văn bản.
        """
        return self.embedding_model_instance.embed_documents([text])[0]
    
    def similarity_search(self, query: str, k: int = None):
        """
        Thực hiện tìm kiếm tài liệu tương tự bằng cách sử dụng truy vấn từ người dùng.

        Tham số:
        query (str): Truy vấn để tìm kiếm tài liệu.
        k (int, tùy chọn): Số lượng tài liệu lân cận gần nhất sẽ được trả về. Nếu không cung cấp, sẽ sử dụng giá trị mặc định của đối tượng.

        Trả về:
        list: Danh sách các tài liệu phù hợp.
        """
        # embedding_model = OpenAIEmbeddings(model=self.embedding_model)
        query_vector = self.embedding_model.encode(query).tolist()

        if query_vector is None:
            return "Invalid query or embedding generation failed."

        if k is None:
            k = self.k

        vector_search_stage = {
            "$vectorSearch": {
                "index": "vector_index",
                "queryVector": query_vector,
                "path": "embedding",
                "numCandidates": 400,
                "limit": k,
                }
            }

        unset_stage = {
            "$unset": "vector"
        }

        project_stage = {
            "$project": {
                "_id": 0,
                "content": 1,
                "score": {
                    "$meta": "vectorSearchScore"
                }
            }
        }

        pipeline = [vector_search_stage, unset_stage, project_stage]

        # Execute the search
        results = self.vectordb.collection.aggregate(pipeline)
        return list(results)


@tool
def ocr_and_lookup(image: bytes) -> str:
    """Thực hiện OCR trên hình ảnh và tìm kiếm tài liệu liên quan dựa trên văn bản đã trích xuất."""
    ocr_tool = OCRTool(embedding_model="text-embedding-ada-002", k=TOOLS_CFG.user_doc_rag_k)
    extracted_text = ocr_tool.perform_ocr(image)
    vector = ocr_tool.embed_text(extracted_text)
    results = ocr_tool.similarity_search(vector, k=ocr_tool.k)

    return "\n\n".join(results)
