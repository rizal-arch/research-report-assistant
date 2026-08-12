from pydantic import BaseModel


class ColumnStats(BaseModel):
    column: str
    count: int
    missing: int | None = None
    mean: float | None = None
    median: float | None = None
    std: float | None = None
    min: float | None = None
    max: float | None = None
    q1: float | None = None
    q3: float | None = None
    skewness: float | None = None
    kurtosis: float | None = None
    note: str | None = None


class DescriptiveResult(BaseModel):
    columns_analyzed: int
    total_rows: int | None = None
    statistics: list[ColumnStats]
    note: str | None = None


class CorrelationPair(BaseModel):
    column_a: str
    column_b: str
    valid_pairs: int
    pearson_r: float | None = None
    p_value: float | None = None
    strength: str | None = None
    significant: bool | None = None
    note: str | None = None


class CorrelationResult(BaseModel):
    pairs_analyzed: int
    correlations: list[CorrelationPair]
    note: str | None = None


class AnalysisResponse(BaseModel):
    success: bool
    filename: str
    file_size_kb: float
    descriptive: DescriptiveResult
    correlation: CorrelationResult
    columns: list[str]
    preview_rows: list[dict]


class ErrorResponse(BaseModel):
    success: bool = False
    detail: str
