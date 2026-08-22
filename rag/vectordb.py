import chromadb

from rag.loader import load_pdf
from rag.splitter import split_text
from rag.embedding import EmbeddingModel


class VectorDatabase:

    def __init__(self):

        self.client = chromadb.PersistentClient(path="chroma_db")

        # Delete old collection if it exists
        try:
            self.client.delete_collection("rag_collection")
            print("Old collection deleted.")
        except:
            pass

        # Create fresh collection
        self.collection = self.client.get_or_create_collection(
            name="rag_collection"
        )

    def add_documents(self, chunks, embeddings):

        ids = [str(i) for i in range(len(chunks))]

        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings.tolist()
        )

        print(f"\nStored {len(chunks)} chunks successfully!")

    def show_documents(self):

        data = self.collection.get()

        print("\n========== STORED DOCUMENTS ==========\n")

        for i, doc in enumerate(data["documents"]):

            print(f"Chunk {i + 1}")
            print(doc)
            print("-" * 60)


def build_database(pdf_path):

    print("Loading PDF...")

    pdf_text = load_pdf(pdf_path)

    print("Splitting PDF...")

    chunks = split_text(pdf_text)

    print(f"Total chunks created: {len(chunks)}")

    print("Creating Embeddings...")

    embedder = EmbeddingModel()

    embeddings = embedder.create_embeddings(chunks)

    print("Saving into ChromaDB...")

    db = VectorDatabase()

    db.add_documents(chunks, embeddings)

    db.show_documents()

    print("\nDatabase Ready!\n")


if __name__ == "__main__":

    pdf_path = "docs/OS_Assessment_Merged.pdf"

    build_database(pdf_path)