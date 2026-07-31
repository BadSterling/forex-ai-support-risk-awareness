import random
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd


CONDITIONS = [
    "explicit",
    "brief",
    "control",
]


EXPERIENCE_LEVELS = [
    "New to forex trading",
    "Some trading experience",
    "Experienced trader",
]


INTENTS = [
    "forex_basics",
    "lot_size",
    "leverage",
    "margin",
    "spread",
    "stop_loss",
    "guaranteed_profit",
    "account_loss",
]


RISK_LEVELS = [
    "LOW",
    "MEDIUM",
    "HIGH",
]


def clamp_likert(value: float) -> int:
    """
    Round and constrain a value to the 1–5 Likert scale.
    """
    return int(
        max(
            1,
            min(5, round(value)),
        )
    )


def generate_survey_data(
    participant_count: int = 120,
    random_seed: int = 42,
) -> pd.DataFrame:
    """
    Generate synthetic survey records for interface testing.

    The condition effects are intentionally small and artificial.
    They must not be interpreted as research findings.
    """
    random.seed(random_seed)
    np.random.seed(random_seed)

    records = []

    condition_offsets = {
        "explicit": {
            "trust": -0.05,
            "risk": 0.35,
            "disclosure": 0.90,
        },
        "brief": {
            "trust": 0.10,
            "risk": 0.20,
            "disclosure": 0.55,
        },
        "control": {
            "trust": 0.20,
            "risk": 0.00,
            "disclosure": -0.30,
        },
    }

    base_timestamp = datetime.now(
        timezone.utc
    ) - timedelta(days=60)

    for index in range(participant_count):
        condition = CONDITIONS[
            index % len(CONDITIONS)
        ]

        experience_level = random.choice(
            EXPERIENCE_LEVELS
        )

        offsets = condition_offsets[
            condition
        ]

        trust_base = np.random.normal(
            3.45 + offsets["trust"],
            0.70,
        )

        credibility_base = np.random.normal(
            3.55 + offsets["trust"],
            0.65,
        )

        risk_base = np.random.normal(
            3.35 + offsets["risk"],
            0.65,
        )

        disclosure_base = np.random.normal(
            3.10 + offsets["disclosure"],
            0.75,
        )

        participant_id = (
            f"SIM-{index + 1:04d}"
        )

        records.append(
            {
                "participant_id": participant_id,
                "experiment_condition": condition,
                "experience_level": experience_level,
                "trust_reliable": clamp_likert(
                    trust_base
                ),
                "trust_confident": clamp_likert(
                    trust_base
                    + np.random.normal(0, 0.30)
                ),
                "credibility_clear": clamp_likert(
                    credibility_base
                ),
                "risk_awareness": clamp_likert(
                    risk_base
                ),
                "risk_understanding": clamp_likert(
                    risk_base
                    + np.random.normal(0, 0.30)
                ),
                "disclosure_clear": clamp_likert(
                    disclosure_base
                ),
                "perceived_identity": (
                    generate_perceived_identity(
                        condition
                    )
                ),
                "overall_helpfulness": int(
                    np.clip(
                        np.random.normal(
                            7.0 + offsets["trust"],
                            1.5,
                        ),
                        0,
                        10,
                    ).round()
                ),
                "open_feedback": "",
                "survey_timestamp_utc": (
                    base_timestamp
                    + timedelta(
                        hours=random.randint(
                            0,
                            60 * 24,
                        )
                    )
                ).isoformat(),
                "data_source": "synthetic",
            }
        )

    return pd.DataFrame(records)


def generate_perceived_identity(
    condition: str,
) -> str:
    """
    Generate an artificial perceived-identity response.
    """
    probabilities = {
        "explicit": [
            0.72,
            0.20,
            0.06,
            0.015,
            0.005,
        ],
        "brief": [
            0.55,
            0.30,
            0.10,
            0.04,
            0.01,
        ],
        "control": [
            0.25,
            0.32,
            0.25,
            0.14,
            0.04,
        ],
    }

    options = [
        "Definitely an AI system",
        "Probably an AI system",
        "Not sure",
        "Probably a human",
        "Definitely a human",
    ]

    return random.choices(
        options,
        weights=probabilities[condition],
        k=1,
    )[0]


def generate_conversation_data(
    survey_data: pd.DataFrame,
    random_seed: int = 42,
) -> pd.DataFrame:
    """
    Generate synthetic conversation-level records
    corresponding to the survey participants.
    """
    random.seed(random_seed)
    np.random.seed(random_seed)

    records = []

    for _, participant in survey_data.iterrows():
        number_of_turns = random.randint(
            2,
            6,
        )

        for turn_number in range(
            1,
            number_of_turns + 1,
        ):
            intent = random.choice(INTENTS)

            if intent == "guaranteed_profit":
                risk_level = "HIGH"

            elif intent in {
                "leverage",
                "margin",
                "stop_loss",
                "account_loss",
            }:
                risk_level = "MEDIUM"

            else:
                risk_level = random.choices(
                    RISK_LEVELS,
                    weights=[0.82, 0.16, 0.02],
                    k=1,
                )[0]

            records.append(
                {
                    "participant_id": participant[
                        "participant_id"
                    ],
                    "experiment_condition": participant[
                        "experiment_condition"
                    ],
                    "turn_number": turn_number,
                    "timestamp_utc": participant[
                        "survey_timestamp_utc"
                    ],
                    "experience_level": participant[
                        "experience_level"
                    ],
                    "user_message": (
                        f"Synthetic question for {intent}"
                    ),
                    "detected_intent": intent,
                    "risk_level": risk_level,
                    "assistant_response": (
                        "Synthetic assistant response"
                    ),
                    "response_time_ms": round(
                        max(
                            5,
                            np.random.normal(
                                18,
                                5,
                            ),
                        ),
                        2,
                    ),
                    "data_source": "synthetic",
                }
            )

    return pd.DataFrame(records)