import streamlit as st
import pandas as pd
import altair as alt

# --- Constants & Mapping ---
BOROUGH_MAP = {
    "BK": "Brooklyn",
    "BX": "Bronx",
    "QN": "Queens",
    "MN": "Manhattan",
    "NY": "Manhattan", # Alternative code
    "ST": "Staten Island",
    "SI": "Staten Island"
}

# STATUS_COLORS = {
#     "TRIGGER": "#FF4B4B",  # Red
#     "WARNING": "#FFA500",  # Orange
#     "OK": "#00AA00"        # Green
# }
STATUS_COLORS = {
    "TRIGGER": "#FF4B4B",  # Red
    "WARNING": "#FFA500"   # Orange
}

@st.cache_data
def load_data():
    try:
        paths = ["data/exports/vehicle_speed_summary.csv", "../data/exports/vehicle_speed_summary.csv"]
        for p in paths:
            try:
                df = pd.read_csv(p)
                # Convert dates
                date_cols = ['first_violation_12m', 'last_violation_12m', 'as_of_date']
                for col in date_cols:
                    if col in df.columns:
                        df[col] = pd.to_datetime(df[col], utc=True)
                
                # Map Boroughs
                df['borough'] = df['county_last_seen'].map(BOROUGH_MAP).fillna(df['county_last_seen'])
                return df
            except FileNotFoundError:
                continue
        return None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def show_overview(df):
    st.markdown("## 🏙️ NYC Safe Streets: ISA Program Dashboard")
    st.caption("Monitoring Pilot for Mandatory Intelligent Speed Assistance (ISA) Installation")
    
    st.divider()

    # --- Top KPIs ---
    st.markdown("#### 📊 Operational Metrics (Trailing 12-Months)")
    col1, col2, col3, col4 = st.columns(4)
    
    # 1. ISA Eligible (Triggered)
    isa_triggers = df[df['status'] == 'TRIGGER']
    isa_count = len(isa_triggers)
    
    # 2. At Risk (Warning)
    warning_count = len(df[df['status'] == 'WARNING'])
    
    # 3. Revenue Ops
    total_fines = isa_triggers['total_fines_12m'].sum()
    
    # 4. Total Monitored
    total_monitored = len(df)

    col1.metric(
        "🚨 Mandate Triggers", 
        f"{isa_count:,}", 
        "16+ Tickets / 12mo", 
        delta_color="inverse", 
        help="Vehicles with >= 16 violations in the trailing 12 months. Mandatory ISA installation required."
    )
    col2.metric(
        "⚠️ At-Risk Vehicles", 
        f"{warning_count:,}", 
        "12-15 Tickets",
        help="Vehicles approaching the threshold. Warning letters sent."
    )
    col3.metric("💰 Outstanding Fines", f"${total_fines:,.0f}", "Triggered Dataset Only")
    col4.metric("🚗 Active Fleet Monitored", f"{total_monitored:,}", "Unique Plates")

    st.divider()
    
    # --- Charts ---
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("📍 Violations by Borough")
        borough_counts = df[df['status'].isin(['TRIGGER', 'WARNING'])].groupby('borough')['violations_12m'].sum().reset_index()
        
        chart_boro = alt.Chart(borough_counts).mark_bar().encode(
            x=alt.X('violations_12m', title='Total Violations'),
            y=alt.Y('borough', sort='-x', title='Borough'),
            color=alt.Color('borough', legend=None),
            tooltip=['borough', 'violations_12m']
        ).properties(height=300)
        st.altair_chart(chart_boro, use_container_width=True)
        
    with c2:
        st.subheader("📉 Risk Distribution")
        # Filter out OK for clarity
        risk_df = df[df['status'].isin(STATUS_COLORS.keys())]
        status_counts = risk_df['status'].value_counts().reset_index()
        status_counts.columns = ['status', 'count']
        
        chart_pie = alt.Chart(status_counts).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="count", type="quantitative"),
            color=alt.Color(field="status", type="nominal", scale=alt.Scale(domain=list(STATUS_COLORS.keys()), range=list(STATUS_COLORS.values()))),
            tooltip=['status', 'count']
        ).properties(height=300)
        st.altair_chart(chart_pie, use_container_width=True)

def show_data(df):
    st.markdown("## 🔎 Detailed Violation Data")
    
    # --- Filters ---
    with st.expander("🛠️ Advanced Filters", expanded=True):
        f_col1, f_col2, f_col3 = st.columns(3)
        
        with f_col1:
            status_filter = st.multiselect("Risk Status", options=['TRIGGER', 'WARNING'], default=['TRIGGER', 'WARNING'])
        
        with f_col2:
            borough_filter = st.multiselect("Borough", options=sorted(df['borough'].dropna().unique()))
            
        with f_col3:
            november_filter = st.checkbox("📅 Active in November (Hackathon Req)", help="Filters vehicles last seen in Nov 2024 or Nov 2025")

    # --- Filtering Logic ---
    filtered_df = df.copy()
    
    if status_filter:
        filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]
        
    if borough_filter:
        filtered_df = filtered_df[filtered_df['borough'].isin(borough_filter)]
        
    if november_filter:
        # Hackathon requirement: "triggered the list in November"
        # We start by looking for any activity in November (Month 11)
        filtered_df = filtered_df[filtered_df['last_violation_12m'].dt.month == 11]

    # --- Display ---
    st.markdown(f"### Showing {len(filtered_df):,} Vehicles")
    
    # Download Button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "⬇️ Download Filtered List",
        csv,
        "isa_eligible_vehicles.csv",
        "text/csv",
        key='download-csv'
    )

    st.dataframe(
        filtered_df[['vehicle_id', 'plate', 'state', 'borough', 'violations_12m', 'total_fines_12m', 'last_violation_12m', 'status']],
        use_container_width=True,
        column_config={
            "vehicle_id": "ID",
            "plate": "Plate",
            "state": "State",
            "borough": "Borough",
            "violations_12m": st.column_config.NumberColumn("Violations (12m)", help="Count in last 12 months"),
            "total_fines_12m": st.column_config.NumberColumn("Fines", format="$%.2f"),
            "last_violation_12m": st.column_config.DatetimeColumn("Last Seen", format="MMM DD, YYYY"),
            "status": st.column_config.TextColumn("Status")
        },
        hide_index=True
    )

def main():
    # Only run set_page_config if this is the main script; 
    # however, st.set_page_config must be the first Streamlit command.
    # Since we are moving this to speedcamera.py, likely it will be called from app.py or run directly.
    # If it's run as a page in a multipage app, set_page_config is good.
    # But if app.py is the entry point, maybe we should be careful. 
    # The original dashboard.py had set_page_config.
    # I'll keep it but wrap it in a try-except or check.
    try:
        st.set_page_config(page_title="NYC Speed Camera Engine", layout="wide", page_icon="🚦")
    except:
        pass

    df = load_data()
    
    if df is None:
        st.error("❌ Data not found. Please run the `data_merge_strategy.py` script first.")
        return

    # Sidebar
    st.sidebar.title("🚦 NYC ISA Pilot")
    
    page = st.sidebar.radio("Navigation", ["Overview", "Violations Data"])
    
    st.sidebar.divider()
    
    # Add Hackathon Context in Sidebar
    st.sidebar.info(
        """
        **Data Lineage:**
        1. **Source**: `speed_cameras_final` (Operational Table)
        2. **Logic**: Merged Ground Truth + County Feeds
        3. **Engine**: Trailing 12-Month Window Aggregation
        
        **Trigger Rule:**
        - **Target**: >= 16 Violations
        - **Window**: Rolling 12 Months
        - **Action**: ISA Installation Order
        """
    )
    
    # As of Date
    if 'as_of_date' in df.columns:
        latest = df['as_of_date'].max()
        st.sidebar.caption(f"📅 Data As Of: {latest.date()}")

    if page == "Overview":
        show_overview(df)
    else:
        show_data(df)

if __name__ == "__main__":
    main()
