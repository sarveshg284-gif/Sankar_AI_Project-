import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from modules.analyzer import analyze_influencers
from modules.email_generator import generate_email

load_dotenv()
st.set_page_config(page_title="AI Influencer Research & Outreach", page_icon="📣", layout="wide")

st.title("📣 AI Influencer Research & Email Outreach")
st.caption("Research leads, score influencer fit, and prepare personalized outreach drafts.")

with st.sidebar:
    st.header("Settings")
    st.write("AI analysis is optional. Without an API key, the app uses transparent rule-based scoring.")
    use_ai = st.toggle("Use Claude AI analysis", value=bool(os.getenv("ANTHROPIC_API_KEY")))
    st.info("Never share or upload your API key. Keep it in your local .env file.")

sample_path = "data/sample_influencers.csv"
if "leads" not in st.session_state:
    st.session_state.leads = pd.read_csv(sample_path)

uploaded = st.file_uploader("Upload influencer CSV (optional)", type=["csv"])
if uploaded:
    try:
        st.session_state.leads = pd.read_csv(uploaded)
        st.success("CSV loaded.")
    except Exception as exc:
        st.error(f"Could not read CSV: {exc}")

df = st.session_state.leads.copy()
st.subheader("1. Influencer lead database")
st.write("Required columns: name, handle, niche, followers, engagement_rate, email, location")
st.dataframe(df, use_container_width=True, hide_index=True)

if st.button("Analyze and score influencers", type="primary"):
    with st.spinner("Analyzing leads..."):
        st.session_state.leads = analyze_influencers(df, use_ai=use_ai)
    st.success("Analysis completed.")

analyzed = st.session_state.leads.copy()
if "score" in analyzed.columns:
    st.subheader("2. Lead scoring")
    st.dataframe(analyzed, use_container_width=True, hide_index=True)
    csv_bytes = analyzed.to_csv(index=False).encode("utf-8")
    st.download_button("Download scored leads (CSV)", csv_bytes, "scored_influencers.csv", "text/csv")

st.subheader("3. Personalized email draft")
if not analyzed.empty:
    names = analyzed["name"].astype(str).tolist()
    selected_name = st.selectbox("Choose an influencer", names)
    row = analyzed[analyzed["name"].astype(str) == selected_name].iloc[0].to_dict()
    brand_name = st.text_input("Your brand / company name", "Sankar Group")
    campaign = st.text_area("Campaign or collaboration details", "We would love to explore a collaboration with you.")
    if st.button("Generate email draft"):
        try:
            draft = generate_email(row, brand_name, campaign)
            st.session_state.email_draft = draft
        except Exception as exc:
            st.error(f"Email generation failed: {exc}")
    if "email_draft" in st.session_state:
        st.text_area("Review and edit before sending", st.session_state.email_draft, height=260)
        st.caption("This app creates drafts only. It does not send emails automatically.")
else:
    st.info("Upload a CSV or use the sample leads to begin.")

st.subheader("4. Outreach tracking")
if "status" not in st.session_state.leads.columns:
    st.session_state.leads["status"] = "Not contacted"
statuses = ["Not contacted", "Draft ready", "Contacted", "Replied", "Interested", "Not interested", "Follow-up due"]
edited = st.data_editor(st.session_state.leads, use_container_width=True, hide_index=True,
                        column_config={"status": st.column_config.SelectboxColumn("status", options=statuses)})
st.session_state.leads = edited
st.download_button("Download CRM data", edited.to_csv(index=False).encode("utf-8"),
                   "influencer_crm.csv", "text/csv")

st.divider()
st.caption("Use publicly available business contact details, respect platform terms, and obtain human approval before outreach.")
