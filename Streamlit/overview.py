import streamlit as st
import speedcamera
import drivers
import pandas as pd

def main():
    # --- Custom CSS for "Fancy" look ---
    st.markdown("""
        <style>
        .big-font {
            font-size:30px !important;
            font-weight: bold;
            color: #2E86C1;
        }
        .metric-card {
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True)

    # --- Header & Banner ---
    col1, col2 = st.columns([1, 4])
    with col1:
        # Placeholder for a logo, using an emoji for now or a reliable URL
        st.write("") # Spacer
        st.markdown("## 🚦") 
    with col2:
        st.title("NYC Safe Streets: ISA Pilot")
        st.caption("Data Science for Social Good (DSSG) - Hackathon Submission")

    st.image("https://images.unsplash.com/photo-1496568816309-51d7c20e3b21?q=80&w=2531&auto=format&fit=crop", 
             caption="Vision Zero: Making NYC Streets Safer", use_column_width=True)

    # --- Load Aggregated Data ---
    with st.spinner("Aggregating County Data..."):
        df_vehicles = speedcamera.load_data()
        df_drivers = drivers.load_data()

    if df_vehicles is not None and df_drivers is not None:
        # Calculate Stats
        # Vehicles
        vehicle_triggers = len(df_vehicles[df_vehicles['status'] == 'TRIGGER'])
        vehicle_warnings = len(df_vehicles[df_vehicles['status'] == 'WARNING'])
        potential_revenue = df_vehicles[df_vehicles['status'] == 'TRIGGER']['total_fines_12m'].sum()
        
        # Drivers
        driver_triggers = len(df_drivers) # All in this file are triggers (11+ points)
        total_points = df_drivers['points'].sum()
        
        total_mandates = vehicle_triggers + driver_triggers
        
        # --- Executive Summary Metrics ---
        st.markdown("### 📊 Executive Summary: Trailing 12-18 Months")
        
        m1, m2, m3 = st.columns(3)
        
        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🚨 Total ISA Mandates</h3>
                <p class="big-font">{total_mandates:,}</p>
                <p>Vehicles (16+ Tix) + Drivers (11+ Pts)</p>
            </div>
            """, unsafe_allow_html=True)
            
        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>⚠️ At-Risk Fleet</h3>
                <p class="big-font">{vehicle_warnings:,}</p>
                <p>Vehicles Receiving Warning Letters</p>
            </div>
            """, unsafe_allow_html=True)
            
        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>💰 Potential Impact</h3>
                <p class="big-font">${potential_revenue:,.0f}</p>
                <p>Outstanding Fines from Recidivists</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.divider()
        
        # --- Detailed Breakdown ---
        c1, c2 = st.columns(2)
        with c1:
            st.info(
                f"""
                **🚗 Vehicle Recidivism (Speed Cameras)**
                - **{vehicle_triggers:,}** Vehicles require immediate installation.
                - **{len(df_vehicles):,}** Total Unique Plates Monitored.
                - Based on **16+ Tickets** in 12 months.
                """
            )
        with c2:
            st.warning(
                f"""
                **🆔 Driver Recidivism (License Points)**
                - **{driver_triggers:,}** Drivers require immediate installation.
                - **{total_points:,}** Total Points accumulated by this group.
                - Based on **11+ Points** in 18 months.
                """
            )
            
    else:
        st.error("⚠️ Could not load data to generate summary statistics. Please run the ETL pipelines.")

    st.divider()

    # --- System Architecture (The "Technical" Content) ---
    st.markdown("### 🏗️ State-level Data Platform Architecture")
    
    st.markdown("""
    This platform simulates a scalable, multi-jurisdiction enforcement system designed to handle data from diverse NY counties.
    
    1.  **📥 Ingest & Profile**: 
        - Agnostic ingestion of CSV/JSON from County Clerks.
        - **Immutable Ground Truth**: Raw historical data is never overwritten.
    2.  **🔄 Normalize (Virtual Views)**: 
        - "Translation Layer" maps diverse county schemas to a canonical State Standard.
    3.  **🔗 Operational Merge**: 
        - `UNION ALL` + `DEDUP` logic combines History + New Feeds into a single **Operational Table**.
    4.  **⚙️ ISA Engine**: 
        - Rolling Window Aggregation (12mo for Vehicles, 18mo for Drivers).
        - Auto-tags records as `TRIGGER`, `WARNING`, or `OK`.
    
    > *"Simple enough for a county clerk to use, robust enough for state-level enforcement."*
    """)
    
    # Optional: Architecture Diagram (Mermaid or Image if we had one)
    # st.image("architecture_diagram.png")
    
    st.success("✅ System Status: Operational | 📅 Last Update: December 2025")

if __name__ == "__main__":
    main()
