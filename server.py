from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from agent import TalentScoutingAgent, load_candidates_from_json


app = FastAPI(
    title="Talent Scouting Agent API",
    version="1.0.0",
    description="Vercel-compatible API entrypoint for JD parsing, matching, and shortlist ranking.",
)


class ScoutRequest(BaseModel):
    jd_text: str = Field(..., min_length=20, description="Full job description text.")
    pool_size: int = Field(12, ge=5, le=50)
    shortlist_size: int = Field(8, ge=3, le=30)
    match_weight: float = Field(0.65, ge=0.0, le=1.0)
    interest_weight: float = Field(0.35, ge=0.0, le=1.0)
    outreach_tone: str = Field("consultative")


def _load_agent() -> TalentScoutingAgent:
    data_path = Path(__file__).resolve().parent / "data" / "candidates.json"
    candidates = load_candidates_from_json(data_path)
    return TalentScoutingAgent(candidates=candidates)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "Talent Scouting Agent API",
        "hint": "POST /scout with {'jd_text': '...'}",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/scout")
def scout(req: ScoutRequest) -> dict[str, Any]:
    try:
        agent = _load_agent()
        parsed = agent.parse_jd(req.jd_text)
        matched = agent.discover_and_match(parsed, candidate_pool_size=req.pool_size)
        engaged = agent.simulate_outreach(matched, parsed, tone=req.outreach_tone)
        shortlist = agent.rank_shortlist(
            engaged_candidates=engaged,
            match_weight=req.match_weight,
            interest_weight=req.interest_weight,
            shortlist_size=req.shortlist_size,
        )
        return {
            "parsed_jd": parsed.to_dict(),
            "shortlist": shortlist,
            "count": len(shortlist),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {exc}") from exc
