import re
import nltk
from nltk.corpus import stopwords
from langchain.vectorstores import Qdrant
from langchain.embeddings import HuggingFaceBgeEmbeddings
from qdrant_client import QdrantClient

# Descargar los datos de stopwords si es la primera vez que usas nltk
nltk.download('stopwords')

def preprocesar_consulta(query):
    # Convertir a minúsculas
    query = query.lower()
    # Eliminar signos de puntuación
    query = re.sub(r'[^\w\s]', '', query)
    # Tokenizar y eliminar stop words
    stop_words = set(stopwords.words('spanish'))
    query_tokens = query.split()
    filtered_query = [word for word in query_tokens if word not in stop_words]
    return ' '.join(filtered_query)

model_name = "BAAI/bge-large-en"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

apikey = "kXClT-VVEv9uMhf1lbk-UKF-poX5iKCFemZP-fK5ACvpGOmmZv2lQA"

url = "https://a16705e6-75a0-4d35-81dd-f11073c3d1c7.us-east4-0.gcp.cloud.qdrant.io:6333"

client = QdrantClient(
    url=url,
    prefer_grpc=False,
    api_key=apikey
)

print(client)
print("##############")

db = Qdrant(client=client, embeddings=embeddings, collection_name="ud_collection")

print(db)
print("######")

# Preprocesar la consulta
query = "que modalidades de trabajo de grado existen?"
query_procesada = preprocesar_consulta(query)
print("Consulta original:", query)
print("Consulta procesada:", query_procesada)

docs = db.similarity_search_with_score(query=query_procesada, k=20)
for i in docs:
    doc, score = i
    print({"score": score, "content": doc.page_content, "metadata": doc.metadata})
