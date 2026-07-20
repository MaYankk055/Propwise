# Propwise

ML based project for Indian real estate price prediction and market analytics.

## Features
- AI price prediction across multiple Indian cities and localities
- Market dashboard with city stats, price/sqft charts, and data tables
- City comparison and market heatmap views
- Price trend analysis and ROI calculator
- Live real estate news feed and model insights

## Quick Start
```bash
pip install -r requirements.txt
python backend/data/generate_dataset.py
python backend/train_model.py
python backend/app.py
# → http://localhost:5001
```

## Tech Stack
Python · Pandas · Scikit-learn · Flask · Chart.js · HTML/CSS/JS

## 🚀 Deploy Live on Render (Docker)
1. Push this repository to GitHub.
2. Create a new **Web Service** on [Render](https://render.com) and connect your GitHub repository.
3. Configure the following settings:
   - **Runtime / Environment**: `Docker` (Render will automatically detect the included `Dockerfile`)
   - **Branch**: `main`
4. Add environment variables (Optional):
   - `NEWS_API_KEY`: Add this if you want live real estate news to work.
   - *Note: Port handling (5001) is managed automatically by the Dockerfile and Render.*
5. Click **Deploy** (or **Manual Deploy** -> **Deploy latest commit**).
6. Once the build is complete and the service is live, click on the generated public URL (e.g., `https://propwise-1.onrender.com`) to view the application!

---

## 📝 Project Summary 

### 🚀 The Elevator Pitch (What is it?)
**Propwise** is a comprehensive Machine Learning based platform designed for Indian real estate market analytics and price prediction. It provides users with AI-driven property valuations, comparative market dashboards, ROI calculators, and live industry news.

### 🛠️ Tech Stack & Frameworks
- **Programming Languages:** Python, JavaScript, HTML5, CSS3
- **Web Framework:** Flask (Python) with Waitress as a production-grade WSGI server
- **Frontend Libraries:** Chart.js (for dynamic, interactive data visualization), Jinja2 (Flask Templating)
- **Deployment & DevOps:** Docker, Render Platform (PaaS)
- **External Integrations:** RESTful News APIs for live market updates (with intelligent JSON-based caching to reduce API calls)

### 🧠 Machine Learning & Data Science
- **Libraries Used:** Scikit-learn, Pandas, NumPy, Matplotlib, Seaborn, Joblib
- **Algorithms Evaluated:**
  1. **Linear Regression:** Baseline model for linear relationships.
  2. **Random Forest Regressor:** Ensemble learning method using 300 decision trees to capture non-linear patterns and interactions.
  3. **Gradient Boosting Regressor:** Sequential ensemble method using 500 estimators with depth 5, optimized via learning rate tuning.
- **Model Selection:** The pipeline automatically trains, evaluates, and dynamically selects the best performing model based on the highest **R² (R-squared) score**.
- **Evaluation Metrics:**
  - **R² (R-Squared):** Measures the proportion of variance in the dependent variable explained by the model.
  - **MAE (Mean Absolute Error):** Measures the average magnitude of the errors in predictions.
  - **RMSE (Root Mean Squared Error):** Penalizes larger errors more heavily.
  - **MAPE (Mean Absolute Percentage Error):** Presents the error as a percentage for easier business interpretation.

### 📊 Data Engineering & Feature Engineering
- **Categorical Encoding:** Applied **Label Encoding** to transform textual categorical variables (City, Locality, State, Property Type, Furnishing, Floor) into machine-readable numeric formats.
- **Derived Features (Feature Engineering):** Created custom features to boost model performance:
  - `price_per_sqft`: Baseline price metric.
  - `room_ratio`: Bathrooms divided by bedrooms to assess layout practicality.
  - `is_new`: Binary flag for properties ≤ 3 years old.
  - `is_luxury`: Binary flag triggered if the amenities count is ≥ 10.
  - `bhk_area`: Interaction feature (bedrooms × area).
- **Exploratory Data Analysis (EDA):** Generated automated visualizations (Correlation Heatmaps, Price Distributions, Feature Importance) using Matplotlib and Seaborn, saving them dynamically as static assets.

### 💡 Key Features
1. **AI Price Prediction Engine:** Predicts property prices with confidence intervals (low/high estimates) based on the model's MAPE, plus computes an "Investment Score".
2. **Interactive Market Dashboard:** Real-time visual comparison of top cities, price trends across tiers, and property types using Chart.js.
3. **Advanced ROI Calculator:** Calculates future property value, capital gains, rental income, and monthly EMI incorporating interest rates and historic city-specific YoY growth rates.
4. **Live News & Caching:** Built a robust data pipeline that fetches live real estate news from external APIs, normalizes the data, categorizes it (e.g., Policy, Market Data, Investment), and caches it locally (TTL system) to optimize performance and rate limits.
5. **Production Ready:** Fully containerized with a `Dockerfile` and `render.yaml` for scalable cloud deployment.
