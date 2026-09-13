import streamlit as st
import requests

st.set_page_config(page_title="Coupon Acceptance Predictor", page_icon="🎟️", layout="wide")

st.title("🎟️ Coupon Acceptance Predictor")
st.write("Answer a few questions about the trip and the driver, and we'll predict whether they'll use the coupon.")

# FastAPI endpoint running locally in the same container via Supervisor
API_URL = "http://localhost:8000/predict"

# Frequency options come back from the model as short codes. These maps let us
# show plain language in the app while still sending the codes the API expects.
FREQUENCY_LABELS = {
    "never": "Never",
    "less1": "Less than once a month",
    "1~3": "1 to 3 times a month",
    "4~8": "4 to 8 times a month",
    "gt8": "More than 8 times a month",
}

AGE_LABELS = {
    "21": "Under 26",
    "26": "26 to 30",
    "31": "31 to 35",
    "36": "36 to 40",
    "41": "41 to 45",
    "46": "46 to 49",
    "50plus": "50 or older",
}

COUPON_LABELS = {
    "coffee house": "Coffee house",
    "restaurant(<20)": "Restaurant (under $20)",
    "carry out & take away": "Carry out / takeaway",
    "bar": "Bar",
    "restaurant(20-50)": "Restaurant ($20 to $50)",
}

EXPIRATION_LABELS = {
    "1d": "Expires in 1 day",
    "2h": "Expires in 2 hours",
}

EDUCATION_LABELS = {
    "some college - no degree": "Some college, no degree",
    "bachelors degree": "Bachelor's degree",
    "masters degree": "Master's degree",
    "high school graduate": "High school graduate",
    "associates degree": "Associate's degree",
    "graduate degree": "Graduate degree",
}

OCCUPATION_LABELS = {
    "student": "Student",
    "unemployed": "Unemployed",
    "computer & mathematical": "Computer & mathematical",
    "management": "Management",
    "sales & related": "Sales & related",
}

INCOME_LABELS = {
    "less than $12500": "Less than $12,500",
    "$25000 - $37499": "$25,000 to $37,499",
    "$50000 - $62499": "$50,000 to $62,499",
    "$75000 - $87499": "$75,000 to $87,499",
    "$100000 or more": "$100,000 or more",
}

PASSENGER_LABELS = {
    "alone": "Driving alone",
    "friend(s)": "With friend(s)",
    "kid(s)": "With kid(s)",
    "partner": "With partner",
}

DESTINATION_LABELS = {
    "no urgent place": "No particular destination",
    "home": "Heading home",
    "work": "Heading to work",
}

MARITAL_LABELS = {
    "single": "Single",
    "married partner": "Married",
    "unmarried partner": "Unmarried partner",
    "divorced": "Divorced",
    "widowed": "Widowed",
}


def label_for(options, labels):
    """Small helper so selectbox shows plain text while keeping the raw code."""
    return lambda value: labels.get(value, value)


with st.form("prediction_form"):
    st.subheader("About the Trip")
    col1, col2, col3 = st.columns(3)

    with col1:
        destination = st.selectbox(
            "Where is the driver headed?",
            list(DESTINATION_LABELS.keys()),
            format_func=label_for(DESTINATION_LABELS, DESTINATION_LABELS),
        )
        passenger = st.selectbox(
            "Who's in the car?",
            list(PASSENGER_LABELS.keys()),
            format_func=label_for(PASSENGER_LABELS, PASSENGER_LABELS),
        )
        weather = st.selectbox("What's the weather like?", ["sunny", "rainy", "snowy"])
        temperature = st.slider("Temperature outside (°F)", 10, 100, 80)
        time = st.select_slider(
            "What time is it?",
            options=["7am", "10am", "2pm", "6pm", "10pm"],
        )

    with col2:
        coupon = st.selectbox(
            "What kind of coupon is it?",
            list(COUPON_LABELS.keys()),
            format_func=label_for(COUPON_LABELS, COUPON_LABELS),
        )
        expiration = st.selectbox(
            "When does the coupon expire?",
            list(EXPIRATION_LABELS.keys()),
            format_func=label_for(EXPIRATION_LABELS, EXPIRATION_LABELS),
        )
        gender = st.selectbox("Driver's gender", ["female", "male"], format_func=lambda x: x.capitalize())

        age_num = st.slider("Driver's age", 16, 80, 26)
        if age_num < 26:
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
        st.caption(f"Age group used for prediction: {AGE_LABELS[age]}")

        maritalStatus = st.selectbox(
            "Marital status",
            list(MARITAL_LABELS.keys()),
            format_func=label_for(MARITAL_LABELS, MARITAL_LABELS),
        )

    with col3:
        has_children = st.selectbox("Does the driver have children?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        education = st.selectbox(
            "Education level",
            list(EDUCATION_LABELS.keys()),
            format_func=label_for(EDUCATION_LABELS, EDUCATION_LABELS),
        )
        occupation = st.selectbox(
            "Occupation",
            list(OCCUPATION_LABELS.keys()),
            format_func=label_for(OCCUPATION_LABELS, OCCUPATION_LABELS),
        )
        income = st.selectbox(
            "Household income",
            list(INCOME_LABELS.keys()),
            format_func=label_for(INCOME_LABELS, INCOME_LABELS),
        )

    st.subheader("How Often Does The Person Go Out?")
    col4, col5 = st.columns(2)

    with col4:
        Bar = st.selectbox("Visits bars", list(FREQUENCY_LABELS.keys()), format_func=label_for(FREQUENCY_LABELS, FREQUENCY_LABELS))
        CoffeeHouse = st.selectbox("Visits coffee houses", list(FREQUENCY_LABELS.keys()), format_func=label_for(FREQUENCY_LABELS, FREQUENCY_LABELS))
        CarryAway = st.selectbox("Orders carry out", list(FREQUENCY_LABELS.keys()), format_func=label_for(FREQUENCY_LABELS, FREQUENCY_LABELS))
        RestaurantLessThan20 = st.selectbox("Eats at restaurants under $20", list(FREQUENCY_LABELS.keys()), format_func=label_for(FREQUENCY_LABELS, FREQUENCY_LABELS))
        Restaurant20To50 = st.selectbox("Eats at restaurants \\$20 to \\$50", list(FREQUENCY_LABELS.keys()), format_func=label_for(FREQUENCY_LABELS, FREQUENCY_LABELS))

    with col5:
        distance_choice = st.selectbox(
            "How far is the coupon location?",
            ["Under 5 minutes", "5 to 15 minutes", "15 to 25 minutes", "Over 25 minutes"],
            index=1,
        )

        if distance_choice == "Under 5 minutes":
            toCoupon_GEQ5min, toCoupon_GEQ15min, toCoupon_GEQ25min = 0, 0, 0
        elif distance_choice == "5 to 15 minutes":
            toCoupon_GEQ5min, toCoupon_GEQ15min, toCoupon_GEQ25min = 1, 0, 0
        elif distance_choice == "15 to 25 minutes":
            toCoupon_GEQ5min, toCoupon_GEQ15min, toCoupon_GEQ25min = 1, 1, 0
        else:
            toCoupon_GEQ5min, toCoupon_GEQ15min, toCoupon_GEQ25min = 1, 1, 1

        direction_choice = st.radio(
            "Is the coupon location on the way, or out of the way?",
            ["On the way", "Out of the way"],
            index=1,
        )

        if direction_choice == "On the way":
            direction_same, direction_opp = 1, 0
        else:
            direction_same, direction_opp = 0, 1

    submitted = st.form_submit_button("Get Prediction")

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
        "direction_opp": direction_opp,
    }

    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            res_data = response.json()
            pred = res_data["accept_prediction"]
            prob = res_data["probability"]
            if pred == 1:
                st.success(f"🎉 **This driver will likely use the coupon** (Confidence: {prob:.1%})")
            else:
                st.warning(f"⚠️ **This driver will likely skip the coupon** (Confidence: {1 - prob:.1%})")
        else:
            st.error(f"Something went wrong talking to the prediction service (error {response.status_code}). Please try again.")
    except Exception as e:
        st.error(f"Could not reach the prediction service: {e}")