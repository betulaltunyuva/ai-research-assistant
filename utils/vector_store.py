import faiss
import numpy as np


def create_faiss_index(embeddings):
    if len(embeddings) == 0:
        raise ValueError(
            "FAISS index oluşturmak için embedding gerekli."
        )

    vectors = np.asarray(
        embeddings,
        dtype="float32"
    )

    dimension = vectors.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(vectors)

    return index


def search_faiss(
    index,
    query_embedding,
    chunks,
    top_k=3
):
    query_vector = np.asarray(
        [query_embedding],
        dtype="float32"
    )

    scores, indices = index.search(
        query_vector,
        top_k
    )

    results = []

    for score, index_number in zip(
        scores[0],
        indices[0]
    ):
        if index_number == -1:
            continue

        results.append({
            "chunk": chunks[index_number],
            "score": float(score),
            "chunk_index": int(index_number)
        })

    return results