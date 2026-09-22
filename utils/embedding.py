from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_model = None


def get_embedding_model():
    global _model

    if _model is None:
        print("Embedding modeli yükleniyor...")

        _model = SentenceTransformer(
            MODEL_NAME,
            device="cpu"
        )

    return _model


def create_embeddings(texts: list[str]):
    if not texts:
        return []

    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        batch_size=4,
        show_progress_bar=False,
        normalize_embeddings=True
    )

    return embeddings