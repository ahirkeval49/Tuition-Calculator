import streamlit as st
import pandas as pd

# App configuration
st.set_page_config(page_title="UHart Cost Calculator", layout="wide")

# Title and description
st.title("🎓 University of Hartford Graduate Cost Calculator")
st.markdown("**Official 2024-2025 Graduate Program Cost Estimates**")

# Load data (robustly with error handling)
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("TuitionCost.csv")
        df.columns = df.columns.str.strip()

        numeric_cols = ['Per Credit', 'Tuition for 18 Credits', 'Fees', 'Living Expenses']
        for col in numeric_cols:
            df[col] = df[col].replace('[\$,]', '', regex=True).astype(float)

        df['College'] = df['College'].str.strip()
        df['Program'] = df['Program'].str.strip()

        return df
    except FileNotFoundError:
        st.error("⚠️ CSV file not found. Please upload 'TuitionCost.csv' in the app directory.")
        st.stop()
    except KeyError as e:
        st.error(f"⚠️ Missing column in CSV: {e}. Check column names carefully.")
        st.stop()
    except Exception as e:
        st.error(f"⚠️ Error loading data: {e}")
        st.stop()

df = load_data()

# College selection
colleges = sorted(df['College'].dropna().unique())
selected_college = st.selectbox("1. Select College", colleges)

# Program selection based on college
programs = sorted(df[df['College'] == selected_college]['Program'].dropna().unique())
selected_program = st.selectbox("2. Select Program", programs)

# Extracting program data
program_data = df[
    (df['College'] == selected_college) & 
    (df['Program'] == selected_program)
].iloc[0]

# Cost calculation
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Tuition Calculation")
    if pd.notna(program_data['Per Credit']):
        credits = st.number_input(
            "Number of Credits",
            min_value=1,
            max_value=100,
            value=12,
            help="Enter credits per semester"
        )
        tuition = credits * program_data['Per Credit']
    else:
        st.info("Flat rate tuition applied (18 credits).")
        tuition = program_data['Tuition for 18 Credits']

    st.metric("Estimated Tuition", f"${tuition:,.2f}")

with col2:
    st.subheader("Additional Costs")
    fees = program_data['Fees']
    living = program_data['Living Expenses']
    st.write(f"**Mandatory Fees:** ${fees:,.2f}")
    st.write(f"**Living Expenses:** ${living:,.2f}")

    if "Hartt" in selected_college:
        st.write("🎵 + $400 Hartt Annual Fee")
        tuition += 400

    if "ELI" in selected_program:
        st.write("🌐 + $5,386 Student Support Fee")
        tuition += 5386

# Final cost breakdown
total_cost = tuition + fees + living

st.markdown("---")
st.subheader("🧾 Total Estimated Cost")
st.markdown(f"""
```plaintext
Tuition:        ${tuition:>12,.2f}
Fees:           ${fees:>12,.2f}
Living Costs:   ${living:>12,.2f}
---------------------------------
Grand Total:    ${total_cost:>12,.2f}

 ```
 """)
