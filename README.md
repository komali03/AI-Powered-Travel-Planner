AI Travel Planner Pro
An AI-powered travel planning application designed to assist users in finding optimal travel options between a given source and destination. The system leverages LangChain and Google GenAI to process user inputs and generate various travel choices such as flights, trains, buses, and cabs, along with comprehensive trip information.

Features
Multiple Transportation Options: Compare flights, trains, buses, and cabs with their estimated costs
Destination Information: Weather forecasts, attractions, and local transport details
Cost Comparisons: Visual price comparison between different travel methods
Trip History: Save and review your planned trips
Packing Suggestions: Get customized packing recommendations based on your destination
Currency Conversion: Quick currency reference for your destination
Project Structure
ai-travel-planner/
├── main.py              # Main application file
├── llm_service.py       # AI models and prompts
├── ui.py                # User interface components
├── storage.py           # Data storage management
├── pages.py             # Application pages
├── requirements.txt     # Dependencies
├── .env.example         # Environment variables template
└── README.md            # Project documentation
Setup Instructions
Clone the repository:

git clone https://github.com/komali03/AI-Powered-Travel-Planner.git
cd ai-travel-planner
Install dependencies:

pip install -r requirements.txt
Set up environment variables:

Copy .env.example to .env
Add your Google API key to the .env file
Run the application:

streamlit run main.py
Usage
Navigate to the "Plan a Trip" page
Enter your source and destination
Select travel date, number of travelers, and preferences
Click "Find Travel Options" to get AI-generated recommendations
Explore the different tabs to view comprehensive trip information
Save interesting trips to your history for future reference
Dependencies
Streamlit: Web application framework
LangChain: Framework for LLM applications
Google GenAI: AI model for generating travel recommendations
Pandas: Data manipulation and analysis
Plotly: Interactive visualizations
Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

AI-Powered-Travel-Planner/AI-Travel-Planner/README.md at main · komali03/AI-Powered-Travel-Planner
