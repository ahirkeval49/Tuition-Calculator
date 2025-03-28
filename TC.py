import streamlit as st
import pandas as pd

# Load data from GitHub using the raw URL
@st.cache_data
def load_data():
    
    df = pd.read_csv("TuitionCost.csv")

    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Now use the EXACT column names found
    df['Per Credit'] = df['Per Credit'].replace('[\$,]', '', regex=True).astype(float)
    df['Tuition for 18 Credits'] = df['Tuition for 18 Credits'].replace('[\$,]', '', regex=True).astype(float)
    df['Fees'] = df['Fees'].replace('[\$,]', '', regex=True).astype(float)
    df['Living Expenses'] = df['Living Expenses'].replace('[\$,]', '', regex=True).astype(float)

    return dff

df = load_data()

# Streamlit App
st.set_page_config(page_title="UHart Cost Calculator", layout="wide")

st.title("🎓 University of Hartford Graduate Cost Calculator")
st.markdown("**Official 2024-2025 Graduate Program Cost Estimates**")

# College Selection
colleges = [col for col in df['College'].unique() if pd.notna(col)]
selected_college = st.selectbox(
    "1. Select College", 
    options=colleges,
    help="Choose your academic college/school"
)

# Program Selection
programs = df[df['College'] == selected_college]['Program'].unique()
selected_program = st.selectbox(
    "2. Select Program", 
    options=programs,
    help="Choose your specific graduate program"
)

# Get Program Data
program_data = df[(df['College'] == selected_college) & 
                  (df['Program'] == selected_program)].iloc[0]

# Cost Calculation
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Tuition Details")
    
    if pd.notna(program_data['Per Credit']):
        credits = st.number_input(
            "Number of Credits",
            min_value=1,
            max_value=100,
            value=12,
            help="Enter your planned credits per semester"
        )
        tuition = credits * program_data['Per Credit']
    else:
        st.write("**Flat Rate Program**")
        tuition = program_data['Tuition for 18 Credits']
    
    st.metric("Estimated Tuition", f"${tuition:,.2f}")

with col2:
    st.subheader("Additional Costs")
    st.write(f"**Mandatory Fees:** ${program_data['Fees']:,.2f}")
    st.write(f"**Living Expenses:** ${program_data['Living Expenses']:,.2f}")
    
    # Special cases
    if "Hartt" in selected_college:
        st.write("+ Additional $400/year Hartt fee")
        tuition += 400
        
    if "ELI" in selected_program:
        st.write("+ $5,386 Student Support Fee")
        tuition += 5386

# Total Calculation
st.markdown("---")
total_cost = tuition + program_data['Fees'] + program_data['Living Expenses']

st.subheader("Total Estimated Cost")
st.markdown(f"""
```plaintext
Tuition:       ${tuition:>10,.2f}
Fees:          ${program_data['Fees']:>10,.2f}
Living Costs:  ${program_data['Living Expenses']:>10,.2f}
--------------------------------
Grand Total:   ${total_cost:>10,.2f}
 ```
 """)
