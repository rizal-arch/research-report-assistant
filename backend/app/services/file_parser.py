import io

import pandas as pd
from fastapi import HTTPException, status


def parse_file_to_dataframe(content: bytes, filename: str) -> pd.DataFrame:
    """Parse bytes content CSV/Excel menjadi Pandas DataFrame."""

    file_ext = filename[filename.rfind("."):].lower()

    try:
        if file_ext == ".csv":
            df = _parse_csv(content)
        elif file_ext in (".xlsx", ".xls"):
            df = _parse_excel(content)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Format file '{file_ext}' tidak dapat diproses.",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Gagal membaca file: {str(e)}. Pastikan format data valid.",
        )

    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File tidak mengandung data. Periksa isi file Anda.",
        )

    if len(df.columns) < 2:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "Data harus memiliki minimal 2 kolom "
                "untuk analisis korelasi."
            ),
        )

    return df


def _parse_csv(content: bytes) -> pd.DataFrame:
    """Coba parse CSV dengan beberapa encoding umum."""

    encodings = ["utf-8", "latin-1", "cp1252"]

    for encoding in encodings:
        try:
            return pd.read_csv(io.BytesIO(content), encoding=encoding)
        except UnicodeDecodeError:
            continue

    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Encoding file CSV tidak dikenali. Gunakan UTF-8.",
    )


def _parse_excel(content: bytes) -> pd.DataFrame:
    """Parse file Excel (xlsx/xls)."""
    return pd.read_excel(io.BytesIO(content), engine="openpyxl")
