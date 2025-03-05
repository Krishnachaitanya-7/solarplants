import streamlit as st
import pandas as pd
import pyodbc

# Database connection function
def get_db_connection():
    conn = pyodbc.connect(
        "Driver={SQL Server};"
    "Server=10.88.0.107;"
    "PORT=1433;"
    "Database=Common_FuncDB;"
    "UID=sa;"
    "PWD=GG@cmcs#1;"
    )
    return conn

# Fetch unique plant names from database (modify table name)
def get_plant_names():
    conn = get_db_connection()
    query = "SELECT DISTINCT plant_name FROM Common_FuncDB.dbo.solar_plants_list"
    df = pd.read_sql(query, conn)
    conn.close()
    return df["plant_name"].tolist()

# Function to save notes to database
def save_plant_notes(plant_notes):
    conn = get_db_connection()
    cursor = conn.cursor()

    for plant, note in plant_notes.items():
        if note.strip():  # Save only if note is not empty
            cursor.execute(
                "INSERT INTO plant_notes (plant_name, note) VALUES (?, ?)",
                (plant, note)
            )

    conn.commit()
    conn.close()

# Get plant names from database
plant_names = get_plant_names()
plant_names.insert(0, "All")  # Add "All" option at the top

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

