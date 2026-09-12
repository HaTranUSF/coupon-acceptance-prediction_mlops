# Data-Driven Coupon Acceptance Prediction 🚀🎟️
[Link to my notebook](https://github.com/HaTranUSF/coupon-acceptance-prediction/blob/main/ISM4543_Final_Project_Draft.ipynb) | [Live Web Application](https://coupon-acceptance-prediction-mlops.onrender.com)

### Optimizing Digital Offers for Drivers 🚗🎟️ (Production-Ready MLOps Edition)

## 📌 Table of Contents
* [🤝 Collaborative Project & My Contributions](#-collaborative-project--my-contributions)
* [⚡ What's New in the Upgraded Version](#-whats-new-in-the-upgraded-version)
* [🎯 Project Overview](#-project-overview)
* [📊 Business Context & Key Metrics](#-business-context--key-metrics)
* [💾 Data](#-data)
* [🛠️ Methodology & Feature Engineering](#-methodology--feature-engineering)
* [⚙️ System Architecture & Deployment](#️-system-architecture--deployment)
* [📊 Key Findings & Insights](#-key-findings--insights)
* [📈 Final Model Performance](#-final-model-performance)
* [💰 Business Recommendations](#-business-recommendations)
* [🚀 Next Steps](#-next-steps)

---
## 🤝 Collaborative Project & My Contributions

This project was originally developed collaboratively with a teammate. My core contributions focused on **exploratory data analysis, feature engineering, model development, model evaluation, and business-impact analysis**.

### Core Contributions
- Conducted exploratory data analysis to identify key patterns in coupon acceptance behavior.
- Performed rigorous data cleaning and feature engineering pipelines.
- Developed and evaluated multiple predictive models (Logistic Regression, Decision Trees, Random Forests).
- Tuned the final model to balance business costs between false positives and false negatives.
- Evaluated model performance using business-oriented metrics.
- Translated model results into actionable coupon-targeting recommendations yielding **~-500 in cost reduction** compared with the baseline.

---

## ⚡ What's New in the Upgraded Version

This repository has been scaled from an academic machine learning notebook into a **production-grade, containerized MLOps web application**. 

* **Dual-Process Architecture (`supervisord`):** Combined a high-performance **FastAPI backend** (handling live data preprocessing and model inference) with an interactive **Streamlit frontend** inside a single optimized Docker container.
* **Full-Stack Deployment on Render:** Hosted live on Render using custom port routing and automated web-service deployment.
* **Enhanced UI with Smart Inputs:** Redesigned the frontend to capture all 24 feature dimensions cleanly—introducing a continuous numeric age slider mapped dynamically to model categorical bins.
* **Robust API Serialization:** Maintained strict consistency between training preprocessing routines (`clean_data`, `engineer_features`) and serving pipelines via Pydantic payload validation.

---

## 🎯 Project Overview

This project develops a machine-learning model to **predict the likelihood that a food delivery or ride-hailing driver will accept a digital coupon offer**, shifting from broad voucher blasts to data-driven targeting.

---

## 📊 Business Context & Key Metrics

Duber sends a large volume of digital coupons, leading to wasted voucher costs and lost revenue.

### 💸 Cost of Prediction Errors
* **False Negative (FN):** Predicts driver will **not** accept when they **would** $\rightarrow$ **$20 lost revenue** per missed conversion.
* **False Positive (FP):** Predicts driver **will** accept when they **won't** $\rightarrow$ **$10 wasted voucher** per case.

---

## 🛠️ Methodology & Feature Engineering

* **Data Cleaning:** Dropped sparse columns and applied mode imputation.
* **Feature Engineering:** Built automated mapping steps for categorical encoding, scaling, and handling proximity flags.
* **Model Selection:** Evaluated models with an optimized **Random Forest Classifier** selected for its superior recall-precision balance.

---

## ⚙️ System Architecture & Deployment

The application runs via a unified Docker image orchestrated by **Supervisor**:
1. **FastAPI (`port 8000`):** Loads `models/model.pkl`, handles input validation through Pydantic (`CouponRequest`), runs feature engineering pipelines, and executes inference.
2. **Streamlit (`port 10000`):** Renders an interactive web interface allowing users to slide, select, and submit driver profiles over HTTP requests to the backend.

---

## 📊 Key Findings & Insights

* **Top Predictive Features:** Coffee House visit frequency, Restaurant (<$20) coupon types, Carry out & Take Away offers, and Bar visit frequency.
* **Behavioral Peaks:** Acceptance peaks at **2 PM and 6 PM**, under **sunny conditions**, and when drivers are within **5–15 minutes** of the destination.

---

## 📈 Final Model Performance

* **Recall:** **0.751** (Captures 75.1% of actual acceptors to minimize $20 FN losses)
* **Precision:** **0.760**
* **F1-Score:** **0.755**

---

## 💰 Business Recommendations

1. **Timing & Weather:** Target windows between **10 AM–2 PM and 6 PM** on sunny days.
2. **Offer Prioritization:** Emphasize *Carry Out & Take Away* and *Restaurant (<$20)* vouchers.
3. **Geo-Fencing:** Deploy coupons strictly within a **5–15 minute** proximity window.
4. **Demographics:** Focus heavily on the **$50k–$62.5k** income bracket.

---

## 🚀 Next Steps

* **A/B Test Pilot Deployment:** Compare model-driven targeting against historical blind blasts.
* **Automated Feedback Loops:** Implement continuous retraining pipelines using real redemption logs to counteract data drift.