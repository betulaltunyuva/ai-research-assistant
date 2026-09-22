from utils.document_reader import read_document
from utils.text_chunker import chunk_text
from utils.embedding import create_embeddings
from utils.vector_store import (
    create_faiss_index,
    search_faiss
)


def prepare_document(
    file_path: str,
    chunk_size: int = 500,
    overlap: int = 50
):
    document = read_document(file_path)

    chunks = chunk_text(
        document["text"],
        chunk_size=chunk_size,
        overlap=overlap
    )

    embeddings = create_embeddings(chunks)

    index = create_faiss_index(embeddings)

    return {
        "document": document,
        "chunks": chunks,
        "index": index
    }


def retrieve_context(
    prepared_document: dict,
    question: str,
    top_k: int = 3,
    min_score: float = 0.70
):
    question_embedding = create_embeddings(
        [question]
    )[0]

    results = search_faiss(
        index=prepared_document["index"],
        query_embedding=question_embedding,
        chunks=prepared_document["chunks"],
        top_k=top_k
    )

    filtered_results = []

    for result in results:
        if result["score"] >= min_score:
            filtered_results.append(result)

    # Hiçbir sonuç eşik değerini geçmezse
    # en iyi sonucu yine de kullan.
    if not filtered_results and results:
        filtered_results = [results[0]]

    context_parts = []

    for number, result in enumerate(
        filtered_results,
        start=1
    ):
        context_parts.append(
            f"[DOC-{number}]\n"
            f"{result['chunk']}"
        )

    context = "\n\n".join(context_parts)

    return {
        "results": filtered_results,
        "context": context
    }