from config import GENERAL_DISCLAIMER
from knowledge_base import KNOWLEDGE_BASE


def select_answer_style(
    intent: str,
    experience_level: str,
) -> str:
    """
    Select a beginner or standard answer from the knowledge base.
    """
    knowledge_item = KNOWLEDGE_BASE[intent]

    if experience_level == "New to forex trading":
        return knowledge_item["beginner_answer"]

    return knowledge_item["standard_answer"]


def generate_unknown_response(
    experience_level: str,
) -> str:
    """
    Return a safe fallback when no supported intent is found.
    """
    if experience_level == "New to forex trading":
        return (
            "I could not confidently identify the topic. You can ask me about "
            "forex basics, lots, leverage, margin, spreads, stop losses, "
            "possible losses or guaranteed-profit claims."
        )

    return (
        "I could not confidently match this question to the current knowledge "
        "base. This prototype currently supports forex basics, lot sizes, "
        "leverage, margin, spreads, stop losses, loss risk and "
        "guaranteed-return claims."
    )


def generate_response(
    intent: str,
    risk_level: str,
    experience_level: str,
) -> str:
    """
    Generate a structured response using knowledge-base content.
    """
    if intent == "unknown":
        answer = generate_unknown_response(
            experience_level=experience_level,
        )
    else:
        answer = select_answer_style(
            intent=intent,
            experience_level=experience_level,
        )

    if risk_level == "HIGH":
        risk_message = (
            "Important risk warning: This question involves a potentially "
            "harmful or unrealistic trading expectation. Guaranteed profits "
            "do not exist, and high-risk trading behaviour can lead to rapid "
            "capital loss."
        )

    elif risk_level == "MEDIUM":
        risk_message = (
            "Risk reminder: This topic can directly affect trading losses. "
            "Position size, leverage and available margin should be considered "
            "before any trading decision."
        )

    else:
        risk_message = (
            "Educational note: Understanding the product and its risks is "
            "important before considering any trading activity."
        )

    return (
        f"{answer}\n\n"
        f"{risk_message}\n\n"
        f"{GENERAL_DISCLAIMER}"
    )