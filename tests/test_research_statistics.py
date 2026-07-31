import pandas as pd

from research_statistics import (
    calculate_cronbach_alpha,
    calculate_eta_squared,
    calculate_group_confidence_intervals,
    classify_eta_squared,
    run_one_way_anova,
    run_tukey_hsd,
)


def create_statistical_test_data():
    return pd.DataFrame(
        {
            "experiment_condition": (
                ["explicit"] * 5
                + ["brief"] * 5
                + ["control"] * 5
            ),
            "trust_reliable": [
                4, 4, 5, 4, 5,
                3, 4, 3, 4, 3,
                2, 3, 2, 3, 2,
            ],
            "trust_confident": [
                4, 5, 5, 4, 4,
                3, 3, 4, 3, 4,
                2, 2, 3, 2, 3,
            ],
            "credibility_clear": [
                5, 4, 5, 4, 5,
                4, 3, 3, 4, 3,
                3, 2, 2, 3, 2,
            ],
            "trust_score": [
                4.33, 4.33, 5.00, 4.00, 4.67,
                3.33, 3.33, 3.33, 3.67, 3.33,
                2.33, 2.33, 2.33, 2.67, 2.33,
            ],
        }
    )


def test_cronbach_alpha_is_calculated():
    data = create_statistical_test_data()

    alpha = calculate_cronbach_alpha(
        data,
        [
            "trust_reliable",
            "trust_confident",
            "credibility_clear",
        ],
    )

    assert alpha is not None
    assert alpha <= 1


def test_confidence_intervals_have_three_groups():
    data = create_statistical_test_data()

    result = (
        calculate_group_confidence_intervals(
            data=data,
            metric_column="trust_score",
        )
    )

    assert len(result) == 3

    assert {
        "lower_bound",
        "upper_bound",
    }.issubset(result.columns)


def test_eta_squared_is_valid():
    data = create_statistical_test_data()

    eta_squared = calculate_eta_squared(
        data=data,
        metric_column="trust_score",
    )

    assert eta_squared is not None
    assert 0 <= eta_squared <= 1


def test_anova_detects_group_difference():
    data = create_statistical_test_data()

    result = run_one_way_anova(
        data=data,
        metric_column="trust_score",
    )

    assert result["valid"] is True
    assert result["p_value"] < 0.05


def test_large_eta_squared_classification():
    assert (
        classify_eta_squared(0.20)
        == "Large effect"
    )

def test_tukey_hsd_returns_all_pairs():
    data = create_statistical_test_data()

    result = run_tukey_hsd(
        data=data,
        metric_column="trust_score",
    )

    # Three groups produce three pairwise comparisons.
    assert len(result) == 3

    required_columns = {
        "group_1",
        "group_2",
        "mean_difference",
        "p_value",
        "confidence_low",
        "confidence_high",
        "significant",
    }

    assert required_columns.issubset(
        result.columns
    )


def test_tukey_detects_significant_difference():
    data = create_statistical_test_data()

    result = run_tukey_hsd(
        data=data,
        metric_column="trust_score",
    )

    assert result["significant"].any()