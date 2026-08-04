import streamlit as st
from dotenv import load_dotenv
import os
import time
import pandas as pd
from google import genai

# ==================== SETUP ====================
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Hospital Analytics Chatbot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS — BRIGHT, POLISHED UI ====================
st.markdown("""
<style>
    /* Overall app background */
    .stApp {
        background-color: #0B0F0D;
    }

    /* Main title styling */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        background: linear-gradient(90deg, #22C55E, #4ADE80, #86EFAC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 16px;
        color: #A1A1AA;
        margin-top: -10px;
        margin-bottom: 25px;
    }

    /* KPI card styling */
    .kpi-card {
        background: linear-gradient(145deg, #111815, #0B0F0D);
        border: 1px solid #1F2A22;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(34, 197, 94, 0.08);
    }

    .kpi-value {
        font-size: 28px;
        font-weight: 800;
        color: #4ADE80;
    }

    .kpi-label {
        font-size: 13px;
        color: #A1A1AA;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }

    /* Chat message bubbles */
    .stChatMessage {
        border-radius: 14px;
        padding: 4px;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #0F1512;
        border-right: 1px solid #1F2A22;
    }

    /* Chat input box */
    .stChatInputContainer {
        border-radius: 14px;
        border: 1px solid #22C55E !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #16A34A, #22C55E);
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: 600;
        padding: 8px 20px;
    }

    .stButton>button:hover {
        background: linear-gradient(90deg, #15803D, #16A34A);
        color: white;
    }

    /* Divider */
    hr {
        border-color: #1F2A22 !important;
    }

    /* Example question chips */
    .example-chip {
        display: inline-block;
        background-color: #14201A;
        border: 1px solid #22C55E;
        color: #4ADE80;
        border-radius: 20px;
        padding: 6px 14px;
        margin: 4px;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== LOAD DATA ====================
appointments = pd.read_csv("cleaned_appointments.csv")
billing = pd.read_csv("cleaned_billing.csv")
doctors = pd.read_csv("cleaned_doctors.csv")
patients = pd.read_csv("cleaned_patients.csv")
treatments = pd.read_csv("cleaned_treatments.csv")

appointments['appointment_date'] = pd.to_datetime(appointments['appointment_date'])

# ==================== PRE-CALCULATED SUMMARY ====================
total_appointments = len(appointments)
total_patients = len(patients)
total_doctors = len(doctors)
no_show_rate = round((appointments['status'] == 'No-show').mean() * 100, 2)
total_revenue = billing['amount'].sum()
date_range = f"{appointments['appointment_date'].min().date()} to {appointments['appointment_date'].max().date()}"

summary_block = f"""
=== QUICK SUMMARY ===
Total Appointments: {total_appointments}
Total Patients: {total_patients}
Total Doctors: {total_doctors}
No-Show Rate: {no_show_rate}%
Total Revenue: ${total_revenue:,.2f}
Data Date Range: {date_range}
"""

# ==================== FULL RAW DATA ====================
raw_data_block = f"""
=== DOCTORS TABLE (full data) ===
{doctors.to_csv(index=False)}

=== PATIENTS TABLE (full data) ===
{patients.to_csv(index=False)}

=== APPOINTMENTS TABLE (full data) ===
{appointments.to_csv(index=False)}

=== TREATMENTS TABLE (full data) ===
{treatments.to_csv(index=False)}

=== BILLING TABLE (full data) ===
{billing.to_csv(index=False)}
"""

# ==================== RETRY-SAFE AI CALL ====================
def ask_ai(question, max_retries=3):
    prompt = f"""
You are a healthcare data analyst assistant. You have access to a summary AND the full raw data tables below.
Use the raw tables to answer ANY question accurately — calculate counts, sums, averages, rankings, or filters yourself from the raw rows if needed.

Rules:
- Use ONLY the data provided below. Never invent names, numbers, or facts not present in this data.
- If a question truly cannot be answered from this data, say so clearly.
- Show your reasoning briefly if you performed a calculation (e.g., "Counting rows where status = 'No-show'...").

{summary_block}

{raw_data_block}

QUESTION: {question}
"""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )
            return response.text
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(5)
            else:
                return f"Sorry, I couldn't get a response right now. Error: {e}"

# ==================== HEADER ====================
st.markdown('<p class="main-title">🏥 Hospital Analytics Chatbot</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Ask any question about appointments, revenue, doctors, branches, treatments, or patients — grounded in the full real dataset.</p>', unsafe_allow_html=True)

# ==================== KPI ROW ====================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{total_appointments}</div>
        <div class="kpi-label">Total Appointments</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{total_patients}</div>
        <div class="kpi-label">Total Patients</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{no_show_rate}%</div>
        <div class="kpi-label">No-Show Rate</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">${total_revenue:,.0f}</div>
        <div class="kpi-label">Total Revenue</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== EXAMPLE QUESTIONS ====================
st.markdown("**💡 Try asking:**")
st.markdown("""
<span class="example-chip">Which branch has the highest no-show rate?</span>
<span class="example-chip">Who is the top revenue-generating doctor?</span>
<span class="example-chip">What's the revenue by payment method?</span>
""", unsafe_allow_html=True)

st.markdown("---")

# ==================== CHAT INTERFACE ====================
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    avatar = "🧑‍💼" if msg["role"] == "user" else "🏥"
    st.chat_message(msg["role"], avatar=avatar).write(msg["content"])

question = st.chat_input("Ask a question about the hospital data...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user", avatar="🧑‍💼").write(question)

    with st.spinner("🔎 Analyzing hospital data..."):
        answer = ask_ai(question)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant", avatar="🏥").write(answer)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## 📊 Data Summary")
    st.markdown(f"""
    <div class="kpi-card" style="text-align:left; margin-bottom: 15px;">
        <b>📅 Date Range</b><br>
        <span style="color:#A1A1AA;">{date_range}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    - 👥 **{total_patients}** patients
    - 🩺 **{total_doctors}** doctors
    - 📅 **{total_appointments}** appointments
    - ⚠️ **{no_show_rate}%** no-show rate
    - 💰 **${total_revenue:,.2f}** total revenue
    """)

    st.markdown("---")
    st.caption("Full raw data tables are also provided to the AI for detailed questions — not just this summary.")

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
