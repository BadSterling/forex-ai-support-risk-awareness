from datetime import datetime, timezone

import pandas as pd

from research_statistics import (
    calculate_cronbach_alpha,
    calculate_group_confidence_intervals,
    classify_cronbach_alpha,
    format_p_value,
    run_one_way_anova,
    run_tukey_hsd,
)


TRUST_ITEMS = [
    "trust_reliable",
    "trust_confident",
    "credibility_clear",
]


RISK_AWARENESS_ITEMS = [
    "risk_awareness",
    "risk_understanding",
]


METRIC_LABELS = {
    "trust_score": "trust",
    "risk_awareness_score": "risk awareness",
    "disclosure_clear": "AI disclosure clarity",
    "overall_helpfulness": "overall helpfulness",
}


def describe_group_means(
    confidence_intervals: pd.DataFrame,
) -> str:
    """
    Generate a readable description of group means.
    """
    if confidence_intervals.empty:
        return (
            "Group means could not be calculated "
            "from the supplied dataset."
        )

    ordered_groups = confidence_intervals.sort_values(
        by="mean",
        ascending=False,
    )

    descriptions = []

    for _, row in ordered_groups.iterrows():
        descriptions.append(
            f"{row['experiment_condition']} "
            f"(M = {row['mean']:.2f}, "
            f"95% CI [{row['lower_bound']:.2f}, "
            f"{row['upper_bound']:.2f}])"
        )

    return "; ".join(descriptions)


def describe_tukey_results(
    tukey_results: pd.DataFrame,
) -> str:
    """
    Describe significant Tukey pairwise comparisons.
    """
    if tukey_results.empty:
        return (
            "Pairwise comparisons could not be calculated."
        )

    significant_results = tukey_results[
        tukey_results["significant"]
    ]

    if significant_results.empty:
        return (
            "Tukey HSD did not identify any statistically "
            "significant pairwise differences."
        )

    descriptions = []

    for _, row in significant_results.iterrows():
        direction = (
            "higher"
            if row["mean_difference"] > 0
            else "lower"
        )

        descriptions.append(
            f"{row['group_1']} was {direction} than "
            f"{row['group_2']} "
            f"(mean difference = "
            f"{row['mean_difference']:.2f}, "
            f"p {format_p_value(row['p_value'])})"
        )

    return "; ".join(descriptions) + "."


def generate_statistical_report(
    survey_data: pd.DataFrame,
    metric_column: str,
    synthetic_data: bool,
) -> str:
    """
    Generate a downloadable Markdown statistical report.
    """
    metric_label = METRIC_LABELS.get(
        metric_column,
        metric_column.replace("_", " "),
    )

    participant_count = survey_data[
        "participant_id"
    ].nunique()

    group_count = survey_data[
        "experiment_condition"
    ].nunique()

    trust_alpha = calculate_cronbach_alpha(
        survey_data,
        TRUST_ITEMS,
    )

    risk_alpha = calculate_cronbach_alpha(
        survey_data,
        RISK_AWARENESS_ITEMS,
    )

    confidence_intervals = (
        calculate_group_confidence_intervals(
            data=survey_data,
            metric_column=metric_column,
        )
    )

    anova_result = run_one_way_anova(
        data=survey_data,
        metric_column=metric_column,
    )

    tukey_results = run_tukey_hsd(
        data=survey_data,
        metric_column=metric_column,
    )

    generated_time = datetime.now(
        timezone.utc
    ).strftime("%Y-%m-%d %H:%M UTC")

    if synthetic_data:
        data_notice = (
            "**Important:** This report is based on synthetic "
            "demonstration data. The results are not empirical "
            "research findings."
        )
    else:
        data_notice = (
            "This report was generated from uploaded research data. "
            "Results should be interpreted in conjunction with the "
            "study design, sampling procedure and ethical approval."
        )

    if anova_result["valid"]:
        anova_text = (
            f"A one-way ANOVA was conducted to compare "
            f"{metric_label} across disclosure conditions. "
            f"The analysis produced "
            f"F = {anova_result['f_statistic']:.3f}, "
            f"p {format_p_value(anova_result['p_value'])}, "
            f"and η² = "
            f"{anova_result['eta_squared']:.3f}. "
            f"The estimated effect was classified as "
            f"{anova_result['effect_classification'].lower()}."
        )
    else:
        anova_text = (
            "The ANOVA could not be calculated because "
            "there were insufficient valid group observations."
        )

    report = f"""# Forex AI Disclosure Statistical Report

Generated: {generated_time}

{data_notice}

## Analysis overview

- Participants: {participant_count}
- Disclosure conditions: {group_count}
- Selected outcome: {metric_label}

## Scale reliability

### Trust scale

Cronbach's alpha: {
    f"{trust_alpha:.3f}"
    if trust_alpha is not None
    else "N/A"
}

Interpretation: {
    classify_cronbach_alpha(trust_alpha)
}

### Risk-awareness scale

Cronbach's alpha: {
    f"{risk_alpha:.3f}"
    if risk_alpha is not None
    else "N/A"
}

Interpretation: {
    classify_cronbach_alpha(risk_alpha)
}

Cronbach's alpha describes internal consistency. It does not by itself establish that a scale is valid.

## Group means and confidence intervals

{describe_group_means(confidence_intervals)}

## One-way ANOVA

{anova_text}

{anova_result["interpretation"]}

## Tukey HSD pairwise comparisons

{describe_tukey_results(tukey_results)}

## Interpretation limitations

- Statistical significance does not necessarily imply practical importance.
- ANOVA assumes independent observations, approximately normal residuals and reasonably similar group variances.
- Tukey HSD is intended as a follow-up comparison after examining the overall group effect.
- Results from synthetic data must never be presented as real participant findings.
- Findings from uploaded data depend on the quality of the study design and sample.

## Project disclaimer

This report was generated by a portfolio research prototype. It is not a substitute for formal statistical review, research supervision or ethics approval.
"""

    return report