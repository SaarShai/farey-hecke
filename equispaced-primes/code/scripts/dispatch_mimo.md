# `dispatch_mimo.sh` — Xiaomi MiMo dispatch wrapper

Bulk-execution lane for cheap generative tasks (Δ-machine draft refinement,
Paper B sections, citation cleanups, etc.). Wraps the Xiaomi MiMo Open
Platform's OpenAI-compatible chat-completions endpoint.

Discovered 2026-05-09. Round-trip verified.

---

## Discovered API contract

| Field                       | Value                                                          |
|-----------------------------|----------------------------------------------------------------|
| Provider                    | Xiaomi MiMo Open Platform (`platform.xiaomimimo.com`)          |
| OpenAI-compatible base URL  | `https://api.xiaomimimo.com/v1`                                |
| Anthropic-compatible base   | `https://api.xiaomimimo.com/anthropic` (not used by wrapper)   |
| Models endpoint             | `GET /v1/models`                                               |
| Chat completions endpoint   | `POST /v1/chat/completions` (OpenAI shape)                     |
| Auth header                 | `Authorization: Bearer $MIMO_API_KEY`                          |
| Key file                    | `~/.farey_api_keys` — defines `MIMO_API_KEY`                   |
| Key prefix (this account)   | `sk-e2w...xkc5` (masked; first 6 + last 4 only)                |

The "OpenAI-compatible key with `thinking:{type:disabled}` requirement"
combination matches what the delta-machine roadmap calls out: the platform
exposes both an OpenAI-style and an Anthropic-style surface and accepts the
Claude-style `thinking` field on the OpenAI-style endpoint.

### Models listed by `/v1/models` (probe at 2026-05-09)

| ID                              | Notes                                              |
|---------------------------------|----------------------------------------------------|
| `mimo-v2-flash`                 | **Wrapper default.** Cheapest, fastest (~1.5s)     |
| `mimo-v2-omni`                  | Multimodal variant                                 |
| `mimo-v2-pro`                   | V2 flagship                                        |
| `mimo-v2.5`                     | V2.5 reasoning model — emits `reasoning_content` unless `thinking:{type:disabled}` |
| `mimo-v2.5-pro`                 | V2.5 flagship (1M context, 128K max output)        |
| `mimo-v2-tts`, `mimo-v2.5-tts`, `mimo-v2.5-tts-voiceclone`, `mimo-v2.5-tts-voicedesign` | TTS, not used by this wrapper |

All five chat-capable models replied 200/`OK` to a short health-check probe.

### Pricing (overseas USD/1M tokens — per third-party docs, verify before billing)

| Model            | Input (cache-miss / cached) | Output | Context | Max output |
|------------------|------------------------------|--------|---------|------------|
| `mimo-v2.5-flash` (not in this account's `/models`) | $0.10 / $0.01 | $0.30 | 256K | 64K |
| `mimo-v2.5`        | $0.40 / $0.08              | $2.00  | 1M      | 128K       |
| `mimo-v2.5-pro`    | $1.00 / $0.20              | $3.00  | 1M      | 128K       |

Pricing source: <https://devtk.ai/en/blog/xiaomi-mimo-v2-5-agent-model-guide-2026/>.
v2 generation pricing not separately documented; treat as an upper bound of the
v2.5 generation. **Always confirm in the billing console before high-volume runs.**

---

## Why `"thinking":{"type":"disabled"}` is mandatory

Empirically (probed 2026-05-09):

- `mimo-v2-flash` works either way (no reasoning tokens emitted).
- `mimo-v2.5` *without* the field returns 200 but injects a `reasoning_content`
  string into the response (43 completion tokens for a one-word answer).
- `mimo-v2.5` *with* `"thinking":{"type":"disabled"}` returns clean content
  in 2 completion tokens, ~1.6s.
- The delta-machine roadmap notes that on some models the visible `content`
  is **empty** when the thinking field is omitted.

The wrapper therefore unconditionally sets `"thinking":{"type":"disabled"}`
on every request.

---

## Usage

```bash
# Stdin
echo "Summarize the abstract of arXiv:2401.00001 in 80 words." \
  | scripts/dispatch_mimo.sh -

# File
scripts/dispatch_mimo.sh prompts/section_4_intro.txt > drafts/section_4.md

# Choose a heavier model and a system prompt
scripts/dispatch_mimo.sh \
  --model mimo-v2.5-pro \
  --max-tokens 16000 \
  --system-file prompts/style_guide.txt \
  prompts/paper_B_section_3.txt \
  > drafts/paper_B_section_3.md

# Inspect raw API response (debugging only)
echo "ping" | scripts/dispatch_mimo.sh --raw - | jq .usage
```

### Flags

| Flag             | Default                       | Notes                                              |
|------------------|-------------------------------|----------------------------------------------------|
| `--model`        | `mimo-v2-flash`               | Any chat model from `/v1/models`                   |
| `--max-tokens`   | `8000`                        | Output cap; per-model max in pricing table above   |
| `--temperature`  | `0.7`                         | Standard sampling                                  |
| `--system-file`  | (none)                        | If set, prepended as a `system` message            |
| `--raw`          | off                           | Emit raw JSON instead of just text                 |
| `-h`, `--help`   | —                             | Print usage                                        |
| Positional arg   | — (required)                  | Prompt file path, or `-` for stdin                 |

### Exit codes

| Code | Meaning                                                       |
|------|---------------------------------------------------------------|
| 0    | Success (response text on stdout, trailing newline)           |
| 1    | Usage / config error (missing key, missing arg, unreadable file) |
| 2    | API call failed (non-200) **or** empty content. Body on stderr. |

---

## Round-trip test (receipt)

Date: 2026-05-09. All tests below ran from
`/Users/za/Documents/Farey NOW/primes-equispaced/`.

| # | Command                                                                                          | Exit | Latency | Result                                              |
|---|--------------------------------------------------------------------------------------------------|------|---------|-----------------------------------------------------|
| 1 | `printf 'Reply only the word READY.' \| ./scripts/dispatch_mimo.sh -`                            | 0    | 2s      | stdout: `READY`                                     |
| 2 | `./scripts/dispatch_mimo.sh --model mimo-v2-flash --max-tokens 20 <file>` (file says `READY-V2`) | 0    | 1s      | stdout: `READY-V2`                                  |
| 3 | `printf 'Reply OK.' \| ./scripts/dispatch_mimo.sh --max-tokens 20 --raw -`                       | 0    | 2s      | valid JSON; `usage.completion_tokens=10`            |
| 4 | `./scripts/dispatch_mimo.sh --model not-a-real-model -` (negative case)                          | 2    | 1s      | stderr shows HTTP 400 + body; key masked as `sk-e2w...xkc5` |
| 5 | `--system-file <pig-latin> <file>` (system-prompt path)                                          | 0    | ~2s     | system prompt applied (Pig-Latin reply observed)    |
| 6 | `grep -F "$MIMO_API_KEY"` over every stderr/stdout produced above                                | —    | —       | **No occurrences. Key absent from all outputs.**    |

Conclusion: wrapper is round-trip clean and safe to dispatch ~50 generative
tasks across the next two weeks at the default `mimo-v2-flash` model.

---

## Known limitations

1. **`mimo-v2-flash` may emit stray `</think>` tags** in some responses
   (observed in test 5 with a system prompt). The wrapper passes content
   through verbatim — strip these in downstream processing if needed,
   e.g. `sed 's|</\?think>||g'`.
2. **Streaming is not supported** by this wrapper. The endpoint accepts
   `"stream": true` but we always read the full response. Add a `--stream`
   flag if needed for long generations.
3. **No automatic retry/backoff.** If 5xx becomes common on a given model,
   wrap calls in your dispatch loop with `until` + sleep, or extend the
   wrapper.
4. **`max_tokens` per-model caps** are not enforced client-side. The default
   `8000` is well within all five chat models. If you raise it past 64K on
   `mimo-v2-flash` family the API will reject.
5. **Pricing is third-party-sourced.** Confirm in the Xiaomi MiMo billing
   console before heavy runs.
6. **The Anthropic-style endpoint at `/anthropic` is not used.** If you ever
   need real Claude-style features (e.g. extended thinking with budget),
   point a separate wrapper at `https://api.xiaomimimo.com/anthropic`.

---

## Security notes

- The script sources `~/.farey_api_keys` and never echoes `$MIMO_API_KEY`.
- All error paths print a masked form (`first 6 + last 4`) only.
- Response bodies dumped to stderr are first piped through
  `sed "s|$MIMO_API_KEY|<MIMO_API_KEY:masked>|g"` so even if the API echoes
  the key back (it shouldn't), it never lands in logs.
- The script writes the request payload to a temp file via `mktemp`, and
  unconditionally `rm -f`s it on `EXIT` via `trap`. The key is in the
  `Authorization` header passed to `curl` directly, never written to disk.
