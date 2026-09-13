# Predicting Coupon Acceptance for a Driverless Taxi Fleet 🚕🎟️
[Link to my notebook](https://github.com/HaTranUSF/coupon-acceptance-prediction/blob/main/ISM4543_Final_Project_Draft.ipynb) | [Live Web Application](https://coupon-acceptance-prediction-mlops.onrender.com)

### Turning an Empty Ride Into a Revenue Opportunity (Production-Ready MLOps Edition)

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
- Translated model results into actionable coupon-targeting recommendations yielding **~$500 in cost reduction** compared with the baseline.

---

## ⚡ What's New in the Upgraded Version

This repository has been scaled from an academic machine learning notebook into a **production-grade, containerized MLOps web application**.

* **Dual-Process Architecture (`supervisord`):** Combined a high-performance **FastAPI backend** (handling live data preprocessing and model inference) with an interactive **Streamlit frontend** inside a single optimized Docker container.
* **Full-Stack Deployment on Render:** Hosted live on Render using custom port routing and automated web-service deployment.
* **Enhanced UI with Smart Inputs:** Redesigned the frontend to capture all 24 feature dimensions cleanly, including a continuous numeric age slider mapped dynamically to model categorical bins.
* **Robust API Serialization:** Maintained strict consistency between training preprocessing routines (`clean_data`, `engineer_features`) and serving pipelines via Pydantic payload validation.

---

## 🎯 Project Overview

Duber is rolling out a driverless taxi fleet. With no driver up front, the back of the front seat now holds an idle screen for the whole ride, and Duber wants to use it for something better than dead air.

The idea: while the taxi is en route, the screen can surface a coupon for a nearby coffee shop, restaurant, bar, or carry-out spot that sits close to the passenger's current route. If the passenger taps to accept, the taxi offers to add that stop to the trip, either as a free detour (covered by the partner venue) or for a small added fare, before continuing on to the original destination.

This only works if the offer shows up at the right moment. A coupon for a coffee shop ten minutes out of the way, shown to someone rushing to a meeting, is just a distraction and a wasted ad slot. This project builds the model that decides when a coupon is actually worth showing.

---

## 📊 Business Context & Key Metrics

Every screen prompt costs Duber something, whether the passenger accepts or not, so blasting a coupon on every ride is not free money. The goal is to only trigger the in-cabin offer when a passenger is actually likely to say yes to the detour.

### 💸 Cost of Prediction Errors
* **False Negative (FN):** Model predicts the passenger will **decline**, so the screen stays blank when they actually **would have** added the stop $\rightarrow$ **$20 in lost detour revenue** per missed opportunity.
* **False Positive (FP):** Model predicts the passenger will **accept**, so the screen shows the offer, but they ignore or decline it $\rightarrow$ **$10 wasted** on the partner-subsidized voucher and screen slot.

---

## 🛠️ Methodology & Feature Engineering

* **Data Cleaning:** Dropped sparse columns and applied mode imputation.
* **Feature Engineering:** Built automated mapping steps for categorical encoding, scaling, and handling proximity flags between the passenger's route and the coupon venue.
* **Model Selection:** Evaluated several models, with an optimized **Random Forest Classifier** selected for its superior recall-precision balance.

---

## ⚙️ System Architecture & Deployment

The application runs via a unified Docker image orchestrated by **Supervisor**, mirroring how this would sit inside the in-cabin screen system:
1. **FastAPI (`port 8000`):** Loads `models/model.pkl`, handles input validation through Pydantic (`CouponRequest`), runs feature engineering pipelines, and executes inference in real time as the ride progresses.
2. **Streamlit (`port 10000`):** Renders an interactive interface standing in for the in-cabin display, letting a rider profile and trip context be entered and submitted to the backend.

---

## 📊 Key Findings & Insights

* **Top Predictive Features:** Coffee house visit frequency, restaurant (<$20) coupon types, carry-out and take-away offers, and bar visit frequency.
* **Behavioral Peaks:** Acceptance peaks at **2 PM and 6 PM**, under **sunny conditions**, and when the coupon venue is within **5 to 15 minutes** of the passenger's current route, close enough to feel like a quick detour rather than a real delay.

---

## 📈 Final Model Performance

* **Recall:** **0.751** (Catches 75.1% of passengers who would have accepted, protecting against the $20 missed-detour cost)
* **Precision:** **0.760**
* **F1-Score:** **0.755**

---

## 💰 Business Recommendations

1. **Timing & Weather:** Trigger the in-cabin offer during **10 AM to 2 PM and around 6 PM** on sunny days, when acceptance is highest.
2. **Offer Prioritization:** Lead with **carry-out and take-away** and **restaurant (<$20)** vouchers, the categories with the strongest pull.
3. **Route-Aware Geo-Fencing:** Only surface a coupon when the venue is a **5 to 15 minute** detour from the current route, not further.
4. **Demographics:** Prioritize riders in the **$50k to $62.5k** income bracket, where acceptance is strongest.

---

## 🚀 Next Steps

* **A/B Test Pilot Deployment:** Compare model-triggered in-cabin offers against a control group with no screen prompts, to confirm the detour revenue lift is real.
* **Automated Feedback Loops:** Implement continuous retraining pipelines using real ride and redemption logs to counteract data drift as routes, venues, and passenger habits change.