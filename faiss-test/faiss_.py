import os
import faiss
import numpy as np

embedding_dir = "embeddings"
index = None

# Initialize FAISS index
d = 768  # Dimensionality of embeddings, change if different
index = faiss.IndexFlatL2(d)

# Add embeddings to the FAISS index
for file in os.listdir(embedding_dir):
    if file.endswith("_embeddings.npy"):
        embeddings = np.load(os.path.join(embedding_dir, file))
        index.add(embeddings)

# Save the FAISS index
faiss.write_index(index, "faiss_index.index")
print("FAISS index created and saved!")