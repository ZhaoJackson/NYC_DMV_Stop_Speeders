from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_RAW = BASE_DIR / "data" / "raw"
DATA_INTERIM = BASE_DIR / "data" / "interim"
DATA_PROCESSED = BASE_DIR / "data" / "processed"

# Thresholds
POINT_THRESHOLD_24M = 11
TICKET_THRESHOLD_12M = 16

WINDOW_24M = 24  # months
WINDOW_12M = 12  # months

# DuckDB database path
DUCKDB_PATH = BASE_DIR / "data" / "super_speeders.duckdb"
