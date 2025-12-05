import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.app.emailer import send_all_emails

if __name__ == "__main__":
    send_all_emails()
