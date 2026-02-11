from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings

from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

DB_PATH = "vectorstore"

print("🤖 Starting Local PDF Chatbot")

# ---------------------------
# Load embeddings & vector DB
# ---------------------------
embeddings = OllamaEmbeddings(model="nomic-embed-text")

vectorstore = FAISS.load_local(
    DB_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# ---------------------------
# Local LLM
# ---------------------------
llm = Ollama(
    model="mistral",
    temperature=0
)

# ---------------------------
# Prompt Template
# ---------------------------
prompt = ChatPromptTemplate.from_template("""
Answer the question based only on the context below.
If the answer is not in the context, say you don't know.

Context:
{context}

Question:
{input}
""")

# Combine documents chain
document_chain = create_stuff_documents_chain(llm, prompt)

# Retrieval chain (NEW API)
qa = create_retrieval_chain(retriever, document_chain)

# ---------------------------
# Chat loop
# ---------------------------
print("📄 Ask questions about your PDF (type 'exit' to quit)\n")

while True:
    query = input("You: ")

    if query.lower() == "exit":
        print("👋 Bye!")
        break

    result = qa.invoke({"input": query})
    print("\n🤖 Bot:", result["answer"], "\n")