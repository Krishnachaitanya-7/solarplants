import streamlit as st
import pandas as pd
import os

# File path for local storage
csv_file_path = "plant_notes.csv"

# Function to read saved notes
def read_saved_notes():
    if os.path.exists(csv_file_path):
        return pd.read_csv(csv_file_path)
    return pd.DataFrame(columns=["plant_name", "note"])

# Function to save notes to CSV
def save_plant_notes(plant_notes):
    # Convert dictionary to DataFrame
    new_data = pd.DataFrame(plant_notes.items(), columns=["plant_name", "note"])

    # Load existing data
    if os.path.exists(csv_file_path):
        existing_data = pd.read_csv(csv_file_path)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    # Save to CSV
    updated_data.to_csv(csv_file_path, index=False)

# Load existing plant names from an Excel sheet
def load_plant_names():
    excel_file = "windplants.xlsx"  # Ensure this file exists in the same directory
    df = pd.read_excel(excel_file)
    return df["plant_name"].tolist()

# Get plant names from Excel
plant_names = load_plant_names()
plant_names.insert(0, "All")  # Add "All" option

# Streamlit UI
st.title("Plant Information Dashboard")

# Dropdown for plant selection
selected_plants = st.multiselect("Select Plants", plant_names, default="All")

# If "All" is selected, show all plants
if "All" in selected_plants:
    selected_plants = [p for p in plant_names if p != "All"]

# Dictionary to store notes
plant_notes = {}

st.markdown("### Enter Notes for Selected Plants")

# Create text entry boxes for selected plants
for plant in selected_plants:
    plant_notes[plant] = st.text_area(f"Notes for {plant}", key=plant)

# Save button
if st.button("Save Notes"):
    save_plant_notes(plant_notes)
    st.success("Notes saved successfully!")

# Display saved notes
st.markdown("### Saved Notes")
saved_notes = read_saved_notes()
st.dataframe(saved_notes)

# Add download button
if os.path.exists(csv_file_path):
    with open(csv_file_path, "rb") as f:
        st.download_button("Download Notes", f, file_name="plant_notes.csv", mime="text/csv")
