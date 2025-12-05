import streamlit as st
from ..config import DATA_PROCESSED

def run_dashboard():
    st.title("Super Speeders Dashboard")
    st.write("Data processed location:", DATA_PROCESSED)
    # TODO: Load and display data
    st.write("Dashboard placeholder")

if __name__ == "__main__":
    run_dashboard()
