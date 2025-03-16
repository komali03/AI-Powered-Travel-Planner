# Install necessary packages
# pip install langchain-google-genai streamlit python-dotenv
# import streamlit for ease of making application, os module for environment variables, load_dotenv for loading environment variables, ChatPromptTemplate for defining the chat prompt, ChatGoogleGenerativeAI for invoking the Google Generative AI model, StrOutputParser for parsing the output, and dotenv for loading environment variables.
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()
# fetch API key from .env file
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Ensure API key is available
if not GOOGLE_API_KEY:
    st.error("API Key not found! Please check your .env file.")

# Define the Chat Prompt
chat_template = ChatPromptTemplate.from_messages(
    [("system","""You are an AI-powered travel cost estimator that helps users plan their trips by providing estimated travel costs for different transportation options. Your goal is to generate cost estimates for various travel modes (flight, train, bus, cab, etc.) based on the user's input. User Input contains Source location (e.g., city, airport, or station), Destination location, Preferred travel date (if provided, consider seasonal variations in pricing and let them know if its peak season or not and reason too), Travel preferences (if any, such as economy vs. premium travel) Your Response Output must contain List of available travel modes (e.g., flight, train, bus, cab, ferry, etc.), Estimated cost range for each mode (low, average, high), Estimated travel time for each mode, Additional details (e.g., fastest route, most budget-friendly option).Rules you must follow are: Fetch real-time or historical cost data from APIs (if available) or use average cost estimates.If data is unavailable for a specific travel mode, indicate so rather than making arbitrary guesses. Also, suggest if any nice places to visit in {destination} and suggest the websites links and apps user can use to book those tickets. Also give seating/sleeper and AC/NAC and corresponding prices if yu can."""),
    ("human",""" Help me plan my trip and book a ticket from {source} to {destination} on {date_of_travel} within {budget_range} with respect to {additional_info}.    """)]
)

# Initialize the Chat Model
chat_model = ChatGoogleGenerativeAI(
    google_api_key=GOOGLE_API_KEY,
    model="gemini-2.0-flash-exp",
    temperature=0.2
)

# Initialize the Output Parser
parser = StrOutputParser()

# Define the Processing Chain
chain = chat_template | chat_model | parser

# Streamlit UI
st.title("AI Powered Travel Planner")

# User Inputs
source = st.text_input('Source Location*')
destination = st.text_input('Destination*')
date_of_travel = st.date_input('Traveling Date')

# Set a Budget Range
budget_range = st.slider(
    "Select your budget range (in ₹)", 
    min_value=100, 
    max_value=100000, 
    value=(100, 100000),  # Default range
    step=50
)
st.write(f"Selected budget range: ₹{budget_range[0]} - ₹{budget_range[1]}")
additional_info = st.text_area("Additional Information (if any specifications or queries)")
# Button Click
btn_click = st.button("Plan My Trip")

if btn_click:
    if not source or not destination:
        st.warning("Please enter both source and destination.")
    else:
        # Create Input Dictionary
        raw_input = {
            "source": source,
            "destination": destination,
            "date_of_travel": str(date_of_travel),  # Convert to string
            "budget_range": f"₹{budget_range[0]} to ₹{budget_range[1]}",
            "additional_info": additional_info
        }
        
        # Invoke Model and Display Response
        response=chain.invoke(raw_input)
        st.write(response)
        

