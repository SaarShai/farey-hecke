"""
Day-1 / Day-2 close: extract JSON from each agent's response, merge into a
single review markdown + structured combined.json.

Each MiMo response has `content: [{type: thinking, ...}, {type: text, text: "..."}]`.
The text block usually contains a fenced ```json ... ``` block which is the
parsed agent output (per the prompts' Output Format sections).

Usage:
    python synthesize.py --day 1   # writes results/d2_numerics_draft.md
    python synthesize.py --day 2   # writes results/d2_d3_final_draft.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

DAY1 = ["agent_A_sieve_xcheck", "agent_B_asymptotic", "agent_C_lvalue_cert", "agent_D_deltaff_null"]
DAY2 = ["agent_E_s3_sweep", "agent_F_mrho_artin", "agent_G_lean_stub", "agent_H_adversarial"]

JSON_BLOCK_RE = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)


def extract_text(response: dict) -> str:
    parts = []
    for block in response.get("content", []):
        if block.get("type") == "text":
            parts.append(block.get("text", ""))
    return "\n".join(parts)


def extract_thinking(response: dict) -> str:
    parts = []
    for block in response.get("content", []):
        if block.get("type") == "thinking":
            parts.append(block.get("thinking", ""))
    return "\n".join(parts)


def extract_json(text: str) -> tuple[dict | None, str]:
    matches = JSON_BLOCK_RE.findall(text)
    if not matches:
        return None, "no ```json``` fence found"
    last = matches[-1]
    try:
        return json.loads(last), "ok"
    except json.JSONDecodeError as e:
        return None, f"JSON parse error: {e}"


def load_agent(name: str) -> dict:
    p = RESULTS / f"{name}.json"
    if not p.exists():
        return {"_missing": True, "_path": str(p)}
    raw = json.loads(p.read_text())
    text = extract_text(raw)
    parsed, parse_status = extract_json(text)
    return {
        "name": name,
        "model": raw.get("model"),
        "stop_reason": raw.get("stop_reason"),
        "usage": raw.get("usage"),
        "elapsed_s": (raw.get("_meta") or {}).get("elapsed_s"),
        "text": text,
        "thinking_chars": len(extract_thinking(raw)),
        "json": parsed,
        "json_parse_status": parse_status,
    }


def render_day1(agents: list[dict]) -> str:
    lines = ["# D2 §Numerics — Day 1 draft (auto-synthesized from MiMo agents A-D)", ""]
    lines.append("## Agent run summary")
    lines.append("")
    lines.append("| Agent | Model | Stop | Elapsed | Tokens out | JSON parsed |")
    lines.append("|---|---|---|---|---|---|")
    for a in agents:
        if a.get("_missing"):
            lines.append(f"| {a.get('_path','?')} | MISSING | — | — | — | — |")
            continue
        usage = a.get("usage") or {}
        lines.append(
            f"| {a['name']} | {a['model']} | {a['stop_reason']} | {a['elapsed_s']:.0f}s "
            f"| {usage.get('output_tokens','?')} | {a['json_parse_status']} |"
        )

    by_name = {a.get("name"): a for a in agents if not a.get("_missing")}

    lines += ["", "## Agent A — sieve cross-check", ""]
    A = by_name.get("agent_A_sieve_xcheck", {})
    if A.get("json"):
        j = A["json"]
        lines.append(f"- Implementation: `{j.get('implementation','?')}`  ({j.get('version','')})")
        lines.append(f"- Verdict: **{j.get('verdict','?')}**")
        if j.get("blocker"):
            lines.append(f"- ⚠ Blocker: {j['blocker']}")
        for c in j.get("cases", []):
            pas = "✓" if c.get("pass") else "✗"
            lines.append(f"  - {pas} q={c.get('q')}, M={c.get('M')}, N={c.get('N')}: measured C={c.get('C_measured')} vs expected {c.get('C_expected')} (|diff|={c.get('abs_diff')})")
    else:
        lines.append(f"- JSON not parsed: {A.get('json_parse_status','?')}")

    lines += ["", "## Agent B — asymptotic correction", ""]
    B = by_name.get("agent_B_asymptotic", {})
    if B.get("json"):
        j = B["json"]
        lines.append(f"- Correction form: `{j.get('correction_form','?')}`")
        lines.append(f"- Explains residual: **{j.get('explains_residual')}**")
        lines.append(f"- (2,T^3) smallness: {j.get('(2,T^3)_smallness_explanation','?')}")
        for case, pred in (j.get("predicted_LSQ_slope_at_finite_N") or {}).items():
            lines.append(f"  - {case}: predicted LSQ at finite N = {pred}")
    else:
        lines.append(f"- JSON not parsed: {B.get('json_parse_status','?')}")

    lines += ["", "## Agent C — m(σ)=0 L-value certificate", ""]
    C = by_name.get("agent_C_lvalue_cert", {})
    if C.get("json"):
        j = C["json"]
        lines.append(f"- Global min |L|: {j.get('global_min_abs_L','?')} ≈ {j.get('global_min_abs_L_decimal_30','?')[:12] if j.get('global_min_abs_L_decimal_30') else '?'}…")
        lines.append(f"- Matches 0.293 claim: **{j.get('matches_claim_0_293')}**")
        lines.append(f"- All cases m=0: **{j.get('all_cases_m_zero')}**")
        if j.get("blocker"):
            lines.append(f"- ⚠ Blocker: {j['blocker']}")
    else:
        lines.append(f"- JSON not parsed: {C.get('json_parse_status','?')}")

    lines += ["", "## Agent D — δ_ff null distribution", ""]
    D = by_name.get("agent_D_deltaff_null", {})
    if D.get("json"):
        j = D["json"]
        lines.append(f"- Null def: {j.get('null_definition','?')[:200]}")
        for c in j.get("cases", []):
            lines.append(
                f"  - **{c.get('label')}**: δ* = {c.get('delta_star_asymptotic')}, "
                f"P(δ_ff=1 | null, N=22) = {c.get('P_delta_ff_eq_1_under_null_N22')} → **{c.get('verdict')}**"
            )
        lines.append(f"- Recommendation: {j.get('recommendation_for_paper','?')}")
    else:
        lines.append(f"- JSON not parsed: {D.get('json_parse_status','?')}")

    lines += ["", "## Ship-gate verdict", "", "(filled in by Claude orchestrator after reviewing agent JSON)"]
    return "\n".join(lines)


def render_day2(agents: list[dict]) -> str:
    lines = ["# D2 paper + D3 companion — Day 2 draft (auto-synthesized from MiMo agents E-H)", ""]
    by_name = {a.get("name"): a for a in agents if not a.get("_missing")}
    for n in DAY2:
        a = by_name.get(n)
        lines += [f"", f"## {n}", ""]
        if not a or not a.get("json"):
            lines.append(f"- JSON not parsed: {(a or {}).get('json_parse_status','MISSING')}")
            continue
        lines.append("```json")
        lines.append(json.dumps(a["json"], indent=2)[:4000])
        lines.append("```")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", type=int, choices=[1, 2], required=True)
    args = ap.parse_args(argv)
    names = DAY1 if args.day == 1 else DAY2
    agents = [load_agent(n) for n in names]
    combined = {"day": args.day, "agents": [{k: v for k, v in a.items() if k != "text"} for a in agents]}
    (RESULTS / f"day{args.day}_combined.json").write_text(json.dumps(combined, indent=2, default=str))
    md = render_day1(agents) if args.day == 1 else render_day2(agents)
    out = RESULTS / (f"d2_numerics_draft.md" if args.day == 1 else "d2_d3_final_draft.md")
    out.write_text(md)
    print(f"wrote {out}")
    print(f"wrote {RESULTS / f'day{args.day}_combined.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
