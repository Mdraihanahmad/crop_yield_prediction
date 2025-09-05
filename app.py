import os
import requests
import streamlit as st
import pandas as pd
import pickle
import gdown


# Google Drive file ID
FILE_ID = "1rmdlpjDkLMCETbLNDO0PGZP8JErWWG8p"
OUTPUT = "pipeline.pkl"

# Download pipeline.pkl if not present
if not os.path.exists(OUTPUT):
    try:
        url = f"https://drive.google.com/uc?id={FILE_ID}"
        gdown.download(url, OUTPUT, quiet=False)
    except Exception as e:
        st.error(f"❌ Could not download pipeline.pkl. Error: {e}")

# Load the pipeline
pipeline = None
if os.path.exists(OUTPUT):
    try:
        with open(OUTPUT, "rb") as f:
            pipeline = pickle.load(f)
    except Exception as e:
        st.error(f"❌ Failed to load pipeline.pkl. Error: {e}")

# Assuming your predict_crop_yield function
def predict_crop_yield(pipeline, area, item, year, average_rain_fall_mm_per_year, pesticides_tonnes, avg_temp):
    input_data = pd.DataFrame({
        'Area': [area],
        'Item': [item],
        'Year': [year],
        'average_rain_fall_mm_per_year': [average_rain_fall_mm_per_year],
        'pesticides_tonnes': [pesticides_tonnes],
        'avg_temp': [avg_temp]
    })
    prediction = pipeline.predict(input_data)
    return prediction[0]

# Streamlit app
def main():
    import matplotlib.pyplot as plt
    from fpdf import FPDF
    import io
    import base64

    # Sidebar contact/feedback
    st.sidebar.markdown("---")
    st.sidebar.header("Contact & Feedback")
    st.sidebar.info("""
    📧 Email: mdraihanahmad47@gmail.com  
    💬 Feedback: [Google Form](https://forms.gle/CXbUbWCwmw2WmRpG6)
    """)

    # Session state for reset
    if 'reset' not in st.session_state:
        st.session_state['reset'] = False

    # Sidebar with app info and a fun quote
    st.sidebar.image("https://img.icons8.com/fluency/96/tractor.png", width=64)
    st.sidebar.title("About This App")
    st.sidebar.info("""
    🌱 **Crop Yield Predictor**
    
    Predict your crop yield based on real farm and weather data. Built with ❤️ for farmers and agri-enthusiasts.
    """)
    st.sidebar.markdown(
        "> _'The ultimate goal of farming is not the growing of crops, but the cultivation and perfection of human beings.'_  \n> - Md Raihan Ahmad"
    )

    st.markdown(
        """
        <style>
        body, .main, .block-container {
            background: #f6fbf4 !important;
        }
        .custom-card {
            background: #fff;
            border-radius: 18px;
            box-shadow: 0 4px 24px 0 rgba(34, 139, 34, 0.10);
            padding: 2.5rem 2rem 2rem 2rem;
            margin: 2rem auto;
            max-width: 600px;
        }
        .result-card {
            background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
            border-radius: 14px;
            padding: 1.5rem 1.2rem;
            margin-top: 1.5rem;
            color: #234d20;
            box-shadow: 0 2px 12px 0 rgba(34, 139, 34, 0.10);
        }
        /* Force light background and text for all input fields and labels */
        .stTextInput, .stNumberInput, .stSelectbox, .stTextArea, .stDateInput, .stSlider, .stMultiSelect, .stRadio, .stCheckbox {
            background: #fff !important;
            color: #234d20 !important;
            border-radius: 10px !important;
            box-shadow: 0 2px 8px 0 rgba(34, 139, 34, 0.07);
        }
        label, .stTextInput label, .stNumberInput label, .stSelectbox label {
            color: #234d20 !important;
            font-weight: 500 !important;
        }
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
            background: #fff !important;
            color: #234d20 !important;
        }
        .stButton>button {
            background: linear-gradient(90deg, #43cea2 0%, #185a9d 100%);
            color: white;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: bold;
            padding: 0.6rem 2.2rem;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #185a9d 0%, #43cea2 100%);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class='custom-card'>
        <h1 style='text-align:center; color:#234d20; margin-bottom:0.2em;'>
            <span style='font-size:1.5em;'>📈</span> Crop Yield Prediction
        </h1>
        <p style='text-align:center; color:#6b7b6b; margin-top:0;'>
            Enter your farm conditions to get accurate yield predictions
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        crop_options = [
            'Maize', 'Wheat', 'Rice', 'Potatoes', 'Barley', 'Soybeans',
            'Tomato', 'Onion', 'Carrot', 'Cabbage', 'Spinach', 'Peas', 'Cauliflower',
            'Apple', 'Banana', 'Mango', 'Orange', 'Grapes', 'Pineapple', 'Papaya',
            'Strawberry', 'Watermelon', 'Pumpkin', 'Cucumber', 'Chili', 'Brinjal',
            'Lettuce', 'Garlic', 'Ginger', 'Sugarcane', 'Cotton', 'Other'
        ]
        default_values = {
            'item': 'Maize',
            'pesticides_tonnes': '',
            'average_rain_fall_mm_per_year': '',
            'avg_temp': '',
            'area': 'India',
            'year': 2025
        }
        if st.session_state['reset']:
            item = default_values['item']
            pesticides_tonnes = default_values['pesticides_tonnes']
            average_rain_fall_mm_per_year = default_values['average_rain_fall_mm_per_year']
            avg_temp = default_values['avg_temp']
            area = default_values['area']
            year = default_values['year']
            st.session_state['reset'] = False
        else:
            item = st.selectbox('Crop Type', crop_options, index=0)
            pesticides_tonnes = st.text_input('Pesticide Usage (kg/ha)', placeholder='e.g., 150')
            average_rain_fall_mm_per_year = st.text_input('Annual Rainfall (mm)', placeholder='e.g., 800')
            avg_temp = st.text_input('Average Temperature (°C)', placeholder='e.g., 25')
            area = st.text_input('Area', value='Albania')
            year = st.number_input('Year', min_value=1900, max_value=2100, value=2025)

        st.markdown("<br>", unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns([2,1])
        with col_btn1:
            predict_btn = st.button('🧮 Predict Yield')
        with col_btn2:
            reset_btn = st.button('🔄 Reset Form')
        st.markdown("</div>", unsafe_allow_html=True)

    if reset_btn:
        st.session_state['reset'] = True
        st.experimental_rerun()

    if predict_btn:
        with st.spinner('Analyzing your data and predicting yield...'):
            # Convert inputs to correct types
            try:
                avg_temp_val = float(avg_temp)
                rain_val = float(average_rain_fall_mm_per_year)
                pest_val = float(pesticides_tonnes)
            except Exception:
                st.error("Please enter valid numeric values for rainfall, pesticide usage, and temperature.")
                return
            predicted_yield = predict_crop_yield(
                pipeline,
                area,
                item,
                year,
                rain_val,
                pest_val,
                avg_temp_val
            )
            # Recommendation logic (simple example)
            if predicted_yield > 40000:
                rec = "Excellent yield expected! Continue current practices and consider premium crop varieties."
            elif predicted_yield > 20000:
                rec = "Good yield. Consider optimizing fertilizer and irrigation for even better results."
            else:
                rec = "Yield is below average. Review soil health, crop rotation, and input levels."

            # Show summary table
            st.subheader("Summary of Your Input & Prediction")
            summary_df = pd.DataFrame({
                'Feature': ['Area', 'Crop', 'Year', 'Rainfall (mm)', 'Pesticide (kg/ha)', 'Avg Temp (°C)', 'Predicted Yield (hg/ha)'],
                'Value': [area, item, year, rain_val, pest_val, avg_temp_val, f"{predicted_yield:.2f}"]
            })
            st.table(summary_df)

            # Simple chart: predicted vs. average yield
            crop_avg_yield = {
                'Maize': 35000, 'Wheat': 32000, 'Rice': 40000, 'Potatoes': 45000, 'Barley': 30000, 'Soybeans': 28000,
                'Tomato': 50000, 'Onion': 42000, 'Carrot': 41000, 'Cabbage': 43000, 'Spinach': 39000, 'Peas': 37000, 'Cauliflower': 42000,
                'Apple': 25000, 'Banana': 60000, 'Mango': 55000, 'Orange': 48000, 'Grapes': 52000, 'Pineapple': 58000, 'Papaya': 54000,
                'Strawberry': 47000, 'Watermelon': 62000, 'Pumpkin': 44000, 'Cucumber': 43000, 'Chili': 36000, 'Brinjal': 41000,
                'Lettuce': 35000, 'Garlic': 34000, 'Ginger': 33000, 'Sugarcane': 70000, 'Cotton': 29000, 'Other': 30000
            }
            avg_yield = crop_avg_yield.get(item, 30000)
            fig, ax = plt.subplots(figsize=(4,2.5))
            ax.bar(['Predicted', 'Average'], [predicted_yield, avg_yield], color=['#43cea2', '#185a9d'])
            ax.set_ylabel('Yield (hg/ha)')
            ax.set_title(f'Predicted vs. Average Yield for {item}')
            st.pyplot(fig)

            # PDF download
            class PDF(FPDF):
                def header(self):
                    self.set_font('Arial', 'B', 14)
                    self.cell(0, 10, 'Crop Yield Prediction Report', ln=1, align='C')
                def footer(self):
                    self.set_y(-15)
                    self.set_font('Arial', 'I', 8)
                    self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

            pdf = PDF()
            pdf.add_page()
            pdf.set_font('Arial', '', 12)
            pdf.cell(0, 10, f'Area: {area}', ln=1)
            pdf.cell(0, 10, f'Crop: {item}', ln=1)
            pdf.cell(0, 10, f'Year: {year}', ln=1)
            pdf.cell(0, 10, f'Rainfall (mm): {rain_val}', ln=1)
            pdf.cell(0, 10, f'Pesticide (kg/ha): {pest_val}', ln=1)
            pdf.cell(0, 10, f'Avg Temp (°C): {avg_temp_val}', ln=1)
            pdf.cell(0, 10, f'Predicted Yield (hg/ha): {predicted_yield:.2f}', ln=1)
            pdf.multi_cell(0, 10, f'Recommendation: {rec}')
            pdf_bytes = pdf.output(dest='S').encode('latin1')
            b64 = base64.b64encode(pdf_bytes).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="crop_yield_report.pdf">📄 Download Prediction as PDF</a>'

            st.markdown(f"""
                <div class='result-card'>
                    <h4 style='margin-bottom:0.5em;'>📈 Yield Prediction Results</h4>
                    <b>Crop:</b> {item}<br>
                    <b>Predicted Yield:</b> {predicted_yield:.2f} hg/ha<br>
                    <b>Recommendation:</b> {rec}<br><br>
                    {href}
                </div>
            """, unsafe_allow_html=True)

    # Footer with credits
    st.markdown("""
    <div style='text-align:center; color:#b2c8b2; margin-top:2.5em; font-size:0.95em;'>
        Made with <span style='color:#43cea2;'>♥</span> by <b>Md Raihan Ahmad</b> | Powered by Streamlit
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
