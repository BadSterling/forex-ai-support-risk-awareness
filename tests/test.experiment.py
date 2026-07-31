from config import EXPERIMENT_CONDITIONS
from experiment import (
    assign_experiment_condition,
    generate_participant_id,
)


def test_participant_id_format():
    participant_id = generate_participant_id()

    assert participant_id.startswith("P-")
    assert len(participant_id) == 10


def test_assigned_condition_is_valid():
    condition = assign_experiment_condition()

    assert condition in EXPERIMENT_CONDITIONS