import chromadb
from sentence_transformers import SentenceTransformer


class SemanticSearch:

    def __init__(self):

        print("Loading Vector Database...")

        self.client = chromadb.PersistentClient(path="chroma_db")

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="rag_collection"
        )

        print("Loading Embedding Model...")

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        print("System Ready!\n")

    def search(self, query, top_k=3):

        # Check whether the collection contains any documents
        data = self.collection.get()

        if len(data["ids"]) == 0:
            return {
                "documents": [[]],
                "ids": [[]],
                "distances": [[]]
            }

        # Create embedding for the query
        query_embedding = self.model.encode(query).tolist()

        # Search ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, len(data["ids"]))
        )

        return results


if __name__ == "__main__":

    search_engine = SemanticSearch()

    while True:

        question = input("\nAsk a Question (type 'exit' to quit): ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        results = search_engine.search(question)

        if len(results["documents"][0]) == 0:

            print("\nNo document has been indexed yet.\n")
            continue

        print("\n========== SEARCH RESULTS ==========\n")

        for i, document in enumerate(results["documents"][0], start=1):

            print(f"Result {i}")
            print("-" * 50)
            print(document)
            print("-" * 50)