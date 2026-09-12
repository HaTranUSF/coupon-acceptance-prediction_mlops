import streamlit as st
import requests

st.set_page_config(page_title="Coupon Acceptance Predictor", page_icon="🚗", layout="wide")

st.title("🚗 Coupon Acceptance Predictor")
st.write("Enter the trip and driver details below to check prediction results from the FastAPI backend.")

# FastAPI endpoint running locally in the same container via Supervisor
API_URL = "http://localhost:8000/predict"

with st.form("prediction_form"):
    st.subheader("Trip & Context Inputs")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        destination = st.selectbox("Destination", ["no urgent place", "home", "work"])
        passenger = st.selectbox("Passenger", ["alone", "friend(s)", "kid(s)", "partner"])
        weather = st.selectbox("Weather", ["sunny", "rainy", "snowy"])
        temperature = st.slider("Temperature (°F)", 10, 100, 80)
        time = st.selectbox("Time of Day", ["10am", "2pm", "6pm", "7am", "10pm"])
        
    with col2:
        coupon = st.selectbox("Coupon Type", ["coffee house", "restaurant(<20)", "carry out & take away", "bar", "restaurant(20-50)"])
        expiration = st.selectbox("Expiration", ["1d", "2h"])
        gender = st.selectbox("Gender", ["female", "male"])
        
        # Age slider converted to match your model's expected categorical bins[cite: 4]
        age_num = st.slider("Driver Age", 16, 80, 26)
        if age_num < 21:
            age = "21"
        elif age_num < 26:
            age = "21"
        elif age_num < 31:
            age = "26"
        elif age_num < 36:
            age = "31"
        elif age_num < 41:
            age = "36"
        elif age_num < 46:
            age = "41"
        elif age_num < 50:
            age = "46"
        else:
            age = "50plus"
            
        maritalStatus = st.selectbox("Marital Status", ["single", "married partner", "unmarried partner", "divorced", "widowed"])
        
    with col3:
        has_children = st.selectbox("Has Children", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        education = st.selectbox("Education", ["some college - no degree", "bachelors degree", "masters degree", "high school graduate", "associates degree", "graduate degree"])
        occupation = st.selectbox("Occupation", ["student", "unemployed", "computer & mathematical", "management", "sales & related"])
        income = st.selectbox("Income Bracket", ["$25000 - $37499", "$50000 - $62499", "$75000 - $87499", "$100000 or more", "less than $12500"])

    st.subheader("Habits & Proximity Flags")
    col4, col5 = st.columns(2)
    with col4:
        Bar = st.selectbox("Visits Bar Frequency", ["never", "less1", "1~3", "4~8", "gt8"])
        CoffeeHouse = st.selectbox("Visits Coffee House Frequency", ["never", "less1", "1~3", "4~8", "gt8"])
        CarryAway = st.selectbox("Carry Away Frequency", ["never", "less1", "1~3", "4~8", "gt8"])
        RestaurantLessThan20 = st.selectbox("Restaurant <20 Frequency", ["never", "less1", "1~3", "4~8", "gt8"])
        Restaurant20To50 = st.selectbox("Restaurant 20-50 Frequency", ["never", "less1", "1~3", "4~8", "gt8"])
        
    with col5:
        toCoupon_GEQ5min = st.selectbox("Distance GEQ 5min", [0, 1], index=1)
        toCoupon_GEQ15min = st.selectbox("Distance GEQ 15min", [0, 1])
        toCoupon_GEQ25min = st.selectbox("Distance GEQ 25min", [0, 1])
        direction_same = st.selectbox("Direction Same", [0, 1])
        direction_opp = st.selectbox("Direction Opposite", [0, 1], index=1)

    submitted = st.form_submit_button("Get Prediction from API")

if submitted:
    # Construct payload matching FastAPI backend requirements[cite: 4]
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
                st.success(f"🎉 **Prediction: LIKELY TO ACCEPT** (Probability: {prob:.1%})")
            else:
                st.warning(f"⚠️ **Prediction: UNLIKELY TO ACCEPT** (Probability: {1 - prob:.1%})")
        else:
            st.error(f"API Error ({response.status_code}): {response.text}")
    except Exception as e:
        st.error(f"Could not connect to FastAPI service: {e}")