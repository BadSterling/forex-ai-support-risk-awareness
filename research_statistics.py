import numpy as np
import pandas as pd
from scipy import stats


def calculate_cronbach_alpha(
    data: pd.DataFrame,
    columns: list[str],
) -> float | None:
    """
    Calculate Cronbach's alpha for a group of questionnaire items.

    Alpha estimates the internal consistency of multiple items
    intended to measure the same underlying construct.
    """
    available_columns = [
        column
        for column in columns
        if column in data.columns
    ]

    if len(available_columns) < 2:
        return None

    item_data = (
        data[available_columns]
        .apply(
            pd.to_numeric,
            errors="coerce",
        )
        .dropna()
    )

    if len(item_data) < 2:
        return None

    number_of_items = len(
        available_columns
    )

    item_variances = item_data.var(
        axis=0,
        ddof=1,
    )

    total_scores = item_data.sum(
        axis=1
    )

    total_variance = total_scores.var(
        ddof=1
    )

    if (
        pd.isna(total_variance)
        or total_variance <= 0
    ):
        return None

    alpha = (
        number_of_items
        / (number_of_items - 1)
    ) * (
        1
        - item_variances.sum()
        / total_variance
    )

    return float(alpha)


def classify_cronbach_alpha(
    alpha: float | None,
) -> str:
    """
    Provide a cautious descriptive interpretation of alpha.
    """
    if alpha is None or pd.isna(alpha):
        return "Unable to calculate"

    if alpha >= 0.90:
        return "Excellent internal consistency"

    if alpha >= 0.80:
        return "Good internal consistency"

    if alpha >= 0.70:
        return "Acceptable internal consistency"

    if alpha >= 0.60:
        return "Questionable internal consistency"

    return "Low internal consistency"


def calculate_mean_confidence_interval(
    values: pd.Series,
    confidence_level: float = 0.95,
) -> dict[str, float | int | None]:
    """
    Calculate the sample mean and a t-based confidence interval.
    """
    clean_values = pd.to_numeric(
        values,
        errors="coerce",
    ).dropna()

    sample_size = len(clean_values)

    if sample_size == 0:
        return {
            "sample_size": 0,
            "mean": None,
            "standard_deviation": None,
            "standard_error": None,
            "lower_bound": None,
            "upper_bound": None,
        }

    mean_value = clean_values.mean()

    if sample_size < 2:
        return {
            "sample_size": sample_size,
            "mean": float(mean_value),
            "standard_deviation": None,
            "standard_error": None,
            "lower_bound": None,
            "upper_bound": None,
        }

    standard_deviation = clean_values.std(
        ddof=1
    )

    standard_error = (
        standard_deviation
        / np.sqrt(sample_size)
    )

    alpha = 1 - confidence_level

    critical_value = stats.t.ppf(
        1 - alpha / 2,
        df=sample_size - 1,
    )

    margin_of_error = (
        critical_value
        * standard_error
    )

    return {
        "sample_size": sample_size,
        "mean": float(mean_value),
        "standard_deviation": float(
            standard_deviation
        ),
        "standard_error": float(
            standard_error
        ),
        "lower_bound": float(
            mean_value - margin_of_error
        ),
        "upper_bound": float(
            mean_value + margin_of_error
        ),
    }


def calculate_group_confidence_intervals(
    data: pd.DataFrame,
    metric_column: str,
    group_column: str = "experiment_condition",
    confidence_level: float = 0.95,
) -> pd.DataFrame:
    """
    Calculate mean confidence intervals for each experimental group.
    """
    records = []

    for group_name, group_data in data.groupby(
        group_column
    ):
        result = (
            calculate_mean_confidence_interval(
                group_data[metric_column],
                confidence_level=confidence_level,
            )
        )

        records.append(
            {
                group_column: group_name,
                "sample_size": result[
                    "sample_size"
                ],
                "mean": result["mean"],
                "standard_deviation": result[
                    "standard_deviation"
                ],
                "standard_error": result[
                    "standard_error"
                ],
                "lower_bound": result[
                    "lower_bound"
                ],
                "upper_bound": result[
                    "upper_bound"
                ],
            }
        )

    return pd.DataFrame(records)


def calculate_eta_squared(
    data: pd.DataFrame,
    metric_column: str,
    group_column: str = "experiment_condition",
) -> float | None:
    """
    Calculate eta-squared effect size for a one-way group comparison.
    """
    analysis_data = data[
        [group_column, metric_column]
    ].copy()

    analysis_data[metric_column] = (
        pd.to_numeric(
            analysis_data[metric_column],
            errors="coerce",
        )
    )

    analysis_data = analysis_data.dropna()

    if analysis_data.empty:
        return None

    grand_mean = analysis_data[
        metric_column
    ].mean()

    total_sum_of_squares = (
        (
            analysis_data[metric_column]
            - grand_mean
        )
        ** 2
    ).sum()

    if total_sum_of_squares <= 0:
        return None

    between_group_sum_of_squares = 0.0

    for _, group_data in analysis_data.groupby(
        group_column
    ):
        group_mean = group_data[
            metric_column
        ].mean()

        between_group_sum_of_squares += (
            len(group_data)
            * (group_mean - grand_mean) ** 2
        )

    eta_squared = (
        between_group_sum_of_squares
        / total_sum_of_squares
    )

    return float(eta_squared)


def classify_eta_squared(
    eta_squared: float | None,
) -> str:
    """
    Classify eta-squared using common descriptive thresholds.
    """
    if (
        eta_squared is None
        or pd.isna(eta_squared)
    ):
        return "Unable to calculate"

    if eta_squared >= 0.14:
        return "Large effect"

    if eta_squared >= 0.06:
        return "Medium effect"

    if eta_squared >= 0.01:
        return "Small effect"

    return "Negligible effect"


def run_one_way_anova(
    data: pd.DataFrame,
    metric_column: str,
    group_column: str = "experiment_condition",
) -> dict:
    """
    Run a one-way ANOVA across experimental groups.

    ANOVA tests whether at least one group mean differs from
    the others. It does not identify which specific groups differ.
    """
    groups = []
    group_names = []

    for group_name, group_data in data.groupby(
        group_column
    ):
        clean_values = pd.to_numeric(
            group_data[metric_column],
            errors="coerce",
        ).dropna()

        if len(clean_values) >= 2:
            groups.append(
                clean_values.to_numpy()
            )

            group_names.append(
                str(group_name)
            )

    if len(groups) < 2:
        return {
            "valid": False,
            "group_names": group_names,
            "f_statistic": None,
            "p_value": None,
            "eta_squared": None,
            "effect_classification": (
                "Unable to calculate"
            ),
            "interpretation": (
                "At least two groups with two or more observations "
                "are required."
            ),
        }

    f_statistic, p_value = stats.f_oneway(
        *groups
    )

    eta_squared = calculate_eta_squared(
        data=data,
        metric_column=metric_column,
        group_column=group_column,
    )

    if p_value < 0.05:
        interpretation = (
            "The group means differ statistically at the "
            "5% significance level. ANOVA alone does not identify "
            "which specific pairs of groups differ."
        )
    else:
        interpretation = (
            "The analysis did not detect a statistically significant "
            "difference between group means at the 5% significance level."
        )

    return {
        "valid": True,
        "group_names": group_names,
        "f_statistic": float(
            f_statistic
        ),
        "p_value": float(
            p_value
        ),
        "eta_squared": eta_squared,
        "effect_classification": (
            classify_eta_squared(
                eta_squared
            )
        ),
        "interpretation": interpretation,
    }

def run_tukey_hsd(
    data: pd.DataFrame,
    metric_column: str,
    group_column: str = "experiment_condition",
    alpha: float = 0.05,
) -> pd.DataFrame:
    """
    Run Tukey's Honestly Significant Difference test.

    Tukey HSD compares every pair of group means while
    controlling the family-wise error rate.
    """
    analysis_data = data[
        [group_column, metric_column]
    ].copy()

    analysis_data[metric_column] = pd.to_numeric(
        analysis_data[metric_column],
        errors="coerce",
    )

    analysis_data = analysis_data.dropna()

    grouped_values = []
    group_names = []

    for group_name, group_data in analysis_data.groupby(
        group_column
    ):
        values = group_data[
            metric_column
        ].to_numpy()

        if len(values) >= 2:
            grouped_values.append(values)
            group_names.append(str(group_name))

    if len(grouped_values) < 2:
        return pd.DataFrame(
            columns=[
                "group_1",
                "group_2",
                "mean_difference",
                "p_value",
                "confidence_low",
                "confidence_high",
                "significant",
            ]
        )

    tukey_result = stats.tukey_hsd(
        *grouped_values
    )

    confidence_interval = (
        tukey_result.confidence_interval(
            confidence_level=1 - alpha
        )
    )

    records = []

    for first_index in range(
        len(group_names)
    ):
        for second_index in range(
            first_index + 1,
            len(group_names),
        ):
            group_1 = group_names[
                first_index
            ]

            group_2 = group_names[
                second_index
            ]

            mean_1 = analysis_data.loc[
                analysis_data[group_column]
                == group_1,
                metric_column,
            ].mean()

            mean_2 = analysis_data.loc[
                analysis_data[group_column]
                == group_2,
                metric_column,
            ].mean()

            p_value = float(
                tukey_result.pvalue[
                    first_index,
                    second_index,
                ]
            )

            records.append(
                {
                    "group_1": group_1,
                    "group_2": group_2,
                    "mean_difference": float(
                        mean_1 - mean_2
                    ),
                    "p_value": p_value,
                    "confidence_low": float(
                        confidence_interval.low[
                            first_index,
                            second_index,
                        ]
                    ),
                    "confidence_high": float(
                        confidence_interval.high[
                            first_index,
                            second_index,
                        ]
                    ),
                    "significant": (
                        p_value < alpha
                    ),
                }
            )

    return pd.DataFrame(records)


def format_p_value(
    p_value: float | None,
) -> str:
    """
    Format a p value for readable statistical reporting.
    """
    if p_value is None or pd.isna(p_value):
        return "N/A"

    if p_value < 0.001:
        return "< .001"

    return f"= {p_value:.3f}"