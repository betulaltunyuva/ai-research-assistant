import numpy as np

from utils.vector_store import (
    create_faiss_index,
    search_faiss
)


def test_faiss_search():
    chunks = [
        "UDP bağlantısız bir protokoldür.",
        "Kediler evcil hayvanlardır.",
        "Python bir programlama dilidir."
    ]

    embeddings = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0]
        ],
        dtype="float32"
    )

    index = create_faiss_index(
        embeddings
    )

    query_embedding = np.array(
        [1.0, 0.0, 0.0],
        dtype="float32"
    )

    results = search_faiss(
        index=index,
        query_embedding=query_embedding,
        chunks=chunks,
        top_k=2
    )

    assert len(results) == 2

    assert (
        results[0]["chunk"]
        == "UDP bağlantısız bir protokoldür."
    )

    assert results[0]["chunk_index"] == 0

    assert isinstance(
        results[0]["score"],
        float
    )