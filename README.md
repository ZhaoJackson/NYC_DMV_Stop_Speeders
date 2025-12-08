# Stop Super Speeders Hackathon: DSSG NYC

**Target Audience**: Technocrats, Legislative Staff, Policy Makers  
**Goal**: Design a scalable, resilient system to identify dangerous drivers ("Super Speeders") and trigger ISA (Intelligent Speed Assistance) interventions.

---

## 🏗️ Project Overview & System Architecture

This project simulates an end-to-end data management system for the **New York State/City DMV**. It aggregates data from multiple agencies (simulated as variable schema feeds) to identify two distinct types of high-risk behavior as defined by Bill A.2299/S.4045.

### 🧩 The Two Data Pipelines

The system is architected into two separate, robust pipelines to handle the distinct nature of **Vehicle** vs **Driver** data.

#### **Pipeline A: Vehicle & Plate Monitoring (Speed Cameras)**
*Target: Vehicles accumulating excessive speed camera tickets.*
- **Logic**: >= 16 speed camera violations in a trailing 12-month window.
- **Input Data**: Speed Camera Summons (Parquet, CSV, JSON feeds).
- **Technology**: SQL (DuckDB) for high-performance schema normalization and deduplication.
- **Output Artifact**: `vehicle_speed_summary.csv`
    - *Key Columns*: `plate`, `state`, `violations_12m`, `status` (TRIGGER/WARNING/OK).

#### **Pipeline B: Driver & License Monitoring (Traffic Violations)**
*Target: Individuals accumulating excessive driver license points.*
- **Logic**: >= 11 points in a trailing 18-month window.
- **Input Data**: Traffic Violation Tickets (Parquet, CSV, JSON feeds).
- **Technology**: Python (Pandas) for complex logic and point aggregation.
- **Output Artifact**: `nyc_speeding_violations_over_18_months.csv`
    - *Key Columns*: `license_id`, `county`, `points`.

---

## 🚀 Usage Guide

### 1. Data Merge Strategy Notebook
The core logic resides in `notebooks/Data_Merge_Strategy.ipynb`. This notebook:
1.  **Ingests** raw data from `data/opendata/`.
2.  **Profiles** diverse schemas from different agencies.
3.  **Normalizes** all data into a standard "Ground Truth" operational schema.
4.  **Executes** both Pipeline A and Pipeline B.
5.  **Generates** the two distinct output CSVs.

### 2. Output Files
-   **`notebooks/vehicle_speed_summary.csv`**: The list of vehicles requiring ISA installation.
-   **`notebooks/nyc_speeding_violations_over_18_months.csv`**: The list of drivers requiring ISA installation.

---

## Background Context
Intelligent Speed Assistance (ISA) devices are used to monitor the driving speeds of vehicles they installed. They are commonly referred to as “speed limiters” due to often being used with high-risk drivers.

NYCDOT’s study of drivers concluded that those with 16 or more speed safety camera violations are twice as likely to kill. Bill ([A.2299/S.4045](https://www.nysenate.gov/legislation/bills/2025/S4045/amendment/A)) proposes mandatory installation of ISA devices for:
1.  Drivers accumulating **11 or more points** within a 18-month period.
2.  Vehicles receiving **16 or more speed-camera tickets** within 12 months.

The Senate version of this bill passed in 2025, but the Assembly needs to approve this in 2026. This hackathon simulates the technical implementation of this policy.

---

## Task & Deliverables
**Task**: Design a working end-to-end system that can ingest historical and updated traffic/speeding ticket data, combine them without duplicates, and trigger alerts.

**Deliverables**:
1.  **Drivers Table** (`nyc_speeding_violations_over_18_months.csv`): License ID, Points, County.
2.  **Vehicles Table** (`vehicle_speed_summary.csv`): Plate, Violations count, Status.

---

## Prerequisites
- Complete volunteer [registration](http://www.nyc-dssg.org) on DSSG-NYC website
- Join DSSG-NYC [Slack Group](https://join.slack.com/t/nyc-dssg/shared_invite/zt-3fhzyi936-hDjiJn05j9EKY3BH9YjXgQ)
- Review DSSG [Anti-harassment Policy](https://github.com/dssg/hitchhikers-guide/blob/master/sources/dssg-manual/conduct-culture-and-communications/README.md)
- Review [Data Mapping Documentation and Architecture](https://docs.google.com/document/d/17KtxoxqKwIKNLGwd1zQ5g4ZBZgqkQ4PuH2VLyByReq4/edit?usp=sharing)
