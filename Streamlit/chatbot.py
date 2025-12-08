import streamlit as st
import os
import prompt
from openai import AzureOpenAI

# Load environment variables (Streamlit secrets should handle this in prod, but we use .env locally)
from dotenv import load_dotenv
load_dotenv()

def get_azure_client():
    """Initializes and returns the Azure OpenAI client."""
    api_key = os.getenv("AZURE_OPENAI_4O_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_4O_ENDPOINT")
    api_version = os.getenv("AZURE_OPENAI_4O_API_VERSION", "2024-02-15-preview")

    if not api_key or not endpoint:
        st.error("❌ Azure API Key or Endpoint not found. Please check your .env or secrets.")
        return None

    return AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=endpoint
    )

def main():
    st.title("🤖 ISA Program AI Assistant")
    st.caption("Ask questions about the speeding violation dataset and ISA triggers.")

    # 1. Load Data
    df = prompt.load_data()
    if df is None:
        st.error("Could not load dataset. Please ensure `data/exports/vehicle_speed_summary.csv` exists.")
        return

    # 2. Add Sidebar info
    st.sidebar.success(f"Context Loaded: {len(df)} vehicle records")
    st.sidebar.markdown("""
    **Sample Questions:**
    - "How many vehicles have triggered the ISA threshold?"
    - "Which borough has the highest number of high-risk drivers?"
    - "Draft a warning email for vehicles with 15 violations."
    """)

    # 3. Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 4. Display Chat Messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 5. Handle User Input
    if question := st.chat_input("Ask about the data..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        # Generate Prompt
        system_prompt = prompt.generate_prompt(question, df)
        
        # Call Azure OpenAI
        client = get_azure_client()
        deployment_name = os.getenv("AZURE_OPENAI_4O_DEPLOYMENT", "gpt-4o")

        if client:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                try:
                    response = client.chat.completions.create(
                        model=deployment_name,
                        messages=[
                            {"role": "system", "content": "You are a helpful data assistant for the NYC Safe Streets program."},
                            {"role": "user", "content": system_prompt}
                        ],
                        stream=True
                    )
                    
                    for chunk in response:
                        if chunk.choices:
                            delta = chunk.choices[0].delta.content
                            if delta:
                                full_response += delta
                                message_placeholder.markdown(full_response + "▌")
                                
                    message_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
                except Exception as e:
                    st.error(f"Error communicating with AI: {e}")

if __name__ == "__main__":
    main()
