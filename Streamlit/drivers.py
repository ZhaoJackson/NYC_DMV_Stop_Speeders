import streamlit as st
import pandas as pd
import altair as alt

# --- Constants ---
BOROUGH_MAP = {
    "BK": "Brooklyn",
    "BX": "Bronx",
    "QN": "Queens",
    "MN": "Manhattan",
    "NY": "Manhattan", 
    "ST": "Staten Island",
    "SI": "Staten Island",
    "Kings": "Brooklyn",
    "Bronx": "Bronx",
    "Queens": "Queens",
    "New York": "Manhattan",
    "Richmond": "Staten Island"
    # 'Other' remains 'Other' or mapped if known
}

@st.cache_data
def load_data():
    path = "data/exports/nyc_speeding_violations_over_18_months.csv"
    try:
        df = pd.read_csv(path)
        # Normalize county names
        df['borough'] = df['county'].map(BOROUGH_MAP).fillna(df['county'])
        return df
    except FileNotFoundError:
        try:
             # Try going up one level if run from subdir
             path = "../data/exports/nyc_speeding_violations_over_18_months.csv"
             df = pd.read_csv(path)
             df['borough'] = df['county'].map(BOROUGH_MAP).fillna(df['county'])
             return df
        except:
            return None

def show_overview(df):
    st.markdown("## 🆔 Driver License Monitoring")
    st.caption("Monitoring Pilot for Persistent Violators (11+ Points in 18 Months)")
    
    st.divider()

    # --- KPIs ---
    st.markdown("#### 📊 Operational Metrics (Trailing 18-Months)")
    col1, col2, col3 = st.columns(3)
    
    total_drivers = len(df)
    total_points = df['points'].sum()
    avg_points = df['points'].mean()
    
    col1.metric(
        "🚨 Mandate Triggers", 
        f"{total_drivers:,}", 
        "11+ Points / 18mo", 
        delta_color="inverse", 
        help="Drivers with >= 11 points in the trailing 18 months. Mandatory ISA installation required."
    )
    col2.metric("💯 Total Points Accrued", f"{total_points:,}", "High-Risk Pool")
    col3.metric("📈 Avg Points / Driver", f"{avg_points:.1f}", "Severity Indicator")
    
    st.divider()
    
    # --- Charts ---
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("📍 Triggers by Borough")
        # clean up borough for chart
        boro_counts = df.groupby('borough')['points'].sum().reset_index()
        
        chart_boro = alt.Chart(boro_counts).mark_bar().encode(
            x=alt.X('points', title='Accumulated Points'),
            y=alt.Y('borough', sort='-x', title='Borough/County'),
            color=alt.Color('borough', legend=None),
            tooltip=['borough', 'points']
        ).properties(height=300)
        st.altair_chart(chart_boro, use_container_width=True)

    with c2:
        st.subheader("📉 Points Distribution")
        chart_hist = alt.Chart(df).mark_bar().encode(
            x=alt.X("points", bin=True, title="Points Range"),
            y=alt.Y("count()", title="Number of Drivers"),
            tooltip=['count()']
        ).properties(height=300)
        st.altair_chart(chart_hist, use_container_width=True)

def main():
    try:
        st.set_page_config(page_title="NYC Driver Points Engine", layout="wide", page_icon="🆔")
    except:
        pass

    df = load_data()
    
    if df is None:
        st.error("❌ Data not found. Please run the `notebooks/sql/Data_violation.py` ETL script first.")
        return

    # Sidebar
    st.sidebar.title("🆔 Driver ISA Logic")
    st.sidebar.info(
        """
        **Data Lineage:**
        1. **Source**: `traffic_violations_final`
        2. **Logic**: Consolidated Driver History
        3. **Engine**: 18-Month Rolling Window
        
        **Trigger Rule:**
        - **Target**: >= 11 Points
        - **Window**: Rolling 18 Months
        - **Action**: ISA Installation Order
        """
    )

    st.sidebar.divider()
    
    # Navigation logic if needed locally, but likely main app controls it
    # We will just show everything in one vertically scrolling page for simplicity or tabs
    
    tab1, tab2 = st.tabs(["Overview", "Detailed List"])
    
    with tab1:
        show_overview(df)
        
    with tab2:
        st.markdown("### 📋 Mandate Trigger List")
        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                "license_id": "License ID",
                "county": "County (Raw)",
                "points": st.column_config.ProgressColumn(
                    "Points", 
                    help="Accumulated Points", 
                    format="%d", 
                    min_value=0, 
                    max_value=int(df['points'].max())
                ),
                "borough": "Borough (Mapped)"
            },
            hide_index=True
        )
        
        # Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "⬇️ Download Trigger List",
            csv,
            "isa_driver_triggers.csv",
            "text/csv",
            key='download-drivers'
        )

if __name__ == "__main__":
    main()
