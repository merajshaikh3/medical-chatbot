from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

class PDFIndexer:
    def __init__(self, doc_path:str, vector_store_path: str, chunk_size: int=500, chunk_overlap: int=50)-> None:
        self.doc_path = doc_path
        self.vector_store_path = vector_store_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def _load_documents(self):
        loader = DirectoryLoader(self.doc_path, glob="**/*.pdf", loader_cls=PyPDFLoader)
        return loader.load()

    def _split_text(self, docs: list):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        return text_splitter.split_documents(docs)

    def _create_embeddings(self):
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        return embeddings  # Generate embeddings directly

    def create_index(self):
        docs = self._load_documents()
        print(f"The type of docs is {type(docs)}")
        text = self._split_text(docs)
        embeddings = self._create_embeddings()

        db = FAISS.from_documents(text, embeddings)
        db.save_local(self.vector_store_path)

if __name__ == "__main__":
   DOC_PATH = r"data/"
   VECTOR_STORE_PATH = r"vector_store/"

   indexer = PDFIndexer(DOC_PATH, VECTOR_STORE_PATH)
   indexer.create_index()






