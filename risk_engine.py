HIGH_RISK_KEYWORDS = [
    "guaranteed",
    "稳赚",
    "保证盈利",
    "risk free",
    "无风险",
    "borrow money",
    "借钱",
    "maximum leverage",
    "最大杠杆",
    "all in",
    "梭哈",
]


MEDIUM_RISK_KEYWORDS = [
    "leverage",
    "杠杆",
    "margin",
    "保证金",
    "stop loss",
    "止损",
    "position size",
    "仓位",
    "lose",
    "亏损",
    "profit",
    "盈利",
]


HIGH_RISK_INTENTS = {
    "guaranteed_profit",
}


MEDIUM_RISK_INTENTS = {
    "leverage",
    "margin",
    "stop_loss",
    "account_loss",
}


def classify_risk(
    message: str,
    intent: str,
) -> str:
    """
    Classify conversational risk using message content and intent.
    """
    normalised_message = message.lower()

    if intent in HIGH_RISK_INTENTS:
        return "HIGH"

    if any(
        keyword in normalised_message
        for keyword in HIGH_RISK_KEYWORDS
    ):
        return "HIGH"

    if intent in MEDIUM_RISK_INTENTS:
        return "MEDIUM"

    if any(
        keyword in normalised_message
        for keyword in MEDIUM_RISK_KEYWORDS
    ):
        return "MEDIUM"

    return "LOW"