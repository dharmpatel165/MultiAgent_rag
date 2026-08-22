import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use the model that worked for you
model = genai.GenerativeModel("models/gemini-3.5-flash")


class AnswerAgent:

    def __init__(self):
        print("Answer Agent Loaded!\n")

    def generate_answer(self,
                        question,
                        retrieved_context,
                        conversation_history=None):

        if conversation_history is None:
            conversation_history = []

        history = ""

        if len(conversation_history) > 0:

            history = "\n".join([
                f"User: {item['question']}\nAssistant: {item['answer']}"
                for item in conversation_history
            ])

        context = "\n".join(retrieved_context)

        prompt = f"""
You are an intelligent AI assistant.

Use ONLY the retrieved context below.

If the answer is not present,
reply exactly:

I could not find this information in the uploaded documents.

----------------------------
Conversation History

{history}

----------------------------
Retrieved Context

{context}

----------------------------
Question

{question}
"""

        response = model.generate_content(prompt)

        return response.text


if __name__ == "__main__":

    agent = AnswerAgent()

    while True:

        question = input("\nQuestion (type 'exit' to quit): ")

        if question.lower() == "exit":
            break

        print("\nEnter Retrieved Context")
        print("Type END on a new line.\n")

        documents = []

        while True:

            line = input()

            if line == "END":
                break

            documents.append(line)

        answer = agent.generate_answer(
            question,
            documents
        )

        print("\n========== AI ANSWER ==========\n")
        print(answer)