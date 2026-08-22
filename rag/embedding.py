from sentence_transformers import SentenceTransformer


class EmbeddingModel:

    def __init__(self):
        print("Loading embedding model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        print("Model loaded successfully!\n")

    def create_embeddings(self, chunks):
        embeddings = self.model.encode(chunks)
        return embeddings


if __name__ == "__main__":

    chunks = [
        "Artificial Intelligence is transforming the world.",
        "Large Language Models understand human language.",
        "Vector Databases store embeddings."
    ]

    embedder = EmbeddingModel()

    vectors = embedder.create_embeddings(chunks)

    print(f"Total embeddings: {len(vectors)}")
    print(f"Embedding Dimension: {len(vectors[0])}")

    print("\nFirst 10 values of the first embedding:")
    print(vectors[0][:10])