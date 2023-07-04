from glob import glob
from pprint import pprint
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings


client = chromadb.Client(
    Settings(chroma_db_impl="duckdb+parquet", persist_directory=".chromadb")
)

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
# model_name="multi-qa-MiniLM-L6-cos-v1"

collection = client.get_or_create_collection(
    "schittscreak", embedding_function=sentence_transformer_ef
)

documents = []
sources = []
ids = []
for idx, episode in enumerate(glob("schittscreek/*.txt")):
    documents.append(" ".join(open(episode, "r").readlines()))
    sources.append({"source": episode.split("/")[1]})
    ids.append(str(idx + 1))

collection.upsert(documents=documents, metadatas=sources, ids=ids)

print(collection._embedding_function)

results = collection.query(query_texts=["Johnny speech for the deceased"], n_results=1)

pprint(results)
