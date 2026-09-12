import streamlit as st
import requests

st.set_page_config(page_title="Coupon Acceptance Predictor", page_icon="🚗", layout="wide")

st.title("🚗 Coupon Acceptance Predictor")
st.write("Enter the trip and driver details below to check prediction results from the FastAPI backend.")

# FastAPI endpoint (pointing locally since they run in the same container)
API_URL = "http://localhost:8000/predict"

with st.form("prediction_form"):
    st.subheader("Trip & Context")
    col1, col2, col3 = st.cols(3) if hasattr(st, "cols") else st.columns(3)
    
    with col1:
        destination = st.selectbox("Destination", ["no urgent place", "home", "work"])
        passenger = st.selectbox("Passenger", ["alone", "friend(s)", "kid(s)", "partner"])
        weather = st.selectbox("Weather", ["sunny", "rainy", "snowy"])
        temperature = st.slider("Temperature", 10, 100, 80)
        time = st.selectbox("Time", ["10am", "2pm", "6pm", "10am", "7am"])
        
    with col2:
        coupon = st.selectbox("Coupon", ["coffee house", "restaurant(<20)", "carry out & take away", "bar", "restaurant(20-50)"])
        expiration = st.selectbox("Expiration", ["1d", "2h"])
        gender = st.selectbox("Gender", ["female", "male"])
        age = st.selectbox("Age", ["21", "26", "31", "36", "41", "46", "50plus"])
        maritalStatus = st.selectbox("Marital Status", ["single", "married partner", "unmarried partner", "divorced", "widowed"])
        
    with col3:
        has_children = st.selectbox("Has Children", [0, 1])
        education = st.selectbox("Education", ["some college - no degree", "bachelors degree", "masters degree"])
        occupation = st.selectbox("Occupation", ["student", "unemployed", "computer & mathematical", "management"])
        income = st.selectbox("Income", ["$25000 - $37499", "$50000 - $62499", "$100000 or more"])

    st.subheader("Habits & Proximity Flags")
    col4, col5 = st.columns(2)
    with col4:
        Bar = st.selectbox("Bar Visits", ["never", "less1", "1~3", "4~8", "gt8"])
        CoffeeHouse = st.selectbox("Coffee House Visits", ["never", "less1", "1~3", "4~8", "gt8"])
        CarryAway = st.selectbox("Carry Away", ["never", "less1", "1~3", "4~8", "gt8"])
        RestaurantLessThan20 = st.selectbox("Restaurant <20", ["never", "less1", "1~3", "4~8", "gt8"])
        Restaurant20To50 = st.selectbox("Restaurant 20-50", ["never", "less1", "1~3", "4~8", "gt8"])
        
    with col5:
        toCoupon_GEQ5min = st.selectbox("Distance GEQ 5min", [0, 1], index=1)
        toCoupon_GEQ15min = st.selectbox("Distance GEQ 15min", [0, 1])
        toCoupon_GEQ25min = st.selectbox("Distance GEQ 25min", [0, 1])
        direction_same = st.selectbox("Direction Same", [0, 1])
        direction_opp = st.selectbox("Direction Opp", [0, 1], index=1)

    submitted = st.form_submit_button("Get Prediction from API")

if submitted:
    payload = {
        "destination": destination,
        "passenger": passenger,
        "weather": weather,
        "temperature": temperature,
        "time": time,
        "coupon": coupon,
        "expiration": expiration,
        "gender": gender,
        "age": age,
        "maritalStatus": maritalStatus,
        "has_children": has_children,
        "education": education,
        "occupation": occupation,
        "income": income,
        "Bar": Bar,
        "CoffeeHouse": CoffeeHouse,
        "CarryAway": CarryAway,
        "RestaurantLessThan20": RestaurantLessThan20,
        "Restaurant20To50": Restaurant20To50,
        "toCoupon_GEQ5min": toCoupon_GEQ5min,
        "toCoupon_GEQ15min": toCoupon_GEQ15min,
        "toCoupon_GEQ25min": toCoupon_GEQ25min,
        "direction_same": direction_same,
        "direction_opp": direction_opp
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            res_data = response.json()
            pred = res_data["accept_prediction"]
            prob = res_data["probability"]
            if pred == 1:
                st.success(f"🎉 Driver is LIKELY to accept! (Probability: {prob:.1%})")
            else:
                st.warning(f"⚠️ Driver is UNLIKELY to accept. (Probability: {1-prob:.1%})")
        else:
            st.error(f"API Error: {response.text}")
    except Exception as e:
        st.error(f"Could not connect to FastAPI service: {e}")