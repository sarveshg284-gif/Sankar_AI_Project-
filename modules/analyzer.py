import os
import json
import pandas as pd

REQUIRED_COLUMNS = ["name", "handle", "niche", "followers", "engagement_rate", "email", "location"]

def _rule_score(row):
    engagement = max(0.0, min(float(row.get("engagement_rate", 0) or 0), 10.0))
    followers = max(0, int(float(row.get("followers", 0) or 0)))
    engagement_points = min(40.0, engagement * 8.0)
    follower_points = 30.0 if 10_000 <= followers <= 200_000 else (20.0 if followers > 0 else 0.0)
    completeness_points = 20.0 if str(row.get("email", "")).strip() else 10.0
    niche_points = 10.0 if str(row.get("niche", "")).strip() else 0.0
    score = round(engagement_points + follower_points + completeness_points + niche_points)
    label = "High" if score >= 75 else ("Medium" if score >= 50 else "Low")
    return score, label

def analyze_influencers(df: pd.DataFrame, use_ai: bool = False) -> pd.DataFrame:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError("Missing required CSV columns: " + ", ".join(missing))

    result = df.copy()
    result["followers"] = pd.to_numeric(result["followers"], errors="coerce").fillna(0).astype(int)
    result["engagement_rate"] = pd.to_numeric(result["engagement_rate"], errors="coerce").fillna(0.0)
    scores = result.apply(_rule_score, axis=1)
    result["score"] = [s[0] for s in scores]
    result["fit_category"] = [s[1] for s in scores]
    result["analysis"] = result.apply(
        lambda r: f"{r['fit_category']} priority based on engagement, audience size, profile completeness and niche information.",
        axis=1
    )

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if use_ai and api_key:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            for idx, row in result.iterrows():
                prompt = (
                    "Assess this influencer lead for a potential brand collaboration. "
                    "Return concise plain text with strengths, risks, and a recommendation. "
                    "Do not invent facts. Data: " + json.dumps(row.to_dict(), default=str)
                )
                response = client.messages.create(
                    model="claude-3-5-haiku-latest",
                    max_tokens=180,
                    messages=[{"role": "user", "content": prompt}]
                )
                result.at[idx, "analysis"] = response.content[0].text
        except Exception as exc:
            result["analysis"] = result["analysis"] + f" (Claude unavailable; rule-based result used: {type(exc).__name__})"
    elif use_ai and not api_key:
        result["analysis"] = result["analysis"] + " (Add ANTHROPIC_API_KEY to .env to enable Claude.)"

    return result
