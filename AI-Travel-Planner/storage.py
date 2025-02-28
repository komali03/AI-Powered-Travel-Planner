# storage.py - Module for data storage and history management
import streamlit as st
import pandas as pd

# Initialize session state for trip history if it doesn't exist
def init_trip_history():
    if "trip_history" not in st.session_state:
        st.session_state.trip_history = []

# Function to save trip to history
def save_trip_to_history(trip_data, source, destination, travel_date):
    # Initialize trip history if it doesn't exist
    init_trip_history()
    
    # Generate a unique ID (use length + 1 or timestamp)
    if st.session_state.trip_history:
        new_id = max(trip["id"] for trip in st.session_state.trip_history) + 1
    else:
        new_id = 1
    
    # Create a trip summary
    trip_summary = {
        "id": new_id,
        "source": source,
        "destination": destination,
        "date": travel_date,
        "recommendation": trip_data.get("recommendation", "N/A"),
        "estimated_cost": trip_data.get("estimated_total_cost", "N/A"),
        "full_data": trip_data
    }
    
    # Append the new trip to session state
    st.session_state.trip_history.append(trip_summary)
    st.success("Trip saved to history!")
    return trip_summary["id"]

# Function to get all saved trips
def get_all_trips():
    init_trip_history()
    return st.session_state.trip_history

# Function to get a specific trip by ID
def get_trip_by_id(trip_id):
    init_trip_history()
    return next((t for t in st.session_state.trip_history if t["id"] == trip_id), None)

# Function to delete a trip by ID
def delete_trip(trip_id):
    init_trip_history()
    st.session_state.trip_history = [t for t in st.session_state.trip_history if t["id"] != trip_id]
    st.success(f"Trip {trip_id} deleted successfully!")

# Function to get trips as DataFrame for display
def get_trips_dataframe():
    trips = get_all_trips()
    
    if not trips:
        return None
        
    return pd.DataFrame([
        {"ID": t["id"], 
         "From": t["source"], 
         "To": t["destination"], 
         "Date": t["date"],
         "Recommended": t["recommendation"].split(".")[0] if "." in t["recommendation"] else t["recommendation"][:50],
         "Est. Cost": t["estimated_cost"]
        } for t in trips
    ])
