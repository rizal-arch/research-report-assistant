from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import JSONResponse

from app.schemas.analysis import AnalysisResponse, ErrorResponse
from app.services.correlation import compute_correlation_analysis
from app.services.descriptive_stats import compute_descriptive_statistics
from app.services.file_parser import parse_file_to_dataframe
from app.utils.validators import validate_file_size, validate_upload_file

router = APIRouter(prefix="/api/v1", tags=["analysis"])


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    responses={
        400: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def analyze_file(file: UploadFile = File(..., description="File CSV atau Excel")):
    """
    Menerima file CSV/Excel, lalu menghasilkan:
    - Statistik deskriptif otomatis
    - Uji korelasi Pearson antar kolom numerik
    """

    # 1. Validasi metadata file
    validate_upload_file(file)

    # 2. Baca & validasi ukuran file
    content = await validate_file_size(file)

    # 3. Parse file menjadi DataFrame
    df = parse_file_to_dataframe(content, file.filename)

    # 4. Hitung statistik deskriptif
    descriptive = compute_descriptive_statistics(df)

    # 5. Hitung korelasi
    correlation = compute_correlation_analysis(df)

    # 6. Siapkan preview data (5 baris pertama)
    preview = df.head(5).fillna("N/A").to_dict(orient="records")

    # 7. Susun response
    file_size_kb = round(len(content) / 1024, 2)

    return AnalysisResponse(
        success=True,
        filename=file.filename,
        file_size_kb=file_size_kb,
        descriptive=descriptive,
        correlation=correlation,
        columns=df.columns.tolist(),
        preview_rows=preview,
    )
