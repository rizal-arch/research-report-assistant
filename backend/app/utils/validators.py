from fastapi import HTTPException, UploadFile, status

from app.config import settings

ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}
ALLOWED_MIME_TYPES = {
    "text/csv",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel",
    "application/octet-stream",  # fallback — beberapa browser mengirim ini
}


def validate_upload_file(file: UploadFile) -> None:
    """Validasi file upload: ekstensi, MIME type, dan ukuran."""

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nama file tidak ditemukan.",
        )

    # Validasi ekstensi
    file_ext = _get_file_extension(file.filename)
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Format file '{file_ext}' tidak didukung. "
                f"Gunakan: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
            ),
        )

    # Validasi MIME type
    if file.content_type and file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"MIME type '{file.content_type}' tidak didukung.",
        )


async def validate_file_size(file: UploadFile) -> bytes:
    """Baca isi file dan validasi ukuran. Mengembalikan bytes content."""

    content = await file.read()

    if len(content) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File kosong. Unggah file yang berisi data.",
        )

    if len(content) > settings.max_file_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Ukuran file melebihi batas maksimum "
                f"({settings.max_file_size_mb} MB)."
            ),
        )

    return content


def _get_file_extension(filename: str) -> str:
    """Ambil ekstensi file dalam lowercase."""
    dot_index = filename.rfind(".")
    if dot_index == -1:
        return ""
    return filename[dot_index:].lower()
