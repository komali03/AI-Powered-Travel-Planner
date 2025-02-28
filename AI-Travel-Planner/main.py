# main.py - Main application file
import streamlit as st
from dotenv import load_dotenv
import os

# Import modules
from llm_service import initialize_llm, setup_langchain
from ui import display_header, create_sidebar_navigation
from pages import plan_trip_page, trip_history_page, about_page
from storage import init_trip_history

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Page configuration
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)

def main():
    # Initialize session state
    init_trip_history()
    
    # App header with logo
    display_header()
    
    # Create sidebar for navigation
    page = create_sidebar_navigation()
    
    # Initialize session state for the travel chain
    if 'travel_chain' not in st.session_state:
        st.session_state.travel_chain = setup_langchain()
    
    # Check if chain was initialized successfully
    if not st.session_state.travel_chain and page != "About":
        st.error("Failed to initialize the AI model. Please check your API key.")
        st.stop()
    
    # Page router
    if page == "Plan a Trip":
        plan_trip_page()
    elif page == "Trip History":
        trip_history_page()
    else:  # About page
        about_page()

if __name__ == "__main__":
    main()
