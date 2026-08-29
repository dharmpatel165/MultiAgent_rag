import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ---------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Make sure your .env file contains GEMINI_API_KEY=YOUR_KEY"
    )


# ---------------------------------------------------------
# GEMINI CLIENT
# ---------------------------------------------------------

client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(
        timeout=30000
    )
)


# ---------------------------------------------------------
# ANSWER AGENT
# ---------------------------------------------------------

class AnswerAgent:

    def __init__(self):

        print("Answer Agent Loaded!")

        self.model_name = "gemini-3.6-flash"


    # -----------------------------------------------------
    # GENERATE ANSWER
    # -----------------------------------------------------

    def generate_answer(
        self,
        question,
        retrieved_context,
        conversation_history=None
    ):

        if conversation_history is None:
            conversation_history = []


        # -------------------------------------------------
        # BUILD CONVERSATION HISTORY
        # -------------------------------------------------

        history = ""

        if conversation_history:

            history = "\n".join(
                [
                    f"User: {item['question']}\n"
                    f"Assistant: {item['answer']}"
                    for item in conversation_history
                ]
            )


        # -------------------------------------------------
        # BUILD RETRIEVED CONTEXT
        # -------------------------------------------------

        if retrieved_context:

            context = "\n\n".join(
                str(item)
                for item in retrieved_context
            )

        else:

            context = "No relevant context was retrieved."


        # -------------------------------------------------
        # PROMPT
        # -------------------------------------------------

        prompt = f"""
You are the Answer Agent of a RAG system.

Your job is to answer the user's question using ONLY
the information contained in the retrieved context.

Do NOT use outside knowledge.

If the answer cannot be found in the retrieved context,
reply exactly:

I could not find this information in the uploaded documents.

Be concise, accurate, and directly answer the question.

--------------------------------
CONVERSATION HISTORY
--------------------------------

{history}

--------------------------------
RETRIEVED CONTEXT
--------------------------------

{context}

--------------------------------
USER QUESTION
--------------------------------

{question}

--------------------------------
ANSWER
--------------------------------
"""


        # -------------------------------------------------
        # GEMINI REQUEST WITH RETRIES
        # -------------------------------------------------

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
                        max_output_tokens=1000
                    )
                )


                # -----------------------------------------
                # CHECK RESPONSE
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
                # LAST ATTEMPT
                # -----------------------------------------

                if attempt == max_attempts:

                    return (
                        "Unable to generate an answer right now. "
                        "Gemini is temporarily unavailable. "
                        "Please try again."
                    )


                # -----------------------------------------
                # WAIT BEFORE RETRY
                # -----------------------------------------

                wait_time = attempt * 2

                print(
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)


# ---------------------------------------------------------
# DIRECT TERMINAL TEST
# ---------------------------------------------------------

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
            "\nEnter Retrieved Context."
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