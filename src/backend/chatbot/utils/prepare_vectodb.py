import os
import yaml
from pyprojroot import here
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
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
    A class to prepare and manage a Vector Database (VectorDB) using documents from a specified directory.
    The class performs the following tasks:
    - Loads and splits documents (PDFs).
    - Splits the text into chunks based on the specified chunk size and overlap.
    - Embeds the document chunks using a specified embedding model.
    - Stores the embedded vectors in a MongoDB collection.

    Attributes:
        doc_dir (str): Path to the directory containing documents (PDFs) to be processed.
        chunk_size (int): The maximum size of each chunk (in characters) into which the document text will be split.
        chunk_overlap (int): The number of overlapping characters between consecutive chunks.
        embedding_model (str): The name of the embedding model to be used for generating vector representations of text.
        mongodb_uri (str): MongoDB URI for connecting to the database.
        db_name (str): The name of the MongoDB database.
        collection_name (str): The name of the collection to be used within the MongoDB database.

    Methods:
        path_maker(file_name: str, doc_dir: str) -> str:
            Creates a full file path by joining the given directory and file name.

        run() -> None:
            Executes the process of reading documents, splitting text, embedding them into vectors, and 
            saving the resulting vector database in MongoDB.
    """

    def __init__(self,
                 doc_dir: str,
                 chunk_size: int,
                 chunk_overlap: int,
                 embedding_model: str,
                 mongodb_uri: str,
                 db_name: str,
                 collection_name: str
                 ) -> None:

        self.doc_dir = doc_dir
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model = embedding_model
        self.mongodb_uri = mongodb_uri
        self.db_name = db_name
        self.collection_name = collection_name

        # Kết nối đến MongoDB
        self.client = MongoClient(self.mongodb_uri)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def path_maker(self, file_name: str, doc_dir):
        """
        Creates a full file path by joining the provided directory and file name.

        Args:
            file_name (str): Name of the file.
            doc_dir (str): Path of the directory.

        Returns:
            str: Full path of the file.
        """
        return os.path.join(here(doc_dir), file_name)

    def run(self):
        """
        Executes the main logic to create and store document embeddings in MongoDB.

        If the collection doesn't exist:
        - It loads PDF documents from the `doc_dir`, splits them into chunks,
        - Embeds the document chunks using the specified embedding model,
        - Stores the embeddings in a MongoDB collection.

        If the collection already contains data, it skips the embedding creation process.

        Prints the creation status and the number of vectors in the MongoDB collection.

        Returns:
            None
        """
        if self.collection.count_documents({}) == 0:
            # Nếu collection chưa có dữ liệu, thực hiện quá trình tạo vector
            print(f"Creating collection '{self.collection_name}' in MongoDB.")

            file_list = os.listdir(here(self.doc_dir))
            docs = [PyPDFLoader(self.path_maker(fn, self.doc_dir)).load_and_split() for fn in file_list]
            docs_list = [item for sublist in docs for item in sublist]

            text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
            )
            doc_splits = text_splitter.split_documents(docs_list)

            embedding_model = OpenAIEmbeddings(model=self.embedding_model)
            for doc_split in doc_splits:
                vector = embedding_model.embed_documents([doc_split.page_content])[0]
                
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
    embedding_model=EMBEDDING_MODEL,
    mongodb_uri=MONGODB_URI,
    db_name=DB_NAME,
    collection_name=COLLECTION_NAME
)

prepare_db_instance.run()

# Để kiểm tra số lượng vector trong MongoDB, bạn có thể sử dụng đoạn mã dưới đây
print("Number of vectors in MongoDB collection:", prepare_db_instance.collection.count_documents({}), "\n\n")
