"""
Mini-project dispatcher. Lesson from prior sprint: MiMo emits substantive
extended thinking but rarely text. We TREAT THE THINKING CONTENT AS THE
DELIVERABLE. Saves response to <out_dir>/<name>.json plus a sibling
<name>.thinking.txt for direct human review.

Usage:
    export MIMO_API_KEY=...
    python dispatch.py <prompts_dir> <out_dir>          # all .md in prompts_dir
    python dispatch.py <prompts_dir> <out_dir> name1 name2  # specific names

Concurrency from MIMO_CONCURRENCY env (default 4).
Per-prompt config from a JSON header in the .md file (front-matter), e.g.:
    ---
    model: mimo-v2.5-pro
    max_tokens: 16000
    ---
"""

from __future__ import annotations

import concurrent.futures as cf
import json
import os
import sys
import time
import urllib.request
import re
from pathlib import Path

ENDPOINT = "https://token-plan-ams.xiaomimimo.com/anthropic/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
DEFAULT_MODEL = "mimo-v2.5"
DEFAULT_MAX_TOKENS = 12000

SYSTEM = (
    "You are a research-mathematician. Open-ended exploration is welcome. "
    "Look for non-obvious connections, counter-intuitive bridges, and missed "
    "opportunities in active areas of mathematics and computer science. "
    "When you're uncertain, say so. Prefer concrete testable predictions over "
    "vague analogies. Reasoning out loud is valued; final summary at end is "
    "valued more."
)


def parse_prompt(text: str) -> tuple[dict, str]:
    cfg = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end > 0:
            for line in text[3:end].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    k, v = k.strip(), v.strip()
                    try:
                        v = int(v)
                    except ValueError:
                        pass
                    cfg[k] = v
            text = text[end + 4:].lstrip()
    return cfg, text


def call_mimo(prompt: str, *, model: str, max_tokens: int, timeout: int = 1800) -> dict:
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
    body = json.dumps(payload).encode()
    req = urllib.request.Request(ENDPOINT, data=body, headers={
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
        "x-api-key": key,
        "anthropic-version": ANTHROPIC_VERSION,
    })
    t0 = time.time()
    content_blocks: list[dict] = []
    final: dict = {"content": [], "_stream_events": 0}
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        for raw in resp:
            line = raw.decode("utf-8", "replace").rstrip("\n")
            if not line.startswith("data:"): continue
            payload_s = line[5:].strip()
            if not payload_s: continue
            try:
                ev = json.loads(payload_s)
            except json.JSONDecodeError:
                continue
            final["_stream_events"] += 1
            t = ev.get("type")
            if t == "message_start":
                msg = ev.get("message", {})
                for k in ("id", "model", "role", "usage"):
                    if k in msg: final[k] = msg[k]
            elif t == "content_block_start":
                idx = ev["index"]
                while len(content_blocks) <= idx:
                    content_blocks.append({})
                block = ev.get("content_block", {})
                content_blocks[idx] = {"type": block.get("type")}
                if block.get("type") == "text":
                    content_blocks[idx]["text"] = block.get("text", "")
                elif block.get("type") == "thinking":
                    content_blocks[idx]["thinking"] = block.get("thinking", "")
            elif t == "content_block_delta":
                idx = ev["index"]
                d = ev.get("delta", {})
                dtype = d.get("type")
                if dtype == "text_delta":
                    content_blocks[idx]["text"] = content_blocks[idx].get("text", "") + d.get("text", "")
                elif dtype == "thinking_delta":
                    content_blocks[idx]["thinking"] = content_blocks[idx].get("thinking", "") + d.get("thinking", "")
            elif t == "message_delta":
                d = ev.get("delta", {})
                if "stop_reason" in d: final["stop_reason"] = d["stop_reason"]
                if "usage" in ev: final.setdefault("usage", {}).update(ev["usage"])
            elif t == "error":
                final["error"] = ev.get("error")
                break
    final["content"] = content_blocks
    final["_meta"] = {"elapsed_s": time.time() - t0, "model": model, "max_tokens": max_tokens}
    return final


def run_one(prompts_dir: Path, out_dir: Path, name: str) -> tuple[str, str]:
    t0 = time.time()
    try:
        text = (prompts_dir / f"{name}.md").read_text()
        cfg, prompt = parse_prompt(text)
        model = cfg.get("model", DEFAULT_MODEL)
        max_tokens = cfg.get("max_tokens", DEFAULT_MAX_TOKENS)
        out = call_mimo(prompt, model=model, max_tokens=max_tokens)
        (out_dir / f"{name}.json").write_text(json.dumps(out, indent=2))
        # Extract thinking + text for easy reading
        thinking = ""
        textout = ""
        for b in out.get("content", []):
            if b.get("type") == "thinking":
                thinking += b.get("thinking", "")
            elif b.get("type") == "text":
                textout += b.get("text", "")
        (out_dir / f"{name}.thinking.txt").write_text(thinking)
        (out_dir / f"{name}.text.txt").write_text(textout)
        usage = out.get("usage", {})
        return name, f"ok {time.time()-t0:.0f}s thinking={len(thinking)} text={len(textout)} usage={usage}"
    except Exception as e:
        (out_dir / f"{name}.error.txt").write_text(repr(e))
        return name, f"err {time.time()-t0:.0f}s: {e!r}"


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    prompts_dir = Path(argv[0])
    out_dir = Path(argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)
    explicit = argv[2:] if len(argv) > 2 else None
    names = explicit or sorted([p.stem for p in prompts_dir.glob("*.md")])
    max_workers = int(os.environ.get("MIMO_CONCURRENCY", "4"))
    print(f"Dispatching {len(names)} agents @ concurrency={max_workers} from {prompts_dir}", flush=True)
    with cf.ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(run_one, prompts_dir, out_dir, n): n for n in names}
        for fut in cf.as_completed(futures):
            name, status = fut.result()
            print(f"  [{name}] {status}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
