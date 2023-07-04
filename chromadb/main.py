from glob import glob
from pprint import pprint
import chromadb

client = chromadb.Client()

collection = client.create_collection("schittscreak")

documents = []
sources = []
ids = []
for idx, episode in enumerate(glob("schittscreek/*.txt")):
    documents.append(" ".join(open(episode, "r").readlines()))
    sources.append({"source": episode.split("/")[1]})
    ids.append(str(idx + 1))

collection.add(documents=documents, metadatas=sources, ids=ids)

results = collection.query(query_texts=["did johnny deliver a eulogy?"], n_results=1)

pprint(results)
