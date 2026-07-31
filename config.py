APP_TITLE = "Forex AI Support & Risk Awareness Assistant"

DISCLOSURE_MODES = {
    "Explicit disclosure": (
        "I am an AI support assistant. My responses provide general "
        "educational information and may not be complete or error-free."
    ),
    "Brief disclosure": (
        "You are speaking with an AI support assistant."
    ),
    "No prominent disclosure": "",
}


EXPERIENCE_LEVELS = [
    "New to forex trading",
    "Some trading experience",
    "Experienced trader",
]


RISK_LEVELS = {
    "LOW": {
        "label": "Low informational risk",
        "description": (
            "The question is mainly educational and does not directly "
            "encourage a high-risk financial action."
        ),
    },
    "MEDIUM": {
        "label": "Moderate risk",
        "description": (
            "The topic involves trading decisions, leverage, margin or "
            "potential financial loss."
        ),
    },
    "HIGH": {
        "label": "High risk",
        "description": (
            "The question may involve unrealistic expectations, excessive "
            "leverage, guaranteed returns or potentially harmful trading behaviour."
        ),
    },
}


GENERAL_DISCLAIMER = (
    "This response is for general educational purposes only and does not "
    "constitute financial advice. Forex and CFD trading involve a substantial "
    "risk of capital loss."
)

EXPERIMENT_CONDITIONS = {
    "explicit": {
        "name": "Explicit AI disclosure",
        "message": (
            "I am an AI support assistant. My responses are generated "
            "automatically from a controlled educational knowledge base. "
            "They may be incomplete or incorrect."
        ),
    },
    "brief": {
        "name": "Brief AI disclosure",
        "message": (
            "You are speaking with an AI support assistant."
        ),
    },
    "control": {
        "name": "Control condition",
        "message": "",
    },
}


SURVEY_SCALE = {
    1: "Strongly disagree",
    2: "Disagree",
    3: "Neither agree nor disagree",
    4: "Agree",
    5: "Strongly agree",
}