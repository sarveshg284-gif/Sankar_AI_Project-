# AI-Powered Instagram Influencer Research & Email Outreach

A beginner-friendly Streamlit prototype for organizing influencer leads, scoring their suitability, preparing personalized email drafts, and tracking outreach status.

## Features
- Load the included sample CSV or upload your own CSV.
- Rule-based influencer scoring with a transparent score and category.
- Optional Claude AI analysis when an Anthropic API key is configured.
- Personalized email draft generation (review/edit before sending).
- Simple CRM status tracking and CSV export.
- No automated email sending; a human reviews every message.

## Requirements
- Python 3.10+
- Git (for publishing to GitHub)
- Optional: Anthropic API key for Claude-powered analysis

## Run locally (Windows)
Open Command Prompt in this folder and run:

```bash
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

The app opens in your browser, usually at `http://localhost:8501`.

## Optional Claude setup
1. Copy `.env.example` to `.env`.
2. Add your own Anthropic API key to `.env`.
3. Restart Streamlit and enable **Use Claude AI analysis** in the sidebar.

Never commit `.env` or share your API key. The app falls back to rule-based scoring if Claude is not configured or its request fails.

## CSV format
Required columns:

`name, handle, niche, followers, engagement_rate, email, location`

`engagement_rate` should be a percentage number, e.g. `3.8` means 3.8%.

## Scoring model
The rule-based score is out of 100:
- Engagement rate: up to 40 points
- Audience size: up to 30 points
- Profile/contact completeness: up to 20 points
- Niche relevance (non-empty niche): up to 10 points

This is a demonstration heuristic, not a guarantee of influencer quality. Verify audience authenticity, fit, and contact permissions manually.

## GitHub publishing
Create an empty repository on GitHub, then run these commands from this folder:

```bash
git init
git add .
git commit -m "Initial AI influencer outreach project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/Sankar_AI_Project.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. Do not upload `.env`, credentials, private customer data, or non-public personal information.

## Important limitations
- Instagram profile discovery/scraping is not included. Add data only through permitted sources and in line with Instagram/Meta terms.
- Claude use requires your own API key and may incur API charges.
- Email generation is draft-only. This prototype does not send emails, schedule follow-ups, or read inbox replies.
- Sample rows are fictional demo data. Replace them with verified, permission-appropriate business leads before real use.
