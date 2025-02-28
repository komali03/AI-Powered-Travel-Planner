# llm_service.py - Module for AI model and prompt management
import os
import json
import streamlit as st
from datetime import datetime
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.llms import GoogleGenerativeAI

# Initialize the Google GenAI LLM
def initialize_llm():
    try:
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            st.error("Google API key not found. Please check your .env file.")
            return None
            
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=google_api_key,
            temperature=0.2,
            top_p=0.85,
            max_output_tokens=2048
        )
        return llm
    except Exception as e:
        st.error(f"Error initializing LLM: {e}")
        return None

# Define the prompt template for travel planning
def get_travel_prompt_template():
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    template = """
    You are a knowledgeable travel assistant that provides accurate and helpful travel information.
    
    Based on the following details, provide detailed travel options with estimated costs:
    
    Source: {source}
    Destination: {destination}
    Travel Date: {travel_date}
    Travelers: {travelers}
    Preferences: {preferences}
    Budget Range: {budget}
    
    For each of the following transportation modes, provide available options, travel time, and estimated cost ranges:
    1. Flights
    2. Trains
    3. Buses
    4. Cabs/Taxis
    
    Additionally, provide:
    - Brief weather information for the destination on the travel date
    - Top 3 attractions at the destination
    - 2-3 accommodation options within the specified budget
    - Local transportation options at the destination
    
    Format your response as a properly formatted JSON object with the following structure:
    {{
        "travel_options": {{
            "flights": [
                {{ "name": "Airline name", "departure": "time", "arrival": "time", "duration": "hours", "cost": "price range", "notes": "any additional info" }}
            ],
            "trains": [...],
            "buses": [...],
            "cabs": [...]
        }},
        "destination_info": {{
            "weather": "weather description",
            "attractions": ["attraction1", "attraction2", "attraction3"],
            "accommodations": [
                {{ "name": "hotel name", "type": "hotel/hostel/etc", "cost_per_night": "price", "location": "area" }}
            ],
            "local_transport": ["option1", "option2"]
        }},
        "recommendation": "your brief recommendation on best travel option",
        "estimated_total_cost": "estimated range for travel + 3 days accommodation"
    }}
    
    Only respond with a valid JSON. Do not include any other text, explanations, or invalid characters.
    """
    
    return PromptTemplate(
        input_variables=["source", "destination", "travel_date", "travelers", "preferences", "budget"],
        template=template
    )

# Setup the LangChain with Google GenAI
def setup_langchain():
    llm = initialize_llm()
    
    if llm:
        prompt_template = get_travel_prompt_template()
        chain = LLMChain(
            llm=llm,
            prompt=prompt_template,
            verbose=False
        )
        return chain
    return None

# Generate travel recommendations
def generate_travel_recommendations(source, destination, travel_date, travelers, preferences, budget, chain):
    try:
        if not source or not destination:
            return None
        
        response = chain.run({
            "source": source,
            "destination": destination,
            "travel_date": travel_date,
            "travelers": travelers,
            "preferences": preferences,
            "budget": budget
        })
        
        # Clean the response if it contains markdown code blocks
        if response.startswith("```json"):
            # Remove the ```json at the beginning and ``` at the end
            cleaned_response = response.replace("```json", "", 1)
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            # Trim whitespace
            cleaned_response = cleaned_response.strip()
        else:
            cleaned_response = response
            
        # Parse JSON response
        return json.loads(cleaned_response)
    except Exception as e:
        st.error(f"An error occurred while generating recommendations: {e}")
        st.error(f"Response received: {response if 'response' in locals() else 'No response'}")
        return None

# Currency converter function
def get_currency_info(destination):
    # Simple currency conversion prompt
    currency_prompt = f"""
    Provide the current currency used in {destination} and the approximate exchange rate from USD.
    Format as JSON: {{"local_currency": "Currency Name (CODE)", "exchange_rate": "1 USD = X Local Currency"}}
    """
    
    try:
        llm = initialize_llm()
        if llm:
            currency_info = llm.invoke(currency_prompt).content
            
            # Clean the response if it contains markdown code blocks
            if currency_info.strip().startswith("```"):
                # Find the position of the first and last backticks
                start_pos = currency_info.find("{")
                end_pos = currency_info.rfind("}")
                
                if start_pos != -1 and end_pos != -1:
                    # Extract just the JSON part
                    cleaned_info = currency_info[start_pos:end_pos+1]
                else:
                    # Try removing markdown formatting
                    cleaned_info = currency_info.replace("```json", "").replace("```", "").strip()
            else:
                cleaned_info = currency_info
                
            # Parse JSON response
            return json.loads(cleaned_info)
    except Exception as e:
        st.warning(f"Could not load currency information: {e}")
        st.warning(f"Response received: {currency_info if 'currency_info' in locals() else 'No response'}")
        return None
