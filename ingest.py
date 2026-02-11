from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

PDF_PATH = "sample.pdf"
DB_PATH = "vectorstore"

print("📄 Loading PDF...")
loader = PyPDFLoader(PDF_PATH)
documents = loader.load()

print("✂️ Splitting text...")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)
chunks = splitter.split_documents(documents)

print("🧠 Creating embeddings (local)...")
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = FAISS.from_documents(chunks, embeddings)

vectorstore.save_local(DB_PATH)

print("✅ PDF ingestion completed!")