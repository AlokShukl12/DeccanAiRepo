from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from agent import TalentScoutingAgent, load_candidates_from_json


app = FastAPI(
    title="Talent Scouting Agent",
    version="1.1.0",
    description="Vercel-compatible interactive UI + API for JD parsing, matching, and shortlist ranking.",
)


DEFAULT_JD = """Senior Applied AI Engineer - Talent Intelligence
Location: Bangalore (Hybrid)
Experience: 4-7 years
Compensation: 24-40 LPA

We are building an AI-powered talent intelligence platform for enterprise recruiting.
Must have:
- Strong Python and SQL fundamentals
- Hands-on experience with LLM, NLP, and machine learning systems
- Production API development with FastAPI or similar
- Cloud deployment experience on AWS/GCP

Good to have:
- LangChain or agentic workflow experience
- Docker/Kubernetes exposure
- Fintech or SaaS domain background
"""


LANDING_PAGE_HTML = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Talent Scouting Agent</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --bg-0: #f4f9fb;
      --bg-1: #eaf2f8;
      --ink-0: #0f2230;
      --ink-1: #314a5e;
      --brand-0: #0f7a8a;
      --brand-1: #0ca678;
      --accent-0: #ff8f3f;
      --card: rgba(255, 255, 255, 0.92);
      --stroke: rgba(15, 39, 61, 0.14);
      --good: #117548;
      --bad: #a42d2d;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{
      margin: 0;
      font-family: "Sora", system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
      color: var(--ink-0);
      background:
        radial-gradient(circle at 8% 6%, #d5edf9 0%, transparent 32%),
        radial-gradient(circle at 95% 2%, #ffe8d5 0%, transparent 36%),
        linear-gradient(180deg, var(--bg-0), var(--bg-1));
    }}
    .shell {{
      max-width: 1160px;
      margin: 0 auto;
      padding: 20px 16px 44px;
    }}
    .hero {{
      border: 1px solid var(--stroke);
      background: linear-gradient(120deg, #ffffffdf, #f6fbffdf);
      border-radius: 18px;
      padding: 18px;
      box-shadow: 0 20px 36px -28px rgba(10, 32, 50, 0.56);
    }}
    .kicker {{
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--brand-0);
      font-weight: 700;
      font-size: 12px;
    }}
    h1 {{
      margin: 4px 0 8px;
      line-height: 1.14;
      font-size: clamp(26px, 4vw, 36px);
    }}
    .sub {{
      color: var(--ink-1);
      font-size: 14px;
      margin-bottom: 8px;
    }}
    .pill {{
      display: inline-block;
      margin-right: 8px;
      margin-bottom: 8px;
      border-radius: 999px;
      padding: 6px 11px;
      color: #fff;
      font-size: 12px;
      font-weight: 600;
      background: linear-gradient(110deg, var(--brand-0), var(--brand-1));
    }}
    .grid {{
      margin-top: 14px;
      display: grid;
      grid-template-columns: 1.5fr .9fr;
      gap: 14px;
    }}
    .card {{
      border: 1px solid var(--stroke);
      border-radius: 14px;
      background: var(--card);
      padding: 14px;
      box-shadow: 0 8px 24px -22px rgba(20, 44, 62, 0.72);
    }}
    .label {{
      font-size: 12px;
      color: #496174;
      font-weight: 600;
      margin-bottom: 6px;
    }}
    textarea {{
      width: 100%;
      min-height: 300px;
      resize: vertical;
      border-radius: 12px;
      border: 1px solid #ccdbe8;
      background: #fcfeff;
      color: #122837;
      font-family: inherit;
      font-size: 13px;
      line-height: 1.5;
      padding: 12px;
      outline: none;
      transition: border-color .2s ease, box-shadow .2s ease;
    }}
    textarea:focus {{
      border-color: #4ca1c4;
      box-shadow: 0 0 0 3px rgba(76, 161, 196, 0.16);
    }}
    .controls {{
      display: grid;
      gap: 10px;
    }}
    .row {{
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 8px;
      align-items: center;
    }}
    input[type="range"] {{ width: 100%; }}
    input, select, button {{
      font-family: inherit;
      font-size: 13px;
    }}
    select {{
      width: 100%;
      border-radius: 10px;
      border: 1px solid #ccdae7;
      background: #fff;
      color: #123043;
      padding: 8px 10px;
    }}
    .btn {{
      width: 100%;
      border: 0;
      border-radius: 12px;
      padding: 11px 12px;
      font-weight: 700;
      cursor: pointer;
      transition: transform .14s ease, filter .2s ease;
    }}
    .btn:hover {{ transform: translateY(-1px); filter: saturate(1.08); }}
    .btn:active {{ transform: translateY(0); }}
    .btn-primary {{
      color: #fff;
      background: linear-gradient(120deg, #0f6f87, #15a579);
    }}
    .btn-secondary {{
      margin-top: 8px;
      color: #214156;
      background: #eef5fa;
      border: 1px solid #d0dfec;
    }}
    .results {{
      margin-top: 14px;
      display: none;
      animation: rise .45s ease;
    }}
    @keyframes rise {{
      from {{ opacity: 0; transform: translateY(8px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    .kpis {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
    }}
    .kpi {{
      border: 1px solid var(--stroke);
      border-radius: 12px;
      background: #ffffffc7;
      padding: 12px;
    }}
    .kpi .t {{
      font-size: 11px;
      color: #577084;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: .06em;
    }}
    .kpi .v {{
      margin-top: 4px;
      font-size: 24px;
      font-weight: 700;
    }}
    .parsed {{
      margin-top: 12px;
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }}
    .chip {{
      display: inline-block;
      margin-right: 6px;
      margin-bottom: 6px;
      border-radius: 999px;
      padding: 4px 9px;
      border: 1px solid #d6e3ed;
      background: #f7fbff;
      color: #22475d;
      font-size: 12px;
      font-weight: 600;
    }}
    .table-wrap {{
      overflow-x: auto;
      border: 1px solid var(--stroke);
      border-radius: 12px;
      background: #fff;
      margin-top: 10px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}
    th, td {{
      text-align: left;
      padding: 10px;
      border-bottom: 1px solid #e6eef6;
      white-space: nowrap;
    }}
    th {{
      font-size: 11px;
      letter-spacing: .05em;
      text-transform: uppercase;
      color: #4e697d;
      background: #f8fbfe;
    }}
    .candidate-list {{
      margin-top: 10px;
      display: grid;
      gap: 10px;
    }}
    details {{
      border: 1px solid var(--stroke);
      border-radius: 12px;
      background: #ffffffd2;
      padding: 10px 12px;
    }}
    summary {{
      cursor: pointer;
      list-style: none;
      font-weight: 700;
      display: flex;
      justify-content: space-between;
      gap: 8px;
    }}
    summary::-webkit-details-marker {{
      display: none;
    }}
    .scoreline {{
      color: #355166;
      font-size: 12px;
      font-weight: 600;
    }}
    .signals {{
      margin-top: 10px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }}
    .signal-good {{
      color: var(--good);
      font-size: 13px;
      margin-bottom: 6px;
      font-weight: 600;
    }}
    .signal-bad {{
      color: var(--bad);
      font-size: 13px;
      margin-bottom: 6px;
      font-weight: 600;
    }}
    .chat {{
      margin-top: 10px;
      display: grid;
      gap: 8px;
    }}
    .bubble {{
      border-radius: 10px;
      padding: 8px 10px;
      font-size: 13px;
      line-height: 1.45;
      max-width: 86%;
    }}
    .bubble.r {{
      justify-self: end;
      background: #d9f5ef;
      border: 1px solid #b3e7da;
    }}
    .bubble.c {{
      justify-self: start;
      background: #eef3f8;
      border: 1px solid #dbe6f0;
    }}
    .status {{
      margin-top: 10px;
      font-size: 13px;
      color: #355167;
      min-height: 18px;
    }}
    .err {{
      color: #a42d2d;
      font-weight: 600;
    }}
    .footer-note {{
      margin-top: 14px;
      font-size: 12px;
      color: #516c80;
    }}
    @media (max-width: 980px) {{
      .grid {{ grid-template-columns: 1fr; }}
      .kpis {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .parsed {{ grid-template-columns: 1fr; }}
      .signals {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <div class="kicker">Recruiter Workspace</div>
      <h1>AI-Powered Talent Scouting and Engagement</h1>
      <div class="sub">Paste a JD, run the agent, and get an explainable shortlist ranked by Match Score and Interest Score.</div>
      <span class="pill">Explainable matching</span>
      <span class="pill">Simulated outreach</span>
      <span class="pill">Action-ready shortlist</span>
    </section>

    <section class="grid">
      <article class="card">
        <div class="label">Job Description</div>
        <textarea id="jdText">{DEFAULT_JD}</textarea>
      </article>
      <aside class="card">
        <div class="controls">
          <div>
            <div class="label">Discovery pool size</div>
            <div class="row">
              <input id="poolSize" type="range" min="5" max="18" step="1" value="12" />
              <strong id="poolSizeV">12</strong>
            </div>
          </div>
          <div>
            <div class="label">Final shortlist size</div>
            <div class="row">
              <input id="shortlistSize" type="range" min="3" max="15" step="1" value="8" />
              <strong id="shortlistSizeV">8</strong>
            </div>
          </div>
          <div>
            <div class="label">Match weight (%)</div>
            <div class="row">
              <input id="matchWeight" type="range" min="40" max="90" step="5" value="65" />
              <strong id="matchWeightV">65</strong>
            </div>
          </div>
          <div>
            <div class="label">Outreach tone</div>
            <select id="tone">
              <option value="consultative">consultative</option>
              <option value="direct">direct</option>
              <option value="mission-led">mission-led</option>
            </select>
          </div>
          <button id="runBtn" class="btn btn-primary">Run Scouting Agent</button>
          <button id="resetBtn" class="btn btn-secondary">Reset to Sample JD</button>
          <div id="status" class="status"></div>
        </div>
      </aside>
    </section>

    <section id="results" class="results">
      <div class="kpis">
        <div class="kpi"><div class="t">Candidates</div><div id="kCount" class="v">-</div></div>
        <div class="kpi"><div class="t">Avg Match</div><div id="kMatch" class="v">-</div></div>
        <div class="kpi"><div class="t">Avg Interest</div><div id="kInterest" class="v">-</div></div>
        <div class="kpi"><div class="t">Top Combined</div><div id="kTop" class="v">-</div></div>
      </div>

      <div class="parsed">
        <article class="card">
          <div class="label">Parsed JD Snapshot</div>
          <div id="parsedSummary"></div>
        </article>
        <article class="card">
          <div class="label">Extracted Signals</div>
          <div id="parsedSignals"></div>
        </article>
      </div>

      <article class="card" style="margin-top:10px;">
        <div class="label">Ranked Shortlist</div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Rank</th>
                <th>Candidate</th>
                <th>Title</th>
                <th>Location</th>
                <th>Match</th>
                <th>Interest</th>
                <th>Combined</th>
              </tr>
            </thead>
            <tbody id="tableBody"></tbody>
          </table>
        </div>
      </article>

      <article class="card" style="margin-top:10px;">
        <div class="label">Candidate Explainability and Conversations</div>
        <div id="candidateList" class="candidate-list"></div>
      </article>
    </section>

    <p class="footer-note">API endpoints remain available at <code>/scout</code> and <code>/health</code>.</p>
  </main>

  <script>
    const $ = (id) => document.getElementById(id);

    const poolSize = $("poolSize");
    const shortlistSize = $("shortlistSize");
    const matchWeight = $("matchWeight");
    const jdText = $("jdText");
    const runBtn = $("runBtn");
    const resetBtn = $("resetBtn");
    const statusEl = $("status");
    const resultsEl = $("results");
    const toneEl = $("tone");

    function bindRange(inputEl, valueEl) {{
      const target = $(valueEl);
      const sync = () => target.textContent = inputEl.value;
      inputEl.addEventListener("input", sync);
      sync();
    }}

    bindRange(poolSize, "poolSizeV");
    bindRange(shortlistSize, "shortlistSizeV");
    bindRange(matchWeight, "matchWeightV");

    resetBtn.addEventListener("click", () => {{
      jdText.value = {DEFAULT_JD!r};
      statusEl.textContent = "Sample JD loaded.";
      statusEl.classList.remove("err");
    }});

    function avg(values) {{
      if (!values.length) return 0;
      return values.reduce((a, b) => a + b, 0) / values.length;
    }}

    function esc(text) {{
      const div = document.createElement("div");
      div.innerText = String(text ?? "");
      return div.innerHTML;
    }}

    function chipList(arr) {{
      if (!arr || !arr.length) return "<span class=\\"chip\\">none</span>";
      return arr.map((s) => `<span class="chip">${{esc(s)}}</span>`).join("");
    }}

    function renderResult(data) {{
      const shortlist = data.shortlist || [];
      const parsed = data.parsed_jd || {{}};

      $("kCount").textContent = shortlist.length;
      $("kMatch").textContent = avg(shortlist.map((x) => x.match_score)).toFixed(2);
      $("kInterest").textContent = avg(shortlist.map((x) => x.interest_score)).toFixed(2);
      $("kTop").textContent = shortlist.length ? Math.max(...shortlist.map((x) => x.combined_score)).toFixed(2) : "0.00";

      $("parsedSummary").innerHTML = `
        <div><b>Role:</b> ${{esc(parsed.title || "Not specified")}}</div>
        <div><b>Experience:</b> ${{esc(parsed.min_experience_years ?? "-")}} to ${{esc(parsed.max_experience_years ?? "-")}}</div>
        <div><b>Location:</b> ${{esc(parsed.location || "Not specified")}}</div>
        <div><b>Work model:</b> ${{esc(parsed.work_model || "Not specified")}}</div>
        <div><b>Compensation:</b> ${{esc(parsed.min_ctc_lpa ?? "-")}} to ${{esc(parsed.max_ctc_lpa ?? "-")}} LPA</div>
      `;

      $("parsedSignals").innerHTML = `
        <div class="label">Must-have skills</div>
        <div>${{chipList(parsed.must_have_skills)}}</div>
        <div class="label" style="margin-top:8px;">Good-to-have skills</div>
        <div>${{chipList(parsed.good_to_have_skills)}}</div>
        <div class="label" style="margin-top:8px;">Domain tags</div>
        <div>${{chipList(parsed.domains)}}</div>
      `;

      $("tableBody").innerHTML = shortlist.map((item, i) => `
        <tr>
          <td>${{i + 1}}</td>
          <td>${{esc(item.name)}}</td>
          <td>${{esc(item.title)}}</td>
          <td>${{esc(item.location)}}</td>
          <td>${{Number(item.match_score).toFixed(2)}}</td>
          <td>${{Number(item.interest_score).toFixed(2)}}</td>
          <td>${{Number(item.combined_score).toFixed(2)}}</td>
        </tr>
      `).join("");

      $("candidateList").innerHTML = shortlist.map((item, i) => {{
        const positive = (item.interest_signals?.positive || []).map((s) => `<div class="signal-good">+ ${{esc(s)}}</div>`).join("");
        const negativeRaw = item.interest_signals?.negative || [];
        const negative = negativeRaw.length
          ? negativeRaw.map((s) => `<div class="signal-bad">- ${{esc(s)}}</div>`).join("")
          : '<div class="signal-good">+ No obvious blockers detected</div>';
        const transcript = (item.transcript || []).map((turn) => {{
          const cls = turn.speaker === "Recruiter" ? "r" : "c";
          const who = turn.speaker === "Recruiter" ? "Recruiter" : "Candidate";
          return `<div class="bubble ${{cls}}"><b>${{who}}:</b> ${{esc(turn.message)}}</div>`;
        }}).join("");
        return `
          <details>
            <summary>
              <span>${{i + 1}}. ${{esc(item.name)}} - ${{esc(item.title)}}</span>
              <span class="scoreline">Match ${{Number(item.match_score).toFixed(1)}} | Interest ${{Number(item.interest_score).toFixed(1)}} | Combined ${{Number(item.combined_score).toFixed(1)}}</span>
            </summary>
            <div style="margin-top:8px;">
              <div><b>Why matched:</b></div>
              <ul>
                ${{(item.explanations || []).map((e) => `<li>${{esc(e)}}</li>`).join("")}}
              </ul>
              <div class="signals">
                <div>
                  <div class="label">Positive signals</div>
                  ${{positive}}
                </div>
                <div>
                  <div class="label">Risk signals</div>
                  ${{negative}}
                </div>
              </div>
              <div class="label" style="margin-top:10px;">Conversation transcript</div>
              <div class="chat">${{transcript}}</div>
            </div>
          </details>
        `;
      }}).join("");

      resultsEl.style.display = "block";
      window.scrollTo({{ top: resultsEl.offsetTop - 14, behavior: "smooth" }});
    }}

    async function runAgent() {{
      const jd = jdText.value.trim();
      if (jd.length < 20) {{
        statusEl.textContent = "Please add a fuller Job Description (minimum 20 characters).";
        statusEl.classList.add("err");
        return;
      }}

      const match = Number(matchWeight.value) / 100;
      const interest = 1 - match;

      statusEl.textContent = "Running agent pipeline...";
      statusEl.classList.remove("err");
      runBtn.disabled = true;
      runBtn.textContent = "Running...";

      try {{
        const resp = await fetch("/scout", {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{
            jd_text: jd,
            pool_size: Number(poolSize.value),
            shortlist_size: Number(shortlistSize.value),
            match_weight: match,
            interest_weight: interest,
            outreach_tone: toneEl.value
          }})
        }});

        if (!resp.ok) {{
          const errData = await resp.json().catch(() => ({{}}));
          throw new Error(errData.detail || `Request failed with status ${{resp.status}}`);
        }}

        const data = await resp.json();
        renderResult(data);
        statusEl.textContent = "Completed. Shortlist generated.";
      }} catch (err) {{
        statusEl.textContent = `Run failed: ${{err.message || err}}`;
        statusEl.classList.add("err");
      }} finally {{
        runBtn.disabled = false;
        runBtn.textContent = "Run Scouting Agent";
      }}
    }}

    runBtn.addEventListener("click", runAgent);
  </script>
</body>
</html>
"""


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


@app.get("/", response_class=HTMLResponse)
def root() -> str:
    return LANDING_PAGE_HTML


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


@app.post("/api/scout")
def scout_alias(req: ScoutRequest) -> dict[str, Any]:
    return scout(req)
