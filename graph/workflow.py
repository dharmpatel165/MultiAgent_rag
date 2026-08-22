import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from graph.state import AgentState

from agents.planner_agent import PlannerAgent
from agents.retriever_agent import RetrieverAgent
from agents.memory_agent import MemoryAgent
from agents.verifier_agent import VerifierAgent
from agents.answer_agent import AnswerAgent


# ---------------- Planner Node ----------------

def planner_node(state: AgentState, planner):

    print("Planner Agent Running...")

    result = planner.plan(state["question"])

    state["planner_action"] = result["action"]

    return state


# ---------------- Retriever Node ----------------

def retriever_node(state: AgentState, retriever):

    print("Retriever Agent Running...")

    documents = retriever.retrieve(state["question"])

    state["retrieved_documents"] = documents

    return state


# ---------------- Memory Node ----------------

def memory_node(state: AgentState, memory):

    print("Memory Agent Running...")

    state["conversation_history"] = memory.get_history()

    return state


# ---------------- Verifier Node ----------------

def verifier_node(state: AgentState, verifier):

    print("Verifier Agent Running...")

    result = verifier.verify(
        state["question"],
        state["retrieved_documents"]
    )

    state["verified"] = result["verified"]
    state["verification_reason"] = result["reason"]

    return state


# ---------------- Answer Node ----------------

def answer_node(state: AgentState, answer, memory):

    print("Answer Agent Running...")

    if not state["verified"]:

        state["final_answer"] = state["verification_reason"]
        return state

    response = answer.generate_answer(
        question=state["question"],
        retrieved_context=state["retrieved_documents"],
        conversation_history=state["conversation_history"]
    )

    state["final_answer"] = response

    memory.save(
        state["question"],
        response
    )

    return state


# ---------------- Main Workflow ----------------

def run_workflow(question):

    # Create fresh agents every time
    planner = PlannerAgent()
    retriever = RetrieverAgent()
    memory = MemoryAgent()
    verifier = VerifierAgent()
    answer = AnswerAgent()

    state = {
        "question": question,
        "planner_action": "",
        "retrieved_documents": [],
        "verified": False,
        "verification_reason": "",
        "conversation_history": [],
        "final_answer": ""
    }

    state = planner_node(state, planner)
    state = retriever_node(state, retriever)
    state = memory_node(state, memory)
    state = verifier_node(state, verifier)
    state = answer_node(state, answer, memory)

    return state["final_answer"]


# ---------------- Test ----------------

if __name__ == "__main__":

    while True:

        question = input("\nAsk a Question (type 'exit' to quit): ")

        if question.lower() == "exit":
            break

        answer = run_workflow(question)

        print("\n==============================")
        print("FINAL ANSWER")
        print("==============================\n")

        print(answer)