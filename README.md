<div align="center">

# 🏥 Healthcare Performance Analytics

### End-to-End Hospital Operations, Financial & Risk Analysis Dashboard

*Built with Python • SQL • Power BI • Google Gemini AI*

[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](#-dashboard-preview)
[![SQL](https://img.shields.io/badge/SQL-Analysis-4479A1?style=for-the-badge&logo=postgresql&logoColor=white)](#-project-structure)
[![Python](https://img.shields.io/badge/Python-Cleaning-2E8B57?style=for-the-badge&logo=python&logoColor=white)](#-project-structure)
[![GenAI](https://img.shields.io/badge/GenAI-Insight%20Chatbot-8B5CF6?style=for-the-badge&logo=google&logoColor=white)](#-ai-powered-insight-chatbot)

</div>

---

## 📌 Overview

This project analyzes a multi-table hospital dataset — **appointments, billing, doctors, patients, and treatments** — to answer one core operational question:

> **"Where is the hospital losing capacity and revenue, and what should management do about it?"**

The dashboard follows an end-to-end pipeline — **Python cleaning → SQL relational modeling → Power BI dashboard → GenAI-powered chatbot** — moving beyond simple reporting into genuine operational and financial insight generation.

---

## 🎯 Key Metrics

<table>
<tr><th>Metric</th><th>Value</th></tr>
<tr><td>Total Appointments</td><td><b>200</b></td></tr>
<tr><td>Total Patients</td><td><b>48</b></td></tr>
<tr><td>Total Doctors</td><td><b>10</b></td></tr>
<tr><td>No-Show Rate</td><td><b>26.0%</b></td></tr>
<tr><td>Total Revenue</td><td><b>$551.25K</b></td></tr>
<tr><td>Avg. Revenue per Appointment</td><td><b>$2.76K</b></td></tr>
</table>

> **Bottom line:** Portfolio risk isn't in appointment volume — it's concentrated in no-show behavior at specific branches and doctor workload imbalance, both directly addressable through targeted operational changes.

---

## 🖥️ Dashboard Preview

<details open>
<summary><b>📅 Page 1 — Appointment Analysis</b></summary>
<br>

Operational view: monthly appointment trends, doctor workload, patient demographics, branch performance, and no-show rate by branch.

<img src="screenshots/Appointment page ss .png" alt="Appointment Analysis Dashboard" width="100%">

</details>

<details>
<summary><b>💰 Page 2 — Financial Analysis</b></summary>
<br>

Revenue breakdown by age group, payment method, insurance provider, and treatment type — connecting financial performance to patient and operational data.

<img src="screenshots/financial page ss .png" alt="Financial Analysis Dashboard" width="100%">

</details>

<details>
<summary><b>💡 Page 3 — Key Insights & Recommendations</b></summary>
<br>

Synthesized operational and financial insights paired with four targeted action cards — the analytical conclusion of the dashboard.

<img src="screenshots/Insight page ss .png" alt="Key Insights Dashboard" width="100%">

</details>

---

## 💡 Key Insights

<table>
<tr>
<td valign="top" width="50%">

**📅 Operational**
- April recorded the highest appointment volume; September was the lowest — a clear seasonal booking pattern
- Central Hospital has the highest no-show rate (~30%) among all branches
- Overall no-show rate stands at 26% — roughly 1 in 4 appointments are missed
- Doctor workload varies significantly across the roster

</td>
<td valign="top" width="50%">

**💰 Financial**
- Chemotherapy generates the highest treatment revenue, followed by MRI
- MedCare Plus leads insurance-driven revenue among all providers
- Credit card is the top-contributing payment method by revenue
- Revenue is diversified across treatments and insurers, reducing single-source dependency risk

</td>
</tr>
</table>

## 🛠️ Recommended Actions

<table>
<tr><th>Action</th><th>Focus</th></tr>
<tr><td>🔴 <b>Reduce No-Shows</b></td><td>Target Central Hospital's high no-show rate with reminders and confirmations</td></tr>
<tr><td>🟠 <b>Optimize Staffing</b></td><td>Align doctor availability with patient demand across branches</td></tr>
<tr><td>🟢 <b>Improve Low-Demand Periods</b></td><td>Use targeted campaigns during low-booking months</td></tr>
<tr><td>🔵 <b>Focus on High-Value Services</b></td><td>Prioritize capacity for Chemotherapy and MRI, the highest-revenue treatments</td></tr>
</table>

---

## 🤖 AI-Powered Insight Chatbot

Beyond the static dashboard, this project includes a **Google Gemini-powered chatbot** that answers natural-language questions about the hospital data — grounded entirely in the real dataset.

**Example questions it can answer:**

"Which branch has the highest no-show rate?"
"Who is the top revenue-generating doctor?"
"What's the revenue breakdown by payment method?"


### 🛡️ Design highlight: hallucination prevention

<blockquote>
An early version of this chatbot fabricated a fictional clinic name and a doctor's last name when given incomplete prompt context. This was caught through manual verification against ground-truth calculations, then fixed by:

1. Injecting **real, calculated values** into every prompt — never placeholders
2. Adding an explicit constraint: <i>"Using ONLY the data provided. Do not invent any names, numbers, or details not explicitly given."</i>
3. Verifying every subsequent output against independently calculated Python values before trusting it

This is a genuine, tested safeguard — not a theoretical claim.
</blockquote>

---

## 🗂️ Project Structure

Hospital-Analytics/
│
├── 01-dataset/ # Raw hospital data (appointments, billing, doctors, patients, treatments)
├── 02-python/ # Data cleaning & preprocessing scripts
├── 03-sql/ # SQL relational schema & analysis queries
├── 04-power-bi/ # Power BI dashboard (.pbix)
├── screenshots/ # Dashboard page exports
├── 06-genai-chatbot/ # Streamlit + Gemini API insight chatbot
└── README.md


---

## 🛠️ Pipeline & Tech Stack

<table>
<tr><th>Stage</th><th>Tool</th><th>Description</th></tr>
<tr><td>🧹 Cleaning</td><td><b>Python (Pandas)</b></td><td>Date/time parsing, dtype correction, deduplication, phone number formatting</td></tr>
<tr><td>🗄️ Modeling</td><td><b>MySQL</b></td><td>Relational schema with primary/foreign keys across 5 tables</td></tr>
<tr><td>🔎 Analysis</td><td><b>SQL</b></td><td>JOINs, window functions (DENSE_RANK), aggregations across the full appointment→treatment→billing chain</td></tr>
<tr><td>📊 Dashboard</td><td><b>Power BI</b></td><td>Multi-page dashboard with DAX measures, conditional formatting, cross-page navigation</td></tr>
<tr><td>🤖 AI Layer</td><td><b>Google Gemini API + Streamlit</b></td><td>Natural-language Q&A grounded in real data, with retry logic and anti-hallucination constraints</td></tr>
<tr><td>🗃️ Version Control</td><td><b>Git & GitHub</b></td><td>Project tracking and hosting</td></tr>
</table>

---

## 📈 Data Modeling Notes

- **Relational schema**: `doctors → appointments → treatments → billing`, with `patients` linked via `appointments`. All joins strictly follow this foreign-key chain — a common bug during development involved joining `appointments` directly to `billing` via `patient_id`, skipping `treatments`, which silently duplicated and inflated revenue figures. Fixed by always routing through the correct intermediate table.
- **Time data handling**: `appointment_time` is stored as a true time-only value, avoiding a default-date artifact that would have misrepresented every appointment as occurring "today."
- **Date format correction**: Source dates were in `DD-MM-YYYY` format; explicit format parsing was required to prevent silent day/month swapping for any date where the day value was ≤ 12.

---

## 🚧 Known Limitations

- Dataset is a fixed snapshot (200 appointments); no live/streaming data source
- The GenAI chatbot currently reads pre-cleaned CSVs directly — not yet connected to a live database
- No direct age column in the source data; age-group revenue is derived from date of birth

---

## 🚀 How to View

**1. Quick look:** Browse the `screenshots/` folder for static page exports.

**2. Full interactivity:** Download `04-power-bi/*.pbix` and open in <a href="https://powerbi.microsoft.com/desktop/">Power BI Desktop</a> (free).

**3. Try the AI chatbot:**
```bash
cd 06-genai-chatbot
pip install streamlit google-genai python-dotenv pandas
streamlit run hospital_chatbot.py
```

---

<div align="center">

**Built by <a href="https://github.com/yash-shukla07">Yash Shukla</a>**

⭐ If this project was useful or interesting, consider starring the repo!

</div>
