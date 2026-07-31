import re


INTENT_KEYWORDS = {
    "forex_basics": [
        "what is forex",
        "forex trading",
        "currency trading",
        "什么是外汇",
        "外汇交易是什么",
    ],
    "lot_size": [
        "lot",
        "one lot",
        "standard lot",
        "一手",
        "手数",
    ],
    "leverage": [
        "leverage",
        "leveraged",
        "杠杆",
    ],
    "margin": [
        "margin",
        "margin call",
        "保证金",
        "追加保证金",
    ],
    "spread": [
        "spread",
        "bid ask",
        "点差",
        "买卖差价",
    ],
    "stop_loss": [
        "stop loss",
        "stop-loss",
        "止损",
    ],
    "guaranteed_profit": [
        "guaranteed profit",
        "guaranteed return",
        "risk free profit",
        "稳赚",
        "保证盈利",
        "无风险收益",
    ],
    "account_loss": [
        "lose all",
        "lose everything",
        "blow my account",
        "爆仓",
        "亏光",
        "全部亏损",
    ],
}


def normalise_text(text: str) -> str:
    """
    Convert text into a simplified form for keyword matching.
    """
    cleaned_text = text.lower().strip()

    cleaned_text = re.sub(
        r"\s+",
        " ",
        cleaned_text,
    )

    return cleaned_text


def detect_intent(message: str) -> str:
    """
    Detect the most likely intent using transparent keyword rules.
    """
    normalised_message = normalise_text(message)

    for intent_name, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in normalised_message:
                return intent_name

    return "unknown"