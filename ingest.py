from langchain.vectorstores import Qdrant
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader

loader = PyPDFLoader("data.pdf")
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# Load the embedding model 
model_name = "BAAI/bge-large-en"
model_kwargs = {'device': 'cpu'}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
)

apikey = "kXClT-VVEv9uMhf1lbk-UKF-poX5iKCFemZP-fK5ACvpGOmmZv2lQA"
url = "https://a16705e6-75a0-4d35-81dd-f11073c3d1c7.us-east4-0.gcp.cloud.qdrant.io:6333"

# Crear la instancia de Qdrant
qdrant = Qdrant.from_documents(
    texts,
    embeddings,
    url=url,
    prefer_grpc=False,
    api_key=apikey,
    collection_name="ud_collection",
    force_recreate=True
)

print("Vector DB Successfully Created!")







