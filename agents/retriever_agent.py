import os
import sys

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from rag.semantic_search import SemanticSearch


class RetrieverAgent:

    def __init__(self):

        print("Loading Retriever Agent...")

        self.search_engine = SemanticSearch()

        print("Retriever Agent Ready!\n")

    def retrieve(self, question):

        results = self.search_engine.search(question)

        if len(results["documents"][0]) == 0:
            return []

        return results["documents"][0]


if __name__ == "__main__":

    retriever = RetrieverAgent()

    while True:

        question = input("\nQuestion (type 'exit' to quit): ")

        if question.lower() == "exit":
            break

        documents = retriever.retrieve(question)

        print("\n========== RETRIEVED DOCUMENTS ==========\n")

        if len(documents) == 0:

            print("No relevant document found.")

        else:

            for i, doc in enumerate(documents):

                print(f"\nChunk {i+1}")
                print("-" * 50)
                print(doc)