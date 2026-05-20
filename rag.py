import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

df = pd.read_csv("instagram_pairs_clean.csv")

model = SentenceTransformer("all-MiniLM-L6-v2")

contexts = df["context"].to_list()

embeddings = model.encode(contexts, show_progress_bar = True)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

faiss.write_index(index, "index.faiss")
df.to_pickle("pairs.pk1")

print(f"Index built with {index.ntotal} vectors")