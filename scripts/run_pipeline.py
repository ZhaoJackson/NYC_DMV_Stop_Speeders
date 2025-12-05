import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.pipeline.load_data import load_all_raw_to_duckdb
from src.pipeline.clean_dedupe import clean_and_dedupe
from src.pipeline.compute_windows import compute_all_windows
from src.pipeline.export_outputs import export_triggered_lists

def main():
    load_all_raw_to_duckdb()
    clean_and_dedupe()
    compute_all_windows()
    export_triggered_lists()

if __name__ == "__main__":
    main()
