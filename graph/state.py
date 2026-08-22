from typing import TypedDict, List


class AgentState(TypedDict):
    question: str
    planner_action: str
    retrieved_documents: List[str]
    verified: bool
    verification_reason: str
    conversation_history: List[dict]
    final_answer: str