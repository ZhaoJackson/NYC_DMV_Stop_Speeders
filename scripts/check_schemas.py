
import duckdb
import os
import pandas as pd
from pathlib import Path

# Setup
DB_PATH = ":memory:"
DATA_DIR = "data/opendata"

con = duckdb.connect(DB_PATH)
con.execute("INSTALL httpfs; LOAD httpfs;")

# Define files
files = {
    "speed_historic": "nyc_speed_cameras_historic.parquet",
    "speed_test1": "test1_nyc_speed_cameras.json",
    "speed_test2": "test2_nyc_speed_cameras.csv",
    "speed_test3": "test3_nyc_speed_cameras.csv",
    "traffic_historic": "nyc_traffic_violations_historic.parquet",
    "traffic_test1": "test1_nyc_traffic_violations.json",
    "traffic_test2": "test2_nyc_traffic_violations.csv",
    "traffic_test3": "test3_nyc_traffic_violations.csv"
}

print("Registering views...")
for name, filename in files.items():
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        print(f"Skipping {path} (not found)")
        continue
    
    try:
        if ".parquet" in filename:
            con.execute(f"CREATE OR REPLACE VIEW {name} AS SELECT * FROM read_parquet('{path}')")
        elif ".csv" in filename:
            # force all_varchar to avoid type inference errors initially
            con.execute(f"CREATE OR REPLACE VIEW {name} AS SELECT * FROM read_csv_auto('{path}', all_varchar=True)")
        elif ".json" in filename:
            con.execute(f"CREATE OR REPLACE VIEW {name} AS SELECT * FROM read_json_auto('{path}')")
        print(f"  Registered {name}")
    except Exception as e:
        print(f"  Failed to register {name}: {e}")

def get_schema_comparison(tables):
    all_cols = set()
    schemas = {}
    for t in tables:
        try:
            res = con.execute(f"PRAGMA table_info('{t}')").fetchall()
            # res: list of (cid, name, type, notnull, dflt_value, pk)
            col_map = {r[1]: r[2] for r in res}
            schemas[t] = col_map
            all_cols.update(col_map.keys())
        except:
            pass
            
    df = pd.DataFrame(index=sorted(list(all_cols)), columns=tables)
    for t in tables:
        for col in df.index:
            df.loc[col, t] = schemas.get(t, {}).get(col, "MISSING")
    return df

print("\n--- SPEED CAMERAS SCHEMA ---")
speed_tables = [t for t in files.keys() if "speed" in t]
print(get_schema_comparison(speed_tables).to_string())

print("\n--- TRAFFIC VIOLATIONS SCHEMA ---")
traffic_tables = [t for t in files.keys() if "traffic" in t]
print(get_schema_comparison(traffic_tables).to_string())
