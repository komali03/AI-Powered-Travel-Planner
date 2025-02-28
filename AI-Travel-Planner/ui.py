# ui.py - Module for UI components and display functions
import streamlit as st
import pandas as pd
import plotly.express as px

# Display app header
def display_header():
    st.title("✈️ AI Travel Planner Pro")
    st.markdown("Plan your perfect journey with AI-powered recommendations")

# Create navigation sidebar
def create_sidebar_navigation():
    with st.sidebar:
        st.header("Navigation")
        return st.radio("Choose a page:", ["Plan a Trip", "Trip History", "About"])

# Function to display travel options as a table
def display_travel_options(options, option_type):
    if not options:
        st.write("No options available.")
        return
    
    df = pd.DataFrame(options)
    st.dataframe(df, use_container_width=True)

# Function to create a price comparison chart
def create_price_comparison(data):
    # Extract lowest price from each category
    price_data = []
    
    for category in ["flights", "trains", "buses", "cabs"]:
        if category in data["travel_options"] and data["travel_options"][category]:
            # Extract numeric price from the first option
            first_option = data["travel_options"][category][0]
            price_text = first_option.get("cost", "0")
            
            # Try to extract a numeric value from the price text
            try:
                # Handle price ranges by taking the lower value
                if "-" in price_text:
                    price_text = price_text.split("-")[0]
                
                # Remove currency symbols and commas
                price_text = ''.join(c for c in price_text if c.isdigit() or c == '.')
                price = float(price_text) if price_text else 0
            except:
                price = 0
                
            price_data.append({"Transportation": category.capitalize(), "Estimated Cost": price})
    
    if price_data:
        df = pd.DataFrame(price_data)
        fig = px.bar(df, x="Transportation", y="Estimated Cost", title="Price Comparison by Transportation Method")
        st.plotly_chart(fig, use_container_width=True)

# Function to display packing suggestions based on destination and weather
def display_packing_suggestions(destination, weather):
    st.subheader("Packing Suggestions")
    
    # Initialize packing list in session state if it doesn't exist
    if "packing_list" not in st.session_state:
        st.session_state.packing_list = {}
    
    # Basic items everyone needs
    basic_items = [
        "Passport/ID", 
        "Phone & charger", 
        "Wallet & credit cards",
        "Medication (if needed)",
        "Toiletries"
    ]
    
    # Weather-based suggestions
    weather_items = []
    if "rain" in weather.lower() or "shower" in weather.lower():
        weather_items.extend(["Umbrella", "Waterproof jacket", "Waterproof shoes"])
    if "hot" in weather.lower() or "warm" in weather.lower() or "sunny" in weather.lower():
        weather_items.extend(["Sunscreen", "Sunglasses", "Hat", "Light clothing", "Water bottle"])
    if "cold" in weather.lower() or "cool" in weather.lower() or "snow" in weather.lower():
        weather_items.extend(["Warm jacket", "Gloves", "Scarf", "Boots", "Thermal layers"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("Essential Items:")
        for item in basic_items:
            # Create a unique key for each checkbox
            key = f"basic_{destination}_{item}"
            # Initialize the item in session state if it doesn't exist
            if key not in st.session_state.packing_list:
                st.session_state.packing_list[key] = False
            
            # Display the checkbox and update state when changed
            checked = st.checkbox(item, value=st.session_state.packing_list[key], key=key)
            st.session_state.packing_list[key] = checked
    
    with col2:
        st.write("Weather-Appropriate Items:")
        for item in weather_items:
            # Create a unique key for each checkbox
            key = f"weather_{destination}_{item}"
            # Initialize the item in session state if it doesn't exist
            if key not in st.session_state.packing_list:
                st.session_state.packing_list[key] = False
            
            # Display the checkbox and update state when changed
            checked = st.checkbox(item, value=st.session_state.packing_list[key], key=key)
            st.session_state.packing_list[key] = checked

# Function to display currency conversion UI
def display_currency_converter(currency_data):
    st.subheader("Currency Converter")
    
    if currency_data:
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"Local currency: {currency_data['local_currency']}")
            st.info(f"Exchange rate: {currency_data['exchange_rate']}")
        
        with col2:
            amount = st.number_input("Amount to convert (USD)", min_value=0.0, value=100.0, step=10.0)
            
            # Extract conversion rate
            rate_text = currency_data['exchange_rate'].split('=')[1].strip()
            rate_value = float(''.join(c for c in rate_text if c.isdigit() or c == '.'))
            
            converted = amount * rate_value
            st.success(f"${amount:.2f} USD = {converted:.2f} {currency_data['local_currency'].split('(')[1].split(')')[0]}")
    else:
        st.warning("Currency information unavailable")

# Main function to display the travel results
def display_travel_results(data, source, destination):
    if not data:
        return
    
    # Create tabs for different sections
    tabs = st.tabs(["Travel Options", "Destination Info", "Comparison", "Packing List"])
    
    with tabs[0]:
        st.subheader("Recommended Option")
        st.info(data["recommendation"])
        
        # Display each travel option in expandable sections
        for option_type in ["flights", "trains", "buses", "cabs"]:
            with st.expander(f"{option_type.capitalize()} Options", expanded=(option_type == "flights")):
                if option_type in data["travel_options"] and data["travel_options"][option_type]:
                    display_travel_options(data["travel_options"][option_type], option_type)
                else:
                    st.write("No options available.")
    
    with tabs[1]:
        # Display destination information
        dest_info = data["destination_info"]
        
        # Weather information
        st.subheader("Weather Forecast")
        st.info(dest_info["weather"])
        
        # Attractions
        st.subheader("Top Attractions")
        for idx, attraction in enumerate(dest_info["attractions"], 1):
            st.write(f"{idx}. {attraction}")
        
        # Accommodations
        st.subheader("Accommodation Options")
        if dest_info["accommodations"]:
            st.dataframe(pd.DataFrame(dest_info["accommodations"]), use_container_width=True)
        
        # Local transport
        st.subheader("Local Transportation")
        for transport in dest_info["local_transport"]:
            st.write(f"• {transport}")
        
        # The currency converter will be added in the page module
    
    with tabs[2]:
        # Price comparison chart
        st.subheader("Price Comparison")
        create_price_comparison(data)
        
        # Total cost estimate
        st.subheader("Estimated Total Trip Cost")
        st.info(f"**{data['estimated_total_cost']}**")
    
    with tabs[3]:
        # Packing suggestions
        display_packing_suggestions(destination, data["destination_info"]["weather"])
