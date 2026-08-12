import numpy as np
import pandas as pd
from scipy import stats


def compute_correlation_analysis(df: pd.DataFrame) -> dict:
    """Hitung korelasi Pearson antar semua kolom numerik."""

    numeric_df = df.select_dtypes(include=[np.number])

    if numeric_df.shape[1] < 2:
        return {
            "pairs_analyzed": 0,
            "correlations": [],
            "note": "Minimal 2 kolom numerik diperlukan untuk uji korelasi.",
        }

    correlations = []
    columns = numeric_df.columns.tolist()

    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):
            col_a = columns[i]
            col_b = columns[j]

            pair_result = _compute_pair_correlation(
                numeric_df[col_a], numeric_df[col_b], col_a, col_b
            )
            correlations.append(pair_result)

    # Urutkan berdasarkan kekuatan korelasi (|r| terbesar dulu)
    correlations.sort(
        key=lambda x: abs(x.get("pearson_r") or 0),
        reverse=True,
    )

    return {
        "pairs_analyzed": len(correlations),
        "correlations": correlations,
    }


def _compute_pair_correlation(
    series_a: pd.Series,
    series_b: pd.Series,
    name_a: str,
    name_b: str,
) -> dict:
    """Hitung korelasi Pearson untuk satu pasang kolom."""

    # Buang baris yang salah satu atau keduanya NaN
    mask = series_a.notna() & series_b.notna()
    clean_a = series_a[mask]
    clean_b = series_b[mask]

    valid_count = int(mask.sum())

    if valid_count < 3:
        return {
            "column_a": name_a,
            "column_b": name_b,
            "valid_pairs": valid_count,
            "pearson_r": None,
            "p_value": None,
            "strength": None,
            "note": "Data terlalu sedikit (min. 3 pasang non-null).",
        }

    # Cek apakah salah satu kolom constant (std = 0)
    if clean_a.std() == 0 or clean_b.std() == 0:
        return {
            "column_a": name_a,
            "column_b": name_b,
            "valid_pairs": valid_count,
            "pearson_r": None,
            "p_value": None,
            "strength": None,
            "note": "Salah satu variabel bernilai konstan.",
        }

    r_value, p_value = stats.pearsonr(clean_a, clean_b)

    return {
        "column_a": name_a,
        "column_b": name_b,
        "valid_pairs": valid_count,
        "pearson_r": _safe_round(r_value),
        "p_value": _safe_round(p_value, 6),
        "strength": _interpret_correlation(r_value),
        "significant": p_value < 0.05 if p_value is not None else None,
    }


def _interpret_correlation(r: float) -> str:
    """Interpretasi kekuatan korelasi berdasarkan |r|."""
    abs_r = abs(r)
    if abs_r >= 0.8:
        return "Sangat Kuat"
    elif abs_r >= 0.6:
        return "Kuat"
    elif abs_r >= 0.4:
        return "Sedang"
    elif abs_r >= 0.2:
        return "Lemah"
    else:
        return "Sangat Lemah"


def _safe_round(value, decimals: int = 4) -> float | None:
    if value is None or (isinstance(value, float) and (np.isnan(value) or np.isinf(value))):
        return None
    return round(float(value), decimals)
