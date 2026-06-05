"""
MiMo dispatcher — posts each agent prompt to the MiMo Anthropic-compatible
/v1/messages endpoint and saves the response under results/.

Confirmed Day 0 (2026-05-26):
  endpoint:    https://token-plan-ams.xiaomimimo.com/anthropic/v1/messages
  auth header: x-api-key  (NOT Bearer)
  request:     Anthropic shape — `system` is top-level, `messages` is user/assistant only
  models:      lowercase IDs: mimo-v2.5-pro (hard math), mimo-v2.5 (mechanical)
  thinking:    ON is required for math correctness; OFF gives wrong group structures

Usage:
    export MIMO_API_KEY=tp-...
    python dispatch.py agent_A_sieve_xcheck
    python dispatch.py --day 1
    python dispatch.py --all

Per-agent model + budget overrides in AGENT_CONFIG below.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "prompts"
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

ENDPOINT = "https://token-plan-ams.xiaomimimo.com/anthropic/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"

SYSTEM = (
    "You are a careful research mathematician working on the Aoki-Koyama "
    "Chebyshev-bias function-field program (D2 + D3 directions). Be terse, "
    "exact, and adversarial toward your own conclusions. If a claim is "
    "uncertain, label it CONJECTURAL. When the prompt's output format calls "
    "for JSON, place exactly one valid JSON object in a fenced code block at "
    "the very end of your response; that block is the parsed output. Show "
    "derivations explicitly — do not skip steps on group-structure or "
    "L-function arithmetic."
)

AGENT_CONFIG = {
    "agent_A_sieve_xcheck":   {"model": "mimo-v2.5",     "max_tokens": 24000, "thinking_budget": 14000},
    "agent_B_asymptotic":     {"model": "mimo-v2.5-pro", "max_tokens": 32000, "thinking_budget": 18000},
    "agent_C_lvalue_cert":    {"model": "mimo-v2.5-pro", "max_tokens": 32000, "thinking_budget": 18000},
    "agent_D_deltaff_null":   {"model": "mimo-v2.5",     "max_tokens": 24000, "thinking_budget": 14000},
    "agent_E_s3_sweep":       {"model": "mimo-v2.5",     "max_tokens": 12000, "thinking_budget":  6000},
    "agent_F_mrho_artin":     {"model": "mimo-v2.5-pro", "max_tokens": 24000, "thinking_budget": 14000},
    "agent_G_lean_stub":      {"model": "mimo-v2.5-pro", "max_tokens": 24000, "thinking_budget": 14000},
    "agent_H_adversarial":    {"model": "mimo-v2.5-pro", "max_tokens": 20000, "thinking_budget": 10000},
}

DAY1 = ["agent_A_sieve_xcheck", "agent_B_asymptotic", "agent_C_lvalue_cert", "agent_D_deltaff_null"]
DAY2 = ["agent_E_s3_sweep", "agent_F_mrho_artin", "agent_G_lean_stub", "agent_H_adversarial"]


def load_prompt(name: str) -> str:
    p = PROMPTS / f"{name}.md"
    text = p.read_text()
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end > 0:
            text = text[end + 4:].lstrip()
    return text


def call_mimo(prompt: str, model: str, max_tokens: int, *, thinking_budget: int | None = None, timeout: int = 1800) -> dict:
    """Streaming call — SSE keeps connection alive past server's idle timeout.

    Reassembles the message_start/content_block_*/message_delta events into the
    same final shape the non-streaming endpoint would return.

    thinking_budget caps the extended-thinking block so the model is forced to
    leave room for text output. When set, temperature MUST be 1.0 per Anthropic
    API requirement for thinking-enabled calls.
    """
    key = os.environ.get("MIMO_API_KEY")
    if not key:
        raise RuntimeError("MIMO_API_KEY not set")
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "system": SYSTEM,
        "stream": True,
        "messages": [{"role": "user", "content": prompt}],
    }
    if thinking_budget:
        payload["thinking"] = {"type": "enabled", "budget_tokens": int(thinking_budget)}
        payload["temperature"] = 1.0
    else:
        payload["temperature"] = 0.2
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
            "x-api-key": key,
            "anthropic-version": ANTHROPIC_VERSION,
        },
    )
    t0 = time.time()
    content_blocks: list[dict] = []  # index -> partial block
    final: dict = {"content": [], "_stream_events": 0}
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        for raw_line in resp:
            line = raw_line.decode("utf-8", errors="replace").rstrip("\n")
            if not line.startswith("data:"):
                continue
            payload = line[5:].strip()
            if not payload:
                continue
            try:
                ev = json.loads(payload)
            except json.JSONDecodeError:
                continue
            final["_stream_events"] += 1
            etype = ev.get("type")
            if etype == "message_start":
                msg = ev.get("message", {})
                for k in ("id", "model", "role", "usage"):
                    if k in msg:
                        final[k] = msg[k]
            elif etype == "content_block_start":
                idx = ev["index"]
                while len(content_blocks) <= idx:
                    content_blocks.append({})
                block = ev.get("content_block", {})
                content_blocks[idx] = {"type": block.get("type")}
                if block.get("type") == "text":
                    content_blocks[idx]["text"] = block.get("text", "")
                elif block.get("type") == "thinking":
                    content_blocks[idx]["thinking"] = block.get("thinking", "")
            elif etype == "content_block_delta":
                idx = ev["index"]
                delta = ev.get("delta", {})
                dtype = delta.get("type")
                if dtype == "text_delta":
                    content_blocks[idx]["text"] = content_blocks[idx].get("text", "") + delta.get("text", "")
                elif dtype == "thinking_delta":
                    content_blocks[idx]["thinking"] = content_blocks[idx].get("thinking", "") + delta.get("thinking", "")
                elif dtype == "signature_delta":
                    content_blocks[idx]["signature"] = content_blocks[idx].get("signature", "") + delta.get("signature", "")
            elif etype == "content_block_stop":
                pass
            elif etype == "message_delta":
                d = ev.get("delta", {})
                if "stop_reason" in d:
                    final["stop_reason"] = d["stop_reason"]
                if "usage" in ev:
                    final.setdefault("usage", {}).update(ev["usage"])
            elif etype == "message_stop":
                pass
            elif etype == "error":
                final["error"] = ev.get("error")
                break
    final["content"] = content_blocks
    final["_meta"] = {"elapsed_s": time.time() - t0, "model": model, "max_tokens": max_tokens, "streamed": True}
    return final


def run_one(name: str) -> tuple[str, str]:
    cfg = AGENT_CONFIG[name]
    t0 = time.time()
    try:
        prompt = load_prompt(name)
        out = call_mimo(
            prompt, cfg["model"], cfg["max_tokens"],
            thinking_budget=cfg.get("thinking_budget"),
        )
        (RESULTS / f"{name}.json").write_text(json.dumps(out, indent=2))
        usage = out.get("usage", {})
        stop = out.get("stop_reason", "?")
        return name, f"ok in {time.time()-t0:.1f}s — stop={stop} usage={usage}"
    except Exception as e:
        (RESULTS / f"{name}.error.txt").write_text(repr(e))
        return name, f"err in {time.time()-t0:.1f}s: {e!r}"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("agent", nargs="?")
    ap.add_argument("--day", type=int, choices=[1, 2])
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args(argv)

    if args.agent:
        names = [args.agent]
    elif args.day == 1:
        names = DAY1
    elif args.day == 2:
        names = DAY2
    elif args.all:
        names = DAY1 + DAY2
    else:
        ap.error("specify agent, --day, or --all")
        return 2

    max_workers = int(os.environ.get("MIMO_CONCURRENCY", "4"))
    print(f"Dispatching {len(names)} agents (concurrency={max_workers})", flush=True)
    with cf.ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(run_one, n): n for n in names}
        for fut in cf.as_completed(futures):
            name, status = fut.result()
            print(f"  [{name}] {status}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
