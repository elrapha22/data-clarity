import streamlit as st
import pandas as pd
import sys

# Set page configuration
st.set_page_config(page_title="Data Clarity", layout="centered")

# Title and Description
st.title("🧹 Data Clarity")
st.subheader("AI-powered data cleaning tool for HR teams")

# Instructions
st.write("""
Upload a CSV file, enter a plain-English instruction like:
> "Drop all columns with more than 40% missing values"
...and watch the magic happen.
""")

# Upload Section
uploaded_file = st.file_uploader("Upload your HR dataset", type=["csv"])

# If a file is uploaded
if uploaded_file:
    # Save uploaded file into session state
    if 'df' not in st.session_state:
        st.session_state.df = pd.read_csv(uploaded_file)
    
    df = st.session_state.df

    # Success message and enhanced preview
    st.success("✅ File uploaded! Here's a preview:")
    st.dataframe(df.sample(min(10, len(df))))  # Show random 10 rows or all if less

    # Dataset Overview
    st.subheader("📊 Dataset Overview")
    rows, cols = df.shape
    memory_usage = round(sys.getsizeof(df) / 1024, 2)  # Memory size in KB
    st.write(f"**Rows:** {rows} | **Columns:** {cols} | **Memory Usage:** {memory_usage} KB")

    # Columns Available
    st.subheader("📝 Columns Available")
    st.json(list(df.columns))

    # Missing Values Summary
    st.subheader("❓ Missing Values")
    missing = df.isnull().sum()
    missing_percent = (missing / len(df)) * 100
    missing_summary = pd.DataFrame({
        "Missing Values": missing,
        "Missing %": missing_percent
    }).sort_values(by="Missing %", ascending=False)

    st.dataframe(missing_summary.style.format({"Missing %": "{:.2f}"}))

    # Data Types Overview
    st.subheader("🔍 Data Types")
    st.dataframe(df.dtypes.astype(str))

    # User Instruction Input
    st.subheader("🧹 Enter your cleaning instruction:")
    user_instruction = st.text_input("For example: 'Remove all rows with missing employee IDs'")

    # Action Button
    if st.button("Apply Cleaning Instruction"):
        st.info("⚙️ Processing... (Feature will be active in the next build step)")
        st.write("🛠️ Cleaned data preview will appear here soon.")

else:
    st.info("👆 Please upload a CSV file to begin.")




