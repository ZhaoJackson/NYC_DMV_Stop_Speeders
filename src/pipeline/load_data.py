from ..db import get_connection, run_query
from ..config import DATA_RAW

def load_all_raw_to_duckdb():
    print("Loading data from:", DATA_RAW)
    # TODO: Implement loading logic using duckdb.read_csv or similar
    # Example:
    # con = get_connection()
    # con.execute(f"CREATE TABLE IF NOT EXISTS raw_data AS SELECT * FROM read_csv_auto('{DATA_RAW}/*.csv')")
    pass
