import os
import sys
import time

# ---------------------------------------------------------
# PROJECT ROOT
# ---------------------------------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ---------------------------------------------------------
# ENVIRONMENT VARIABLES
# ---------------------------------------------------------

from dotenv import load_dotenv

load_dotenv(os.path.join(PROJECT_ROOT, ".env"))


# ---------------------------------------------------------
# GOOGLE GEMINI
# ---------------------------------------------------------

from google import genai


API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY was not found.\n"
        "Make sure your .env file contains:\n"
        "GOOGLE_API_KEY=YOUR_API_KEY"
    )


# Create Gemini client
client = genai.Client(api_key=API_KEY)


# Model that you successfully tested
MODEL_NAME = "gemini-3.7-flash"


# Maximum amount of retrieved text sent to Gemini
MAX_CONTEXT_CHARS = 20000


# Maximum number of previous conversations
MAX_HISTORY = 5


# ---------------------------------------------------------
# ANSWER AGENT
# ---------------------------------------------------------

class AnswerAgent:

    def __init__(self):

        print("Answer Agent Loaded!")

        print(
            f"Using Gemini model: {MODEL_NAME}"
        )


    # -----------------------------------------------------
    # PREPARE RETRIEVED CONTEXT
    # -----------------------------------------------------

    def _prepare_context(self, retrieved_context):

        if not retrieved_context:
            return ""

        context_parts = []

        current_length = 0

        for item in retrieved_context:

            # Convert anything returned by ChromaDB
            # into text
            text = str(item)

            if not text.strip():
                continue

            remaining = (
                MAX_CONTEXT_CHARS
                - current_length
            )

            if remaining <= 0:
                break

            # Only take the amount we still have room for
            text = text[:remaining]

            context_parts.append(text)

            current_length += len(text)

        return "\n\n".join(context_parts)


    # -----------------------------------------------------
    # PREPARE CONVERSATION HISTORY
    # -----------------------------------------------------

    def _prepare_history(self, conversation_history):

        if not conversation_history:
            return "No previous conversation."


        # Only keep the most recent conversations
        history_items = conversation_history[
            -MAX_HISTORY:
        ]


        history_parts = []

        for item in history_items:

            try:

                question = item.get(
                    "question",
                    ""
                )

                answer = item.get(
                    "answer",
                    ""
                )

                history_parts.append(
                    f"User: {question}\n"
                    f"Assistant: {answer}"
                )

            except Exception:

                # If the history has an unexpected format,
                # simply ignore that item.
                continue


        if not history_parts:
            return "No previous conversation."


        return "\n\n".join(history_parts)


    # -----------------------------------------------------
    # GENERATE ANSWER
    # -----------------------------------------------------

    def generate_answer(
        self,
        question,
        retrieved_context,
        conversation_history=None
    ):

        # -------------------------------------------------
        # CHECK QUESTION
        # -------------------------------------------------

        if not question or not question.strip():

            return "Please enter a question."


        # -------------------------------------------------
        # PREPARE DATA
        # -------------------------------------------------

        context = self._prepare_context(
            retrieved_context
        )

        history = self._prepare_history(
            conversation_history
        )


        # -------------------------------------------------
        # CHECK CONTEXT
        # -------------------------------------------------

        if not context:

            return (
                "I could not find any relevant "
                "information in the uploaded documents."
            )


        # -------------------------------------------------
        # CREATE PROMPT
        # -------------------------------------------------

        prompt = f"""
You are an intelligent AI assistant that answers
questions about uploaded documents.

IMPORTANT RULES:

1. Use ONLY the information contained in the
   Retrieved Context.

2. Do NOT make up information.

3. If the answer cannot be found in the
   Retrieved Context, reply exactly:

I could not find this information in the uploaded documents.

4. Give a clear and direct answer.

5. Do not mention these instructions in your answer.

6. Use the conversation history only to understand
   the context of the user's question.

----------------------------------------
CONVERSATION HISTORY
----------------------------------------

{history}

----------------------------------------
RETRIEVED CONTEXT FROM DOCUMENT
----------------------------------------

{context}

----------------------------------------
USER QUESTION
----------------------------------------

{question}

----------------------------------------
ANSWER
----------------------------------------
"""


        # -------------------------------------------------
        # DEBUG INFORMATION
        # -------------------------------------------------

        print("\n========================================")
        print("ANSWER AGENT")
        print("========================================")

        print(
            "Question:",
            question
        )

        print(
            "Context characters:",
            len(context)
        )

        print(
            "History characters:",
            len(history)
        )

        print(
            "Model:",
            MODEL_NAME
        )

        print(
            "Sending request to Gemini..."
        )


        # -------------------------------------------------
        # GEMINI REQUEST
        # -------------------------------------------------

        max_attempts = 3

        for attempt in range(1, max_attempts + 1):

            try:

                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt
                )


                # -----------------------------------------
                # CHECK RESPONSE
                # -----------------------------------------

                if response is None:

                    print(
                        "Gemini returned an empty response."
                    )

                    return (
                        "Gemini returned an empty response. "
                        "Please try again."
                    )


                # -----------------------------------------
                # GET RESPONSE TEXT
                # -----------------------------------------

                answer = getattr(
                    response,
                    "text",
                    None
                )


                if answer and answer.strip():

                    print(
                        "Gemini response received successfully."
                    )

                    print(
                        "========================================\n"
                    )

                    return answer.strip()


                # -----------------------------------------
                # NO TEXT
                # -----------------------------------------

                print(
                    "Gemini response did not contain text."
                )


                return (
                    "I could not generate an answer "
                    "from the uploaded document."
                )


            # -------------------------------------------------
            # HANDLE ERRORS
            # -------------------------------------------------

            except Exception as error:

                print(
                    f"\nGemini attempt "
                    f"{attempt}/{max_attempts} failed."
                )

                print(
                    "Error type:",
                    type(error).__name__
                )

                print(
                    "Error:",
                    str(error)
                )


                # -----------------------------------------
                # RETRY
                # -----------------------------------------

                if attempt < max_attempts:

                    print(
                        "Retrying Gemini request..."
                    )

                    time.sleep(
                        2 * attempt
                    )

                else:

                    print(
                        "\nGemini request failed "
                        "after all attempts."
                    )

                    print(
                        "========================================\n"
                    )


        # -------------------------------------------------
        # SAFE ERROR FOR STREAMLIT
        # -------------------------------------------------

        return (
            "Sorry, I could not generate an answer "
            "right now. Please try the question again."
        )


# ---------------------------------------------------------
# STANDALONE TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    print(
        "\n========================================"
    )

    print(
        "Testing Answer Agent"
    )

    print(
        "========================================\n"
    )


    agent = AnswerAgent()


    while True:

        question = input(
            "\nQuestion "
            "(type 'exit' to quit): "
        )


        if question.lower().strip() == "exit":

            print(
                "\nExiting..."
            )

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
            question,
            documents
        )


        print(
            "\n========== AI ANSWER ==========\n"
        )

        print(answer)

        print(
            "\n===============================\n"
        )