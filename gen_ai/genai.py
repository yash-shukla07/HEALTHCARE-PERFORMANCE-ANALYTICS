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

# ==================== LOAD DATA ====================
appointments = pd.read_csv("cleaned_appointments.csv")
billing = pd.read_csv("cleaned_billing.csv")
doctors = pd.read_csv("cleaned_doctors.csv")
patients = pd.read_csv("cleaned_patients.csv")
treatments = pd.read_csv("cleaned_treatments.csv")

appointments['appointment_date'] = pd.to_datetime(appointments['appointment_date'])

# ==================== PRE-CALCULATED SUMMARY (fast answers for common questions) ====================
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

# ==================== FULL RAW DATA (so the AI can answer ANYTHING, not just pre-picked metrics) ====================
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

# ==================== STREAMLIT UI ====================
st.set_page_config(page_title="Hospital Analytics Chatbot", page_icon="🏥")
st.title("🏥 Hospital Analytics Chatbot")
st.caption("Ask any question about appointments, revenue, doctors, branches, treatments, or patients — grounded in the full real dataset.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

question = st.chat_input("Ask a question about the hospital data...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    with st.spinner("Thinking..."):
        answer = ask_ai(question)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)

with st.sidebar:
    st.subheader("📊 Quick Summary")
    st.text(summary_block)
    st.caption("Full raw data tables are also provided to the AI for detailed questions.")