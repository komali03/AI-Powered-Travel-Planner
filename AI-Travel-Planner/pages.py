# pages.py - Module for different application pages
import streamlit as st
from datetime import datetime, timedelta

# Import from other modules
from llm_service import generate_travel_recommendations, get_currency_info
from ui import display_travel_results, display_currency_converter
from storage import save_trip_to_history, get_trips_dataframe, get_trip_by_id, delete_trip

# Plan a Trip page
def plan_trip_page():
    # Input form for travel details
    with st.form("travel_form"):
        st.subheader("Enter Your Travel Details")
        
        col1, col2 = st.columns(2)
        with col1:
            source = st.text_input("Source Location", placeholder="e.g., New York")
            travelers = st.number_input("Number of Travelers", min_value=1, max_value=10, value=1)
            preferences = st.multiselect(
                "Travel Preferences", 
                options=["Fastest", "Cheapest", "Most comfortable", "Direct routes", "Eco-friendly", "Luxury"],
                default=["Fastest"]
            )
        
        with col2:
            destination = st.text_input("Destination", placeholder="e.g., Los Angeles")
            travel_date = st.date_input(
                "Travel Date", 
                min_value=datetime.now().date(),
                max_value=datetime.now().date() + timedelta(days=365),
                value=datetime.now().date() + timedelta(days=30)
            )
            budget = st.select_slider(
                "Budget Range",
                options=["Budget", "Moderate", "Luxury"],
                value="Moderate"
            )
        
        submit_button = st.form_submit_button("Find Travel Options")
    
    # Store travel form data in session_state to persist it
    if source:
        st.session_state.source = source
    if destination:
        st.session_state.destination = destination
    st.session_state.travel_date = travel_date.strftime("%Y-%m-%d")
    
    # Processing and displaying results
    if submit_button:
        if source and destination:
            with st.spinner("Planning your travel options..."):
                recommendations = generate_travel_recommendations(
                    source, 
                    destination, 
                    travel_date.strftime("%Y-%m-%d"),
                    str(travelers),
                    ", ".join(preferences),
                    budget,
                    st.session_state.travel_chain
                )
                
                if recommendations:
                    # Store recommendations in session state to persist between page loads
                    st.session_state.current_recommendations = recommendations
                    st.session_state.current_source = source
                    st.session_state.current_destination = destination
                    
                    # Display travel results
                    display_travel_results(recommendations, source, destination)
                    
                    # Add the currency converter
                    currency_data = get_currency_info(destination)
                    display_currency_converter(currency_data)
                    
                    # Save trip button - not inside form to prevent page reload
                    if st.button("Save This Trip to History"):
                        save_trip_to_history(
                            recommendations, 
                            source, 
                            destination, 
                            st.session_state.travel_date
                        )
                        # Don't reload the page after saving
        else:
            st.warning("Please enter both source and destination locations.")
    
    # Display previously generated recommendations if they exist
    elif 'current_recommendations' in st.session_state:
        st.info("Showing your previously generated travel plan. Fill the form and click 'Find Travel Options' to generate a new plan.")
        display_travel_results(
            st.session_state.current_recommendations, 
            st.session_state.current_source, 
            st.session_state.current_destination
        )
        
        # Add the currency converter
        if 'current_destination' in st.session_state:
            currency_data = get_currency_info(st.session_state.current_destination)
            display_currency_converter(currency_data)
        
        # Save trip button
        if st.button("Save This Trip to History"):
            save_trip_to_history(
                st.session_state.current_recommendations, 
                st.session_state.current_source, 
                st.session_state.current_destination, 
                st.session_state.travel_date
            )

# Trip History page
def trip_history_page():
    st.subheader("Your Saved Trips")
    
    # Get trip history as DataFrame
    trip_df = get_trips_dataframe()
    
    if trip_df is None:
        st.info("No trips saved yet. Plan a trip to see it here!")
        return
    
    # Display trip history as a table
    st.dataframe(trip_df, use_container_width=True)
    
    # Create columns for selection and deletion
    col1, col2 = st.columns(2)
    
    with col1:
        # Allow user to select a trip to view details
        trip_ids = [t["id"] for t in st.session_state.trip_history]
        
        if trip_ids:
            selected_trip_id = st.selectbox(
                "Select a trip to view details:", 
                options=trip_ids,
                format_func=lambda x: f"Trip {x}: {next((t['source'] for t in st.session_state.trip_history if t['id'] == x), '')} → {next((t['destination'] for t in st.session_state.trip_history if t['id'] == x), '')}"
            )
            
            # View button
            if st.button("View Selected Trip", key="view_trip_button"):
                selected_trip = get_trip_by_id(selected_trip_id)
                if selected_trip:
                    st.session_state.viewing_trip = selected_trip
    
    with col2:
        # Delete functionality
        if trip_ids:
            delete_trip_id = st.selectbox(
                "Select a trip to delete:", 
                options=trip_ids,
                format_func=lambda x: f"Trip {x}: {next((t['source'] for t in st.session_state.trip_history if t['id'] == x), '')} → {next((t['destination'] for t in st.session_state.trip_history if t['id'] == x), '')}"
            )
            
            # Delete button
            if st.button("Delete Selected Trip", key="delete_trip_button"):
                delete_trip(delete_trip_id)
                st.experimental_rerun()
    
    # Display the selected trip if it exists in session state
    if 'viewing_trip' in st.session_state and st.session_state.viewing_trip:
        trip = st.session_state.viewing_trip
        
        st.subheader(f"Trip Details: {trip['source']} → {trip['destination']}")
        st.markdown(f"**Date:** {trip['date']}")
        
        # Display trip data
        display_travel_results(trip["full_data"], trip["source"], trip["destination"])
        
        # Add currency converter
        currency_data = get_currency_info(trip["destination"])
        display_currency_converter(currency_data)
        
        # Button to clear viewing state
        if st.button("Close Trip Details", key="close_trip_details"):
            del st.session_state.viewing_trip
            st.experimental_rerun()

# About page
def about_page():
    st.subheader("About AI Travel Planner Pro")
    st.markdown("""
    ### How it works
    This AI-powered travel planner uses Google's Generative AI to provide you with comprehensive 
    travel options between any two locations. It analyzes various transportation modes including 
    flights, trains, buses, and cabs to help you make an informed decision.
    
    ### Features
    - **Multiple Transportation Options**: Compare flights, trains, buses, and cabs
    - **Destination Information**: Weather forecasts, attractions, and local transport details
    - **Cost Comparisons**: Visual price comparison between different travel methods
    - **Trip History**: Save and review your planned trips
    - **Packing Suggestions**: Get customized packing recommendations based on your destination
    - **Currency Conversion**: Quick currency reference for your destination
    
    ### Privacy
    We do not store your travel plans on our servers. All saved trips are stored locally in your browser's session.
    """)
    
    # Version information
    st.markdown("---")
    st.caption("AI Travel Planner Pro v1.0.0")
    st.caption("Built with Streamlit, LangChain, and Google GenAI")
