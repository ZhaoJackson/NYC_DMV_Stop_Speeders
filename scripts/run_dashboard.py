import sys
from pathlib import Path
import os

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

# This script is a wrapper. Usually you run `streamlit run src/app/dashboard.py` directly.
# But if we want a python entry point:
if __name__ == "__main__":
    print("Please run this command in your terminal:")
    print("streamlit run src/app/dashboard.py")
