import streamlit as st
import pandas as pd

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

# Initialize session state for user instructions if it doesn't exist
if "instructions_log" not in st.session_state:
    st.session_state["instructions_log"] = []

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
    with st.expander("📊 Dataset Overview", expanded=False):
        st.write(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")
        total_missing = df.isnull().sum().sum()
        missing_percent = (total_missing / (df.shape[0] * df.shape[1])) * 100
        st.write(f"**Total Missing Values:** {total_missing} ({missing_percent:.2f}%)")

    # Columns Available
    with st.expander("📝 Columns Available", expanded=False):
        st.write(df.columns.tolist())

    # Missing Values Summary
    with st.expander("❓ Missing Values", expanded=False):
        missing_summary = df.isnull().sum()
        missing_cols = missing_summary[missing_summary > 0]
        if not missing_cols.empty:
            st.dataframe(missing_cols)
        else:
            st.write("✅ No missing values detected.")

    # User Instruction Input
    st.subheader("🧹 Enter your cleaning instruction:")
    user_instruction = st.text_input("For example: 'Remove all rows with missing employee IDs'")

    # Action Button
    if st.button("Apply Cleaning Instruction"):
        if user_instruction:
            # Save user instruction to session state
            st.session_state["instructions_log"].append(user_instruction)
            st.success("✅ Instruction received!")
            
            # Display the received instruction
            st.write(f"📝 **Interpreted Instruction:** {user_instruction}")
        else:
            st.warning("⚠️ Please enter a cleaning instruction.")

    # Display History of Instructions
    if st.session_state["instructions_log"]:
        with st.expander("🗒️ Cleaning Instructions Log"):
            for idx, inst in enumerate(st.session_state["instructions_log"], 1):
                st.write(f"{idx}. {inst}")

else:
    st.info("👆 Please upload a CSV file to begin.")






