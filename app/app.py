import streamlit as st
import pandas as pd
from datetime import datetime
import os
from fuzzywuzzy import fuzz

# --- Set page configuration
st.set_page_config(page_title="Data Clarity", layout="centered")

# --- Helper Functions
def log_action(instruction, status):
    """Save the cleaning action to a log file."""
    log_folder = "logs"
    os.makedirs(log_folder, exist_ok=True)
    log_file = os.path.join(log_folder, "cleaning_log.txt")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"{timestamp} | Instruction: '{instruction}' | Status: {status}\n")

def interpret_instruction(instruction, df, threshold=0.4):
    """Interpret flexible cleaning instructions and modify the DataFrame."""
    instruction = instruction.lower()
    cleaned_df = df.copy()

    action_mapping = {
        "remove missing rows": ["remove rows with missing", "delete rows missing", "drop rows missing", "remove empty rows"],
        "drop missing columns": ["drop columns missing", "remove empty columns", "delete columns missing", "drop null columns"],
        "remove duplicates": ["remove duplicates", "delete duplicates", "drop repeated rows", "remove repeated entries"],
        "fill missing": ["fill missing", "fix missing", "replace missing", "fill empty cells"],
        "standardize columns": ["standardize headers", "clean column names", "standardize columns"],
    }

    best_match = None
    best_score = 0

    for action, phrases in action_mapping.items():
        for phrase in phrases:
            score = fuzz.partial_ratio(instruction, phrase)
            if score > best_score:
                best_match = action
                best_score = score

    if best_score < 60:
        return cleaned_df, None

    if best_match == "remove missing rows":
        cleaned_df = cleaned_df.dropna()
        action = "Removed rows with missing values"
    elif best_match == "drop missing columns":
        cleaned_df = cleaned_df.dropna(axis=1, thresh=int((1 - threshold) * len(df)))
        action = f"Dropped columns with more than {threshold*100:.0f}% missing values"
    elif best_match == "remove duplicates":
        cleaned_df = cleaned_df.drop_duplicates()
        action = "Removed duplicate rows"
    elif best_match == "fill missing":
        cleaned_df = cleaned_df.fillna("Unknown")
        action = "Filled missing values with 'Unknown'"
    elif best_match == "standardize columns":
        cleaned_df.columns = cleaned_df.columns.str.strip().str.lower().str.replace(' ', '_')
        action = "Standardized column names"
    else:
        action = None

    return cleaned_df, action

def suggest_corrections():
    """Suggest likely actions when the user's instruction isn't recognized."""
    suggestions = [
        "Remove all rows with missing values",
        "Drop columns with more than 40% missing values",
        "Remove duplicate rows",
        "Fill missing values with 'Unknown'",
        "Standardize column names",
    ]
    message = "⚠️ Instruction not recognized.\n\nYou could try:\n\n"
    message += "\n".join(f"- {s}" for s in suggestions)
    return message

# --- Session State Initialization
if "action_history" not in st.session_state:
    st.session_state.action_history = []
if "current_df" not in st.session_state:
    st.session_state.current_df = None
if "show_cleaned_preview" not in st.session_state:
    st.session_state.show_cleaned_preview = False

# --- Sidebar Layout
with st.sidebar:
    st.header("📜 Action History")
    if st.session_state.action_history:
        for i, record in enumerate(st.session_state.action_history, 1):
            st.write(f"{i}. {record}")
    else:
        st.write("No actions yet.")

# --- UI Layout
st.title("🧹 Data Clarity")
st.subheader("AI-powered data cleaning tool for HR teams")

st.write("""
Upload a CSV file and enter plain-English instructions like:
- "Drop columns missing more than 40%"
- "Remove duplicate rows"
- "Fill missing Salary column with 'Unknown'"
- "Standardize headers"

*Examples: remove duplicates, fill missing values, clean column names, drop empty columns.*
""")

uploaded_file = st.file_uploader("Upload your HR dataset", type=["csv"])

if uploaded_file:
    if st.session_state.current_df is None:
        df = pd.read_csv(uploaded_file)
        st.session_state.original_df = df.copy()
        st.session_state.current_df = df.copy()

    st.success("✅ File uploaded! Here's a quick preview:")
    st.dataframe(st.session_state.current_df.head())

    with st.expander("📊 Dataset Overview", expanded=True):
        df = st.session_state.current_df
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

    st.subheader("🧹 Enter your cleaning instruction:")

    threshold = st.slider(
        "Set missing value threshold for column dropping:",
        min_value=0.0, max_value=1.0, value=0.4, step=0.05
    )

    user_instruction = st.text_input("For example: Remove rows with missing values, Drop empty columns, Standardize headers")
    st.caption("💡 Tip: You can type things like 'drop empty rows', 'remove duplicates', or 'fill missing job titles'.")

    if st.button("Apply Cleaning Instruction"):
        if user_instruction:
            with st.spinner("⚙️ Processing your instruction..."):
                cleaned_df, action = interpret_instruction(user_instruction, st.session_state.current_df, threshold)

            if action:
                st.session_state.current_df = cleaned_df.copy()
                st.session_state.show_cleaned_preview = True
                log_action(user_instruction, f"Success - {action}")
                st.session_state.action_history.append(action)
                st.success(f"🧹 {action}!")
                st.rerun()  # ✅ Corrected refresh here
            else:
                st.warning(suggest_corrections())
                log_action(user_instruction, "Warning - Unsupported instruction")

        else:
            st.warning("⚠️ Please enter or select a cleaning instruction first.")

    if st.session_state.show_cleaned_preview:
        st.subheader("🧽 Cleaned Data Preview:")
        st.dataframe(st.session_state.current_df.head())

        csv = st.session_state.current_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Cleaned Data",
            data=csv,
            file_name='cleaned_data.csv',
            mime='text/csv',
        )

    if st.button("🔄 Reset to Original Data"):
        st.session_state.current_df = st.session_state.original_df.copy()
        st.session_state.action_history = []
        st.session_state.show_cleaned_preview = False
        st.success("✅ Data reset to original upload!")
        st.rerun()  # ✅ Corrected refresh here

else:
    st.info("👆 Please upload a CSV file to begin.")








