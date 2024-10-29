from langchain_core.tools import tool
from chatbot.model.config.load_tools_config import TOOLS_CFG
from backend.settings import PROJECT_CFG
import pytesseract
from PIL import Image
import io
from chatbot.model.utils.prepare_vectodb import PrepareVectorDB
import os




class OCRTool:
    """
    Công cụ để thực hiện OCR trên hình ảnh được tải lên và chuẩn bị thông tin cho RAG.

    Các thuộc tính:
    k (int): Số lượng tài liệu lân cận gần nhất sẽ được truy xuất dựa trên sự tương đồng của truy vấn.
    """

    def __init__(self, mongodb_uri:str, db_name:str, k: int, collection_name: str) -> None:
        """
        Khởi tạo công cụ OCRTool với cấu hình cần thiết.

        Tham số:
        k (int): Số lượng tài liệu lân cận gần nhất sẽ được truy xuất dựa trên sự tương đồng của truy vấn.
        """
        self.name = "ocr_and_lookup"
        self.embedding_model = PROJECT_CFG.embedding_model
        # self.embedding_model_instance = OpenAIEmbeddings(model=self.embedding_model)
        self.k=k
        self.mongodb_uri=mongodb_uri
        self.db_name=db_name
        self.collection_name=collection_name
        self.image_dir = 'documents/images'
        self.vectordb = PrepareVectorDB(
            doc_dir=TOOLS_CFG.user_doc_rag_unstructured_docs,
            chunk_size=TOOLS_CFG.user_doc_rag_chunk_size,
            chunk_overlap=TOOLS_CFG.user_doc_rag_chunk_overlap,
            mongodb_uri=self.mongodb_uri,
            db_name=self.db_name,
            collection_name=self.collection_name
        )

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
    
    def extract_images(self):
        """
        Kiểm tra thư mục hình ảnh và tải lên các hình ảnh có sẵn để thực hiện OCR.

        Trả về:
        list: Danh sách các văn bản đã trích xuất từ tất cả hình ảnh.
        """
        extracted_texts = []
        try:
            for filename in os.listdir(self.image_dir):
                if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    image_path = os.path.join(self.image_dir, filename)
                    with open(image_path, 'rb') as image_file:
                        image_data = image_file.read()
                        text = self.perform_ocr(image_data)
                        extracted_texts.append(text)

                    os.remove(image_path)
        except Exception as e:
            raise e
        return extracted_texts

    # def embed_text(self, text: str):
    #     """
    #     Nhúng văn bản đã trích xuất thành vector.

    #     Tham số:
    #     text (str): Văn bản đã trích xuất.

    #     Trả về:
    #     list: Vector của văn bản.
    #     """
    #     return self.embedding_model_instance.embed_documents([text])[0]
    
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
                "path": "vector",
                "numCandidates": 400,
                "limit": k,
                }
            }

        unset_stage = {
            "$unset": "vector"
        }

        project_stage = {
            "$project": {
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


@tool('ocr_and_lookup')
def ocr_and_lookup(query: str) -> str:
    """Thực hiện OCR trên hình ảnh và tìm kiếm tài liệu liên quan dựa trên văn bản đã trích xuất."""
    ocr_tool = OCRTool(
        mongodb_uri= TOOLS_CFG.user_rag_mongodb_url,
        db_name=TOOLS_CFG.user_db_name,
        k=TOOLS_CFG.user_rag_k,
        collection_name=TOOLS_CFG.user_rag_collection_name)
    extracted_texts = ocr_tool.extract_images()
    combined_text = ' '.join(extracted_texts)
    prompt = f"{query} {combined_text}"
    # vector = ocr_tool.embed_text(extracted_text)
    results = ocr_tool.similarity_search(prompt, k=ocr_tool.k)

    search_result = ""
    for result in results:
        print('---result', result)
        search_result += f"Content: {result.get('content', 'N/A')}\n"
    return search_result
