# Step 1: Load the PDF Document

from langchain_community.document_loaders import PyPDFLoader

file_path = "F:/summer work/maktek/maktek tasks/self_learning/Ai Interns Agreement.docx (2).pdf"
loader = PyPDFLoader(file_path)
pages = loader.load()
print(f"Number of pages loaded: {len(pages)}")

# Concatenate the content of all pages into a single string
all_data = "".join(page.page_content for page in pages)

# Step 2: Split the Document
from langchain.text_splitter import TokenTextSplitter

# Initialize the text splitter with a more practical chunk size
text_splitter = TokenTextSplitter(
    chunk_size=200,  # Adjust chunk size for more practical splitting
    chunk_overlap=0
)

# Split the text into chunks
docs = text_splitter.split_text(all_data)
print(f"Number of document chunks: {len(docs)}")

#Embed the Split Text
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Embed the document chunks
doc_results = embedding_model.embed_documents(docs)

print(f"Embedding of the first chunk: {doc_results[0]}")


#vectorstore
#A vector store takes care of storing embedded data and performing vector search for you.

