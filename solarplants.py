import streamlit as st
import pandas as pd
import os

# Custom CSS for colorful styling
st.markdown("""
    <style>
        .main {
            background-color: #f0f2f6;
        }
        .title {
            font-size: 30px;
            color: #1f77b4;
            font-weight: bold;
            text-align: center;
        }
        .section {
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 15px;
        }
        .saved-note {
            background-color: #eaf7e4;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# File path for local storage
csv_file_path = "plant_notes.csv"

# Function to read saved notes
def read_saved_notes():
    if os.path.exists(csv_file_path):
        return pd.read_csv(csv_file_path)
    return pd.DataFrame(columns=["plant_name", "note"])

# Function to save notes to CSV
def save_plant_notes(plant_notes):
    new_data = pd.DataFrame(plant_notes.items(), columns=["plant_name", "note"])

    if os.path.exists(csv_file_path):
        existing_data = pd.read_csv(csv_file_path)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_csv(csv_file_path, index=False)

# Load existing plant names from an Excel sheet
def load_plant_names():
    excel_file = "plant_names.xlsx"  # Ensure this file exists in the same directory
    df = pd.read_excel(excel_file)
    return df["plant_name"].tolist()

# Get plant names from Excel
plant_names = load_plant_names()
plant_names.insert(0, "All")  # Add "All" option

# Sidebar navigation
st.sidebar.image("https://via.placeholder.com/150", width=150)  # Replace with your logo/image
st.sidebar.title("Dashboard Navigation")
selected_page = st.sidebar.radio("Go to", ["Home", "Saved Notes"])

# Main Page
st.markdown('<div class="title">🌿 Plant Information Dashboard</div>', unsafe_allow_html=True)

if selected_page == "Home":
    st.markdown('<div class="section"><h3>🔍 Select Plants</h3></div>', unsafe_allow_html=True)
    
    # Dropdown for plant selection
    selected_plants = st.multiselect("Select Plants", plant_names, default="All")

    # If "All" is selected, show all plants
    if "All" in selected_plants:
        selected_plants = [p for p in plant_names if p != "All"]

    # Dictionary to store notes
    plant_notes = {}

    st.markdown('<div class="section"><h3>📝 Enter Notes</h3></div>', unsafe_allow_html=True)

    # Create text entry boxes for selected plants
    for plant in selected_plants:
        plant_notes[plant] = st.text_area(f"Notes for {plant}", key=plant)

    # Save button
    if st.button("💾 Save Notes", help="Click to save entered notes"):
        save_plant_notes(plant_notes)
        st.success("✅ Notes saved successfully!")

elif selected_page == "Saved Notes":
    st.markdown('<div class="section"><h3>📜 Saved Notes</h3></div>', unsafe_allow_html=True)
    
    # Display saved notes in a structured format
    saved_notes = read_saved_notes()
    if saved_notes.empty:
        st.info("No notes saved yet!")
    else:
        for _, row in saved_notes.iterrows():
            st.markdown(f'<div class="saved-note"><b>{row["plant_name"]}:</b> {row["note"]}</div>', unsafe_allow_html=True)

    # Add download button
    if os.path.exists(csv_file_path):
        with open(csv_file_path, "rb") as f:
            st.download_button("⬇️ Download Notes", f, file_name="plant_notes.csv", mime="text/csv")
