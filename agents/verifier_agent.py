class VerifierAgent:

    def __init__(self):
        print("Verifier Agent Loaded!")

    def verify(self, question, retrieved_context):

        # No document found
        if not retrieved_context or len(retrieved_context) == 0:
            return {
                "verified": False,
                "reason": "No relevant document was retrieved."
            }

        question = question.lower()

        # Questions that are obviously about the uploaded document
        document_queries = [
            "summary",
            "summarize",
            "summarise",
            "explain",
            "describe",
            "document",
            "pdf",
            "file",
            "content",
            "contents",
            "what is written",
            "overview",
            "conclusion",
            "introduction"
        ]

        if any(keyword in question for keyword in document_queries):
            return {
                "verified": True,
                "reason": "Question is about the uploaded document."
            }

        # Check if important words appear in the retrieved context
        context = " ".join(retrieved_context).lower()

        words = [
            word for word in question.split()
            if len(word) > 3
        ]

        matches = sum(
            1 for word in words
            if word in context
        )

        if matches >= 1:
            return {
                "verified": True,
                "reason": "Relevant context found."
            }

        return {
            "verified": False,
            "reason": "Retrieved context does not answer the question."
        }


if __name__ == "__main__":

    verifier = VerifierAgent()

    docs = [
        "Machine Learning is a branch of Artificial Intelligence."
    ]

    print(verifier.verify(
        "Give me summary",
        docs
    ))