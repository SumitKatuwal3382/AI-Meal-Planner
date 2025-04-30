# Import All the Required Libraries
import streamlit as st
import json
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

# Setup the Environment
load_dotenv()

# Initialize and load the Llama 3.3 Model
llm = ChatGroq(model="llama-3.3-70b-versatile")

# Define the function to load custom CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Create a Streamlit Application - st.set_page_config must be the first Streamlit command
st.set_page_config(page_title="AI Meal Planner", layout="centered")

# Apply custom styling after set_page_config
load_css("styles.css")

st.title("AI Meal Planner")

# Create two columns for input fields
col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    weight = st.slider("Weight (kg)", min_value=30, max_value=200, value=70)

with col2:
    age = st.number_input("Age", min_value=15, max_value=90, value=20)
    height = st.slider("Height (cm)", min_value=20, max_value=250, value=150)

aim = st.radio("Aim", ["Lose", "Gain", "Maintain"])

user_data = f"""
                - I am a {gender}.
                - My weight is {weight} kg.
                - I am {age} years old.
                - My height is {height} cm.
                - My aim is to {aim} weight.
            """
output_format = """
                {
                    "range": "Range of ideal weight",
                    "target": "Target Weight",
                    "difference": "Weight I need to gain or lose",
                    "bmi": "My BMI",
                    "meal_plan": {
                        "Day 1": {
                            "Breakfast": {"meal": "Description", "calories": "Calorie count"},
                            "Lunch": {"meal": "Description", "calories": "Calorie count"},
                            "Dinner": {"meal": "Description", "calories": "Calorie count"}
                        },
                        "Day 2": {
                            "Breakfast": {"meal": "Description", "calories": "Calorie count"},
                            "Lunch": {"meal": "Description", "calories": "Calorie count"},
                            "Dinner": {"meal": "Description", "calories": "Calorie count"}
                        },
                        "Day 3": {
                            "Breakfast": {"meal": "Description", "calories": "Calorie count"},
                            "Lunch": {"meal": "Description", "calories": "Calorie count"},
                            "Dinner": {"meal": "Description", "calories": "Calorie count"}
                        },
                        "Day 4": {
                            "Breakfast": {"meal": "Description", "calories": "Calorie count"},
                            "Lunch": {"meal": "Description", "calories": "Calorie count"},
                            "Dinner": {"meal": "Description", "calories": "Calorie count"}
                        },
                        "Day 5": {
                            "Breakfast": {"meal": "Description", "calories": "Calorie count"},
                            "Lunch": {"meal": "Description", "calories": "Calorie count"},
                            "Dinner": {"meal": "Description", "calories": "Calorie count"}
                        },
                        "Day 6": {
                            "Breakfast": {"meal": "Description", "calories": "Calorie count"},
                            "Lunch": {"meal": "Description", "calories": "Calorie count"},
                            "Dinner": {"meal": "Description", "calories": "Calorie count"}
                        },
                        "Day 7": {
                            "Breakfast": {"meal": "Description", "calories": "Calorie count"},
                            "Lunch": {"meal": "Description", "calories": "Calorie count"},
                            "Dinner": {"meal": "Description", "calories": "Calorie count"}
                        }
                    },
                    "total_days": "Total days to reach target weight",
                    "weight_per_week": "Weight to lose or gain per week, a week has 7 days, make sure to do calculation carefully"
                }
                """
prompt = user_data + ("Using the information provided, generate output by following the output format defined. "
                      "The output should be in JSON format, nothing else, exclude any additional description or detail.") + output_format

def clean_json_string(json_string):
    # Remove the starting and ending backticks and any language identifier
    if json_string.startswith('```'):
        json_string = json_string[json_string.find('\n')+1:-3].strip()
    elif json_string.endswith('```'):
        json_string = json_string[:-3].strip()
    # Validate the JSON format
    try:
        parsed_json = json.loads(json_string)
        return parsed_json
    except json.JSONDecodeError:
        raise ValueError("The provided string is not valid JSON.")

if st.button("Generate Meal Plan"):
    with st.spinner("Creating Meal Plan"):
        text_area_placeholder = st.empty()
        result = llm.invoke(prompt)
        parser = StrOutputParser()
        response = parser.invoke(result)
        if text_area_placeholder:
            meal_plan = text_area_placeholder.text_area("Generated JSON", value=response, height=350)
        meal_plan_json = clean_json_string(meal_plan)

        st.title("Meal Plan")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Range")
            st.markdown(meal_plan_json["range"])
            st.subheader("Target")
            st.markdown(meal_plan_json["target"])
        with col2:
            st.subheader(f"{aim}")
            st.markdown(meal_plan_json["difference"])
            st.subheader("BMI")
            st.markdown(meal_plan_json["bmi"])
        with col3:
            st.subheader("Total Days")
            st.markdown(meal_plan_json["total_days"])
            st.subheader("Per Week")
            st.markdown(meal_plan_json["weight_per_week"])

        st.subheader("Meal Plan for 7 Days")
        for day, meals in meal_plan_json["meal_plan"].items():
            st.markdown(f"**{day}**")
            st.markdown(f"- **Breakfast**: {meals['Breakfast']['meal']} ({meals['Breakfast']['calories']})")
            st.markdown(f"- **Lunch**: {meals['Lunch']['meal']} ({meals['Lunch']['calories']})")
            st.markdown(f"- **Dinner**: {meals['Dinner']['meal']} ({meals['Dinner']['calories']})")
