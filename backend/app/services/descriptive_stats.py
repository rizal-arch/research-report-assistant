import numpy as np
import pandas as pd


def compute_descriptive_statistics(df: pd.DataFrame) -> dict:
    """Hitung statistik deskriptif untuk semua kolom numerik."""

    numeric_df = df.select_dtypes(include=[np.number])

    if numeric_df.empty:
        return {
            "columns_analyzed": 0,
            "statistics": [],
            "note": "Tidak ditemukan kolom numerik dalam data.",
        }

    stats_list = []

    for col in numeric_df.columns:
        series = numeric_df[col].dropna()

        if series.empty:
            stats_list.append({
                "column": col,
                "count": 0,
                "note": "Semua nilai kosong (NaN)",
            })
            continue

        stats_list.append({
            "column": col,
            "count": int(series.count()),
            "missing": int(df[col].isna().sum()),
            "mean": _safe_round(series.mean()),
            "median": _safe_round(series.median()),
            "std": _safe_round(series.std()),
            "min": _safe_round(series.min()),
            "max": _safe_round(series.max()),
            "q1": _safe_round(series.quantile(0.25)),
            "q3": _safe_round(series.quantile(0.75)),
            "skewness": _safe_round(series.skew()),
            "kurtosis": _safe_round(series.kurtosis()),
        })

    return {
        "columns_analyzed": len(stats_list),
        "total_rows": len(df),
        "statistics": stats_list,
    }


def _safe_round(value, decimals: int = 4) -> float | None:
    """Bulatkan angka dengan aman, handle NaN dan Infinity."""
    if value is None or (isinstance(value, float) and (np.isnan(value) or np.isinf(value))):
        return None
    return round(float(value), decimals)
