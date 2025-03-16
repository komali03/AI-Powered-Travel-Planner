### **📌 AI Powered Travel Planner**
🚀 **AI-Powered Travel Cost Estimator & Planner** using **Streamlit, LangChain, and Google Generative AI**  

---

## **🌍 About the Project**
This AI-powered travel planner estimates travel costs, suggests booking platforms, and provides insights into budget-friendly, fastest, and available travel modes. It also considers **seasonal variations** and **popular attractions** at the destination.

🔹 **Core Features:**  
✔️ Estimate travel costs for multiple transport modes (flight, train, bus, cab, ferry)  
✔️ Suggests **booking websites & apps**  
✔️ Provides real-time/historical price range estimates  
✔️ Checks **seasonal variations (peak/off-season)** and gives reasons  
✔️ Recommends **popular places** to visit at the destination  
✔️ Supports **seating options (AC/Non-AC, Sleeper, Economy, Premium)**  

---

## **⚙️ Tech Stack**
- **Python** 🐍
- **Streamlit** (for UI)
- **LangChain** (for structured AI interactions)
- **Google Generative AI (Gemini-2.0)** 🔥
- **dotenv** (for secure API key management)

---

## **📥 Installation & Setup**
### **🔹 Step 1: Clone the Repository**
```sh
git clone https://github.com/komali-03/AI-Travel-Planner.git
cd AI-Travel-Planner
```

### **🔹 Step 2: Create a Virtual Environment**
```sh
python -m venv venv
```
Activate it:  
- **Windows (PowerShell):**  
  ```sh
  venv\Scripts\activate
  ```
- **Mac/Linux:**  
  ```sh
  source venv/bin/activate
  ```

### **🔹 Step 3: Install Dependencies**
```sh
pip install -r requirements.txt
```

### **🔹 Step 4: Set Up API Key**
1. Create a `.env` file inside the project directory  
2. Add your **Google Generative AI Key**  
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

### **🔹 Step 5: Run the Application**
```sh
streamlit run app.py
```
---

## **📌 Example Usage**
1️⃣ Enter **Source & Destination**  
2️⃣ Select a **Budget Range**  
3️⃣ Enter **Travel Date** & **Additional Preferences**  
4️⃣ Click **"Plan My Trip"** to get AI-generated travel insights  

---

## **🛠 Dependencies**
Your **`requirements.txt`** should include:
```txt
streamlit
google-generativeai
langchain
langchain-google-genai
python-dotenv
```

---

## **🛠 Troubleshooting**
- **Issue:** `ModuleNotFoundError: No module named 'streamlit'`  
  ✅ **Solution:** Run `pip install streamlit`
  
- **Issue:** `No module named 'langchain_google_genai'`  
  ✅ **Solution:** Run `pip install langchain-google-genai`

- **Issue:** `.env file API key not found`  
  ✅ **Solution:** Ensure your `.env` file exists with the correct API key.

---

## **📌 Contributing**
🙌 Feel free to **fork** this repo, create a **feature branch**, and submit a **pull request**. Contributions are welcome! 🎉

---

## **📄 License**
MIT License. Feel free to modify and use it. 🚀

---

## **📞 Contact**
🔹 **GitHub:** [https://github.com/komali-03]  
🔹 **LinkedIn:** [https://www.linkedin.com/in/radha-komalidevi-m-11280722b/]  
🔹 **Email:** [mrkomalidevi03@gmail.com]

---

🚀 **Enjoy AI-powered travel planning!** ✈️ 🚆 🚗
