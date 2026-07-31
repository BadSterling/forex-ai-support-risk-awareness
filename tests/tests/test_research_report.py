from research_analytics import (
    add_composite_scores,
)
from research_report import (
    generate_statistical_report,
)
from sample_data_generator import (
    generate_survey_data,
)


def test_report_contains_main_sections():
    survey_data = generate_survey_data(
        participant_count=60,
        random_seed=42,
    )

    enriched_data = add_composite_scores(
        survey_data
    )

    report = generate_statistical_report(
        survey_data=enriched_data,
        metric_column="trust_score",
        synthetic_data=True,
    )

    assert "# Forex AI Disclosure Statistical Report" in report
    assert "## Scale reliability" in report
    assert "## One-way ANOVA" in report
    assert "## Tukey HSD pairwise comparisons" in report


def test_synthetic_report_contains_warning():
    survey_data = generate_survey_data(
        participant_count=30,
        random_seed=42,
    )

    enriched_data = add_composite_scores(
        survey_data
    )

    report = generate_statistical_report(
        survey_data=enriched_data,
        metric_column="risk_awareness_score",
        synthetic_data=True,
    )

    assert "synthetic" in report.lower()
    assert "not empirical" in report.lower()