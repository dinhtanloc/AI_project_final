import os
import yaml
from pyprojroot import here
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPEN_AI_API_KEY")

with open(here("configs/tools_config.yml")) as cfg:
    app_config = yaml.load(cfg, Loader=yaml.FullLoader)

# Uncomment the following configs to run for stories document
CHUNK_SIZE = app_config["stories_rag"]["chunk_size"]
CHUNK_OVERLAP = app_config["stories_rag"]["chunk_overlap"]
EMBEDDING_MODEL = app_config["stories_rag"]["embedding_model"]
MONGODB_URI = app_config["stories_rag"]["mongodb_uri"]  # URL kết nối MongoDB
DB_NAME = app_config["stories_rag"]["db_name"]  # Tên cơ sở dữ liệu MongoDB
COLLECTION_NAME = app_config["stories_rag"]["collection_name"]
DOC_DIR = app_config["stories_rag"]["unstructured_docs"]

class PrepareVectorDB:
    """
    Lớp này được sử dụng để chuẩn bị và quản lý một cơ sở dữ liệu vector (VectorDB) bằng cách sử dụng tài liệu từ một thư mục được chỉ định.
    Lớp này thực hiện các tác vụ sau:
    - Tải và chia nhỏ tài liệu (PDF).
    - Chia nhỏ văn bản thành các phần dựa trên kích thước và độ chồng chéo được chỉ định.
    - Nhúng các đoạn văn bản tài liệu bằng cách sử dụng một mô hình nhúng đã chỉ định.
    - Lưu trữ các vector đã nhúng vào một collection trong MongoDB.

    Thuộc tính:
        doc_dir (str): Đường dẫn đến thư mục chứa tài liệu (PDF) sẽ được xử lý.
        chunk_size (int): Kích thước tối đa của mỗi đoạn (tính bằng ký tự) mà văn bản tài liệu sẽ được chia nhỏ.
        chunk_overlap (int): Số ký tự chồng lấp giữa các đoạn liên tiếp.
        embedding_model (str): Tên của mô hình nhúng được sử dụng để tạo ra các biểu diễn vector của văn bản.
        mongodb_uri (str): URI MongoDB để kết nối đến cơ sở dữ liệu.
        db_name (str): Tên của cơ sở dữ liệu MongoDB.
        collection_name (str): Tên của collection sẽ được sử dụng trong cơ sở dữ liệu MongoDB.

    Phương thức:
        path_maker(file_name: str, doc_dir: str) -> str:
            Tạo một đường dẫn đầy đủ bằng cách nối thư mục đã cho với tên tệp.

        run() -> None:
            Thực hiện quá trình đọc tài liệu, chia nhỏ văn bản, nhúng chúng thành vector và
            lưu cơ sở dữ liệu vector kết quả vào MongoDB.
    """

    def __init__(self,
                 doc_dir: str,
                 chunk_size: int,
                 chunk_overlap: int,
                 mongodb_uri: str,
                 db_name: str,
                 collection_name: str
                 ) -> None:

        self.doc_dir = doc_dir
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model = SentenceTransformer("keepitreal/vietnamese-sbert")
        self.mongodb_uri = mongodb_uri
        self.db_name = db_name
        self.collection_name = collection_name

        # Kết nối đến MongoDB
        self.client = MongoClient(self.mongodb_uri)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def path_maker(self, file_name: str, doc_dir):
        """
        Tạo một đường dẫn đầy đủ bằng cách nối thư mục và tên tệp.

        Tham số:
            file_name (str): Tên của tệp.
            doc_dir (str): Đường dẫn đến thư mục.

        Trả về:
            str: Đường dẫn đầy đủ của tệp.
        """
        return os.path.join(here(doc_dir), file_name)

    def run(self):
        """
        Thực hiện logic chính để tạo và lưu các nhúng tài liệu vào MongoDB.

        Nếu collection chưa tồn tại:
        - Tải các tài liệu PDF từ `doc_dir`, chia nhỏ chúng thành các đoạn,
        - Nhúng các đoạn tài liệu bằng mô hình nhúng đã chỉ định,
        - Lưu các nhúng vào một collection trong MongoDB.

        Nếu collection đã có dữ liệu, quá trình tạo nhúng sẽ bị bỏ qua.

        In trạng thái tạo và số lượng vector trong collection MongoDB.

        Trả về:
            None
        """
        if self.collection.count_documents({}) == 0:
            # Nếu collection chưa có dữ liệu, thực hiện quá trình tạo vector
            print(f"Creating collection '{self.collection_name}' in MongoDB.")

            file_list = [fn for fn in os.listdir(here(self.doc_dir)) if fn.endswith('.pdf')]
            docs = [PyPDFLoader(self.path_maker(fn, self.doc_dir)).load_and_split() for fn in file_list]
            docs_list = [item for sublist in docs for item in sublist]

            text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
            )
            doc_splits = text_splitter.split_documents(docs_list)

            # embedding_model = OpenAIEmbeddings(model=self.embedding_model)
            for doc_split in doc_splits:
                vector = self.embedding_model.encode(doc_split.page_content).tolist()

                # Lưu vào MongoDB
                document = {
                    "content": doc_split.page_content,
                    "vector": vector,
                    # Bạn có thể thêm thông tin bổ sung nếu cần
                }
                self.collection.insert_one(document)

            print("VectorDB is created and saved in MongoDB.")
            print("Number of vectors in MongoDB collection:", self.collection.count_documents({}), "\n\n")
        else:
            print(f"Collection '{self.collection_name}' already exists in MongoDB.")

prepare_db_instance = PrepareVectorDB(
    doc_dir=DOC_DIR,
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    mongodb_uri=MONGODB_URI,
    db_name=DB_NAME,
    collection_name=COLLECTION_NAME
)

prepare_db_instance.run()

print("Number of vectors in MongoDB collection:", prepare_db_instance.collection.count_documents({}), "\n\n")