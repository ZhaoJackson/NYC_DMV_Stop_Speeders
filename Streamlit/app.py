import streamlit as st
import overview
import speedcamera
import drivers
import chatbot

# Set page config at the very top level
st.set_page_config(page_title="NYC Safe Streets", layout="wide", page_icon="🚦")

def main():
    st.sidebar.title("Navigation")
    
    # Navigation selection
    page = st.sidebar.radio(
        "Go to",
        ["🏠 Project Overview", "🚦 Speed Camera Dashboard", "🆔 Driver Points Dashboard", "🤖 AI Assistant"]
    )
    
    st.sidebar.divider()
    st.sidebar.markdown("### Families for Safe Streets - DSSG NYC")
    
    if page == "🏠 Project Overview":
        overview.main()
    elif page == "🚦 Speed Camera Dashboard":
        speedcamera.main()
    elif page == "🆔 Driver Points Dashboard":
        drivers.main()
    elif page == "🤖 AI Assistant":
        chatbot.main()

if __name__ == "__main__":
    main()