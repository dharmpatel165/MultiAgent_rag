import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in .env file."
    )


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(
        timeout=30000
    )
)


# =========================================================
# ANSWER AGENT
# =========================================================

class AnswerAgent:

    def __init__(self):

        print("Answer Agent Loaded!")

        # This is the model we already tested successfully
        self.model_name = "gemini-3.6-flash"


    # =====================================================
    # GENERATE ANSWER
    # =====================================================

    def generate_answer(
        self,
        question,
        retrieved_context,
        conversation_history=None
    ):

        # -------------------------------------------------
        # Conversation history
        # -------------------------------------------------

        if conversation_history is None:
            conversation_history = []


        history = ""

        if conversation_history:

            history = "\n\n".join(
                [
                    f"User: {item.get('question', '')}\n"
                    f"Assistant: {item.get('answer', '')}"
                    for item in conversation_history
                ]
            )


        # -------------------------------------------------
        # Retrieved context
        # -------------------------------------------------

        if retrieved_context:

            context = "\n\n".join(
                str(item)
                for item in retrieved_context
            )

        else:

            context = "No relevant information was retrieved."


        # -------------------------------------------------
        # Prompt
        # -------------------------------------------------

        prompt = f"""
You are an intelligent AI assistant inside a
Retrieval-Augmented Generation (RAG) system.

Your job is to answer the user's question using ONLY
the retrieved context provided below.

Do NOT use outside knowledge.

If the answer is not present in the retrieved context,
reply exactly:

I could not find this information in the uploaded documents.

Keep your answer clear, accurate, and concise.

========================
CONVERSATION HISTORY
========================

{history}

========================
RETRIEVED CONTEXT
========================

{context}

========================
USER QUESTION
========================

{question}

========================
ANSWER
========================
"""


        # =================================================
        # GEMINI REQUEST
        # =================================================

        max_attempts = 3

        for attempt in range(1, max_attempts + 1):

            try:

                print(
                    f"Gemini request "
                    f"{attempt}/{max_attempts}..."
                )


                response = client.models.generate_content(

                    model=self.model_name,

                    contents=prompt,

                    config=types.GenerateContentConfig(

                        temperature=0.2,

                        max_output_tokens=1000,

                        thinking_config=types.ThinkingConfig(
                            thinking_level="low"
                        )
                    )
                )


                # -----------------------------------------
                # Check response
                # -----------------------------------------

                if response is None:

                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )


                if not response.text:

                    raise RuntimeError(
                        "Gemini returned no text."
                    )


                print("Gemini response received.")

                return response.text


            except Exception as e:

                print(
                    f"Gemini attempt {attempt} failed."
                )

                print(
                    f"Error type: {type(e).__name__}"
                )

                print(
                    f"Error: {str(e)}"
                )


                # -----------------------------------------
                # Stop after final attempt
                # -----------------------------------------

                if attempt == max_attempts:

                    return (
                        "Gemini is temporarily unavailable. "
                        "Please try again in a moment."
                    )


                # -----------------------------------------
                # Retry delay
                # -----------------------------------------

                wait_time = attempt * 2

                print(
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)


# =========================================================
# DIRECT TERMINAL TEST
# =========================================================

if __name__ == "__main__":

    agent = AnswerAgent()


    while True:

        question = input(
            "\nQuestion "
            "(type 'exit' to quit): "
        )


        if question.lower() == "exit":

            break


        print(
            "\nEnter Retrieved Context"
        )

        print(
            "Type END on a new line when finished.\n"
        )


        documents = []


        while True:

            line = input()


            if line == "END":

                break


            documents.append(line)


        answer = agent.generate_answer(

            question=question,

            retrieved_context=documents
        )


        print(
            "\n========== AI ANSWER ==========\n"
        )

        print(answer)