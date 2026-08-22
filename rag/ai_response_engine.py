import os
from dotenv import load_dotenv
import google.generativeai as genai

from semantic_search import SemanticSearch

# Load environment variables
load_dotenv()

# Configure Gemini
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=API_KEY)

# Load Gemini Model
model = genai.GenerativeModel("models/gemini-3.5-flash")


class AIResponseEngine:

    def __init__(self):
        print("Loading Semantic Search...")
        self.search_engine = SemanticSearch()
        print("AI Response Engine Ready!\n")

    def generate_answer(self, question):

        # Retrieve relevant chunks
        results = self.search_engine.search(question)

        context = "\n\n".join(results["documents"][0])

        prompt = f"""
You are a helpful AI assistant.

Use ONLY the context below to answer the user's question.

Context:
{context}

Question:
{question}

If the answer is not present in the context, reply:
"I could not find this information in the uploaded documents."
"""

        response = model.generate_content(prompt)

        return response.text


if __name__ == "__main__":

    engine = AIResponseEngine()

    while True:

        question = input("\nAsk a Question (type 'exit' to quit): ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        answer = engine.generate_answer(question)

        print("\n========== AI ANSWER ==========\n")
        print(answer)