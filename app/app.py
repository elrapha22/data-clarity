import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Set page configuration
st.set_page_config(page_title="Data Clarity", layout="centered")

# Helper function to log actions
def log_action(instruction, status):
    """Save the cleaning action to a log file."""
    log_folder = "logs"
    os.makedirs(log_folder, exist_ok=True)  # Create folder if it doesn't exist
    log_file = os.path.join(log_folder, "cleaning_log.txt")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"{timestamp} | Instruction: '{instruction}' | Status: {status}\n")

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
    # Read the file
    df = pd.read_csv(uploaded_file)
    
    # Success message and data preview
    st.success("✅ File uploaded! Here's a quick preview:")
    st.dataframe(df.head())  # Preview first few rows

    # Dataset Overview
    with st.expander("📊 Dataset Overview", expanded=True):
        st.markdown(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")
        missing_total = df.isnull().sum().sum()
        missing_pct = (missing_total / (df.shape[0] * df.shape[1])) * 100
        st.markdown(f"**Total Missing Values:** {missing_total} ({missing_pct:.2f}%)")

        missing_cols = df.isnull().sum()
        missing_cols = missing_cols[missing_cols > 0]
        if not missing_cols.empty:
            st.markdown("🔍 **Columns with missing values:**")
            st.dataframe(missing_cols)
        else:
            st.markdown("✅ No missing values detected.")

    # User Instruction Input
    st.subheader("🧹 Enter your cleaning instruction:")
    user_instruction = st.text_input("For example: 'Remove all rows with missing employee IDs'")

    # Action Button
    if st.button("Apply Cleaning Instruction"):
        if user_instruction:
            st.info("⚙️ Processing your instruction...")

            cleaned_df = df.copy()  # Work on a copy

            # Very basic interpretation
            if "missing" in user_instruction.lower() and ("row" in user_instruction.lower() or "rows" in user_instruction.lower()):
                cleaned_df = cleaned_df.dropna()
                st.success("🧹 Successfully removed rows with missing values!")
                log_action(user_instruction, "Success - Removed rows with missing values")
            else:
                st.warning("⚠️ Sorry, instruction not recognized yet. Try mentioning 'missing' and 'rows'.")
                log_action(user_instruction, "Warning - Unsupported instruction")

            # Display cleaned data
            st.subheader("🧽 Cleaned Data Preview:")
            st.dataframe(cleaned_df.head())
        else:
            st.warning("⚠️ Please enter a cleaning instruction before clicking the button.")
else:
    st.info("👆 Please upload a CSV file to begin.")





