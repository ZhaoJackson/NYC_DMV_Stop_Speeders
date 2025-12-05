import duckdb
from .config import DUCKDB_PATH

def get_connection():
    return duckdb.connect(str(DUCKDB_PATH))

def run_query(query: str, params: dict | None = None):
    with get_connection() as con:
        return con.execute(query, params or {}).fetchdf()
