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

1. **Core Technologies**
   - Python
   - Pandas
   - Scikit-learn
   - Flask
   - Chart.js
   - HTML/CSS/JavaScript

---

## 🚀 Elevator Pitch (What is it?)

1. **About Propwise**
   - Propwise is a comprehensive Machine Learning platform for Indian real estate market analytics and price prediction.
   - It offers AI-driven property valuations, comparative market dashboards, ROI calculators, and live industry news.

---

## 🛠️ Tech Stack & Frameworks

1. **Programming Languages**
   - Python
   - JavaScript
   - HTML5
   - CSS3

2. **Web Framework**
   - Flask (Python)
   - Waitress as a production-grade WSGI server

3. **Frontend Libraries**
   - Chart.js for dynamic, interactive visualizations
   - Jinja2 for Flask templating

4. **Deployment & DevOps**
   - Docker
   - Render Platform (PaaS)

5. **External Integrations**
   - RESTful News APIs for live market updates
   - Intelligent JSON-based caching to reduce API calls

---

## 🧠 Machine Learning & Data Science

1. **Libraries Used**
   - Scikit-learn
   - Pandas
   - NumPy
   - Matplotlib
   - Seaborn
   - Joblib

2. **Algorithms Evaluated**
   - **Linear Regression**
     - Baseline model for linear relationships.
   - **Random Forest Regressor**
     - Ensemble method using 300 decision trees to capture non-linear patterns and interactions.
   - **Gradient Boosting Regressor**
     - Sequential ensemble method using 500 estimators with depth 5, tuned with learning rate optimization.

3. **Model Selection Strategy**
   - Automatically trains and evaluates multiple models.
   - Dynamically selects the best-performing model based on highest **R² (R-squared)** score.

4. **Evaluation Metrics**
   - **R² (R-Squared):** Proportion of variance explained by the model.
   - **MAE (Mean Absolute Error):** Average absolute prediction error.
   - **RMSE (Root Mean Squared Error):** Penalizes larger prediction errors more strongly.
   - **MAPE (Mean Absolute Percentage Error):** Error represented in percentage form for business interpretability.

---

## 📊 Data Engineering & Feature Engineering

1. **Categorical Encoding**
   - Applied Label Encoding for:
     - City
     - Locality
     - State
     - Property Type
     - Furnishing
     - Floor

2. **Derived Features**
   - **price_per_sqft:** Baseline price efficiency metric.
   - **room_ratio:** Bathrooms ÷ bedrooms to evaluate layout practicality.
   - **is_new:** Binary flag for properties ≤ 3 years old.
   - **is_luxury:** Binary flag when amenities count ≥ 10.
   - **bhk_area:** Interaction feature (bedrooms × area).

---

## 💡 Key Features

1. **AI Price Prediction Engine**
   - Predicts property prices with confidence intervals (low/high estimates) using model MAPE.
   - Generates an additional **Investment Score**.

2. **Interactive Market Dashboard**
   - Real-time visual analysis of top cities, price trends across tiers, and property type insights using Chart.js.

3. **Advanced ROI Calculator**
   - Estimates future value, capital gains, rental income, and monthly EMI.
   - Incorporates interest rates and historical city-specific YoY growth.

4. **Live News & Caching Pipeline**
   - Fetches live real estate news from external APIs.
   - Normalizes and categorizes news (Policy, Market Data, Investment, etc.).
   - Uses local TTL-based caching for performance and API rate-limit optimization.

5. **Production Readiness**
   - Fully containerized with `Dockerfile` and `render.yaml`.
   - Built for scalable cloud deployment.
