import re


class PlannerAgent:

    def __init__(self):
        print("Planner Agent Loaded")


    def plan(self, question):

        question = question.lower()

        # Greetings
        greetings = [
            "hi",
            "hello",
            "hey",
            "good morning",
            "good evening"
        ]

        if question in greetings:
            return {
                "action": "direct",
                "reason": "Greeting detected"
            }

        # Memory questions
        memory_keywords = [
            "previous",
            "before",
            "last question",
            "history",
            "earlier"
        ]

        if any(word in question for word in memory_keywords):
            return {
                "action": "memory",
                "reason": "Conversation history required"
            }

        # Summarization
        summary_keywords = [
            "summarize",
            "summary",
            "short note",
            "brief"
        ]

        if any(word in question for word in summary_keywords):
            return {
                "action": "summarize",
                "reason": "User requested summarization"
            }

        # Default → Search document
        return {
            "action": "retrieval",
            "reason": "Needs document retrieval"
        }


if __name__ == "__main__":

    planner = PlannerAgent()

    while True:

        question = input("\nQuestion : ")

        if question == "exit":
            break

        result = planner.plan(question)

        print(result)