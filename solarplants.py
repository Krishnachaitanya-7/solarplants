import streamlit as st
import pandas as pd
import os

# Load plant names from Excel
def get_plant_names_from_excel():
    df = pd.read_excel("windplants.xlsx")  # Ensure the file is uploaded in the repo
    return df["plant_name"].tolist()

# Function to save notes to a CSV file
def save_plant_notes_to_csv(plant_notes):
    file_path = "plant_notes.csv"

    # Convert dictionary to DataFrame
    data = [{"plant_name": plant, "note": note} for plant, note in plant_notes.items() if note.strip()]
    
    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)
        df = pd.DataFrame(data)
        df = pd.concat([existing_df, df], ignore_index=True)
    else:
        df = pd.DataFrame(data)

    df.to_csv(file_path, index=False)

# Get plant names
plant_names = get_plant_names_from_excel()
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
    save_plant_notes_to_csv(plant_notes)
    st.success("Notes saved successfully! Check `plant_notes.csv` for records.")
