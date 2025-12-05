# Stop Super Speeders Pipeline

## Project Goal
This project aims to identify and stop "super speeders" by analyzing ticket data and automating warnings or penalties.

## Data Source
Data comes from the hackathon datasets (migrated to `data/raw`).

## Structure
- `data/`: Contains raw, interim, and processed data.
- `notebooks/`: EDA and rule prototyping.
- `src/`: Source code for the pipeline and application.
    - `src/pipeline/`: Data loading, cleaning, and window computation logic.
    - `src/app/`: Dashboard and emailer logic.
- `scripts/`: Entry points to run the pipeline and tools.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill in your details:
   ```bash
   cp .env.example .env
   ```

## Usage

### Run the Pipeline
To load data, clean it, and compute lists:
```bash
python scripts/run_pipeline.py
```

### Run the Dashboard
To view the results:
```bash
streamlit run src/app/dashboard.py
```

### Send Emails (Simulation)
To send notifications:
```bash
python scripts/send_emails.py
```
