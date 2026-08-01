(() => {
  "use strict";

  const FORBIDDEN_KEY = /^(answer|correct|gold|ground_truth|label|loss|outcome|target|truth)$/i;
  const COST_KEYS = new Set([
    "reviewer_rate_per_hour",
    "operator_rate_per_hour",
    "compute_usd",
    "rework_usd",
    "integration_usd",
    "license_usd",
  ]);
  const status = document.querySelector("#pilot-status");
  const manifestInput = document.querySelector("#pilot-manifest");
  const manifestSummary = document.querySelector("#pilot-manifest-summary");
  const sessionInput = document.querySelector("#pilot-session-id");
  const rateInput = document.querySelector("#pilot-reviewer-rate");
  const beginButton = document.querySelector("#pilot-begin");
  const review = document.querySelector("#pilot-review");
  const complete = document.querySelector("#pilot-complete");
  const conditionBadge = document.querySelector("#pilot-condition");
  const progress = document.querySelector("#pilot-progress");
  const prompt = document.querySelector("#pilot-prompt");
  const choices = document.querySelector("#pilot-choices");
  const skipButton = document.querySelector("#pilot-skip");
  const pauseButton = document.querySelector("#pilot-pause");
  const completeSummary = document.querySelector("#pilot-complete-summary");
  const downloadButton = document.querySelector("#pilot-download");
  const evidence = document.querySelector("#pilot-evidence");

  let loaded = null;
  let state = null;

  const setStatus = (message, error = false) => {
    status.textContent = message;
    status.classList.toggle("error", error);
  };

  const isRecord = (value) => value !== null && typeof value === "object" && !Array.isArray(value);

  const rejectForbiddenKeys = (value, path = "manifest") => {
    if (Array.isArray(value)) {
      value.forEach((item, index) => rejectForbiddenKeys(item, `${path}[${index}]`));
      return;
    }
    if (!isRecord(value)) return;
    Object.entries(value).forEach(([key, child]) => {
      if (FORBIDDEN_KEY.test(key)) {
        throw new Error(`${path}.${key} is not allowed in a label-blind manifest`);
      }
      rejectForbiddenKeys(child, `${path}.${key}`);
    });
  };

  const asciiToken = (value, name) => {
    if (typeof value !== "string" || !/^[A-Za-z0-9._:-]+$/.test(value)) {
      throw new Error(`${name} must be a nonblank ASCII token`);
    }
    return value;
  };

  const digestToken = (value, name) => {
    const token = asciiToken(value, name);
    if (!/^[0-9a-f]{64}$/i.test(token)) throw new Error(`${name} must be a SHA-256 hex digest`);
    return token.toLowerCase();
  };

  const validateManifest = (value) => {
    rejectForbiddenKeys(value);
    if (!isRecord(value)) throw new Error("manifest must be a JSON object");
    const condition = asciiToken(value.condition, "condition");
    const orderDigest = digestToken(value.order_digest, "order_digest");
    const cohortDigest = digestToken(value.cohort_digest, "cohort_digest");
    if (!Array.isArray(value.items) || value.items.length === 0 || value.items.length > 10000) {
      throw new Error("items must contain between 1 and 10,000 entries");
    }
    const items = value.items.map((item, index) => {
      if (!isRecord(item)) throw new Error(`items[${index}] must be an object`);
      const itemId = asciiToken(item.item_id, `items[${index}].item_id`);
      if (typeof item.prompt !== "string" || !item.prompt.trim()) {
        throw new Error(`items[${index}].prompt must be a nonblank string`);
      }
      if (!Array.isArray(item.choices) || item.choices.length < 2 || item.choices.length > 16) {
        throw new Error(`items[${index}].choices must contain 2 to 16 choices`);
      }
      const itemChoices = item.choices.map((choice, choiceIndex) => {
        if (!isRecord(choice)) throw new Error(`items[${index}].choices[${choiceIndex}] must be an object`);
        const choiceId = asciiToken(choice.choice_id, `items[${index}].choices[${choiceIndex}].choice_id`);
        if (typeof choice.text !== "string" || !choice.text.trim()) {
          throw new Error(`items[${index}].choices[${choiceIndex}].text must be a nonblank string`);
        }
        return {choice_id: choiceId, text: choice.text};
      });
      if (new Set(itemChoices.map((choice) => choice.choice_id)).size !== itemChoices.length) {
        throw new Error(`items[${index}] has duplicate choice IDs`);
      }
      return {item_id: itemId, prompt: item.prompt, choices: itemChoices};
    });
    const itemIds = items.map((item) => item.item_id);
    if (new Set(itemIds).size !== itemIds.length) throw new Error("item IDs must be unique");
    if (value.item_ids !== undefined && JSON.stringify(value.item_ids) !== JSON.stringify(itemIds)) {
      throw new Error("item_ids must match items in the frozen order");
    }
    return {condition, order_digest: orderDigest, cohort_digest: cohortDigest, items};
  };

  // This is the Python module's canonical JSON shape for the ASCII/hash-only
  // evidence fields. Cost fields are floats in Python even when their value is
  // integral, so retain the .0 spelling for those keys.
  const canonical = (value, key = "") => {
    if (value === null) return "null";
    if (Array.isArray(value)) return `[${value.map((item) => canonical(item)).join(",")}]`;
    if (typeof value === "object") {
      return `{${Object.keys(value).sort().map((name) => `${JSON.stringify(name)}:${canonical(value[name], name)}`).join(",")}}`;
    }
    if (typeof value === "number") {
      if (!Number.isFinite(value)) throw new Error("non-finite numbers are not allowed");
      if (COST_KEYS.has(key) && Number.isInteger(value)) return `${value}.0`;
      return Number.isInteger(value) ? String(value) : JSON.stringify(value);
    }
    return JSON.stringify(value);
  };

  const sha256 = async (text) => {
    if (!window.crypto || !window.crypto.subtle) {
      throw new Error("Web Crypto is unavailable; use the loopback pilot URL");
    }
    const bytes = new TextEncoder().encode(text);
    const digest = await window.crypto.subtle.digest("SHA-256", bytes);
    return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
  };

  const nowNs = () => {
    const candidate = Math.max(1, Math.round(window.performance.now() * 1_000_000));
    if (!state) return candidate;
    state.lastMonotonicNs = Math.max(candidate, state.lastMonotonicNs + 1);
    return state.lastMonotonicNs;
  };

  const utcNow = () => new Date().toISOString();

  const record = async (eventType, itemId = null, payload = {}) => {
    const monotonicNs = nowNs();
    const body = {
      sequence: state.events.length,
      event_type: eventType,
      monotonic_ns: monotonicNs,
      utc: utcNow(),
      item_id: itemId,
      payload,
      previous_hash: state.previousHash,
    };
    const eventHash = await sha256(canonical(body));
    const event = {...body, event_hash: eventHash};
    state.events.push(event);
    state.previousHash = eventHash;
    return event;
  };

  const clearChoices = () => {
    while (choices.firstChild) choices.removeChild(choices.firstChild);
  };

  const showCurrent = async () => {
    const item = state.items[state.position];
    if (!item) {
      await record("session_end");
      state.ended = true;
      skipButton.disabled = true;
      pauseButton.disabled = true;
      complete.hidden = false;
      review.hidden = true;
      completeSummary.textContent = `Recorded ${state.events.length} events for ${state.items.length} items. Ground truth was not loaded.`;
      setStatus("Session sealed. Download the JSONL evidence.");
      return;
    }
    state.currentItem = item;
    progress.textContent = `Item ${state.position + 1} of ${state.items.length}`;
    prompt.textContent = item.prompt;
    clearChoices();
    item.choices.forEach((choice, choiceIndex) => {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = choice.text;
      button.addEventListener("click", () => respond(choice, choiceIndex));
      choices.append(button);
    });
    await record("item_shown", item.item_id, {position: state.position + 1});
  };

  const advance = async () => {
    state.position += 1;
    await showCurrent();
  };

  const respond = async (choice, choiceIndex) => {
    if (!state || state.ended || state.paused || state.busy || !state.currentItem) return;
    state.busy = true;
    try {
      await record("response", state.currentItem.item_id, {
        selection: choice.choice_id,
        selection_index: choiceIndex,
      });
      state.currentItem = null;
      await advance();
    } finally {
      state.busy = false;
    }
  };

  const skip = async () => {
    if (!state || state.ended || state.paused || state.busy || !state.currentItem) return;
    state.busy = true;
    try {
      await record("skip", state.currentItem.item_id, {reason: "participant_skip"});
      state.currentItem = null;
      await advance();
    } finally {
      state.busy = false;
    }
  };

  const togglePause = async () => {
    if (!state || state.ended || state.busy) return;
    state.busy = true;
    try {
      if (state.paused) {
        await record("resume", state.currentItem ? state.currentItem.item_id : null);
        state.paused = false;
        pauseButton.textContent = "Pause";
        setStatus("Session resumed.");
        return;
      }
      await record("pause", state.currentItem ? state.currentItem.item_id : null);
      state.paused = true;
      pauseButton.textContent = "Resume";
      setStatus("Session paused; the interval is excluded from active time.");
    } finally {
      state.busy = false;
    }
  };

  const manifestRecord = (manifest, manifestSha256) => ({
    record_type: "manifest",
    manifest,
    manifest_sha256: manifestSha256,
  });

  const download = async () => {
    if (!state || !state.ended) return;
    const records = [manifestRecord(state.manifest, state.manifestSha256), ...state.events.map((event) => ({record_type: "event", event}))];
    const content = `${records.map((entry) => canonical(entry)).join("\n")}\n`;
    evidence.value = content;
    evidence.hidden = false;
    const blob = new Blob([content], {type: "application/x-ndjson"});
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `${state.manifest.session_id}.jsonl`;
    document.body.append(anchor);
    anchor.click();
    anchor.remove();
    window.setTimeout(() => URL.revokeObjectURL(url), 0);
    setStatus("JSONL download started. Verify it before analysis.");
  };

  const begin = async () => {
    try {
      const sessionId = asciiToken(sessionInput.value.trim(), "session ID");
      const reviewerRate = Number(rateInput.value);
      if (!Number.isFinite(reviewerRate) || reviewerRate < 0) throw new Error("reviewer rate must be finite and nonnegative");
      const itemIds = loaded.items.map((item) => item.item_id);
      const manifest = {
        schema_version: "workflow-measurement-v1",
        session_id: sessionId,
        condition: loaded.condition,
        order_digest: loaded.order_digest,
        cohort_digest: loaded.cohort_digest,
        item_ids: itemIds,
        item_count: itemIds.length,
        cost_inputs: {
          reviewer_rate_per_hour: reviewerRate,
          operator_rate_per_hour: 0,
          compute_usd: 0,
          rework_usd: 0,
          integration_usd: 0,
          license_usd: 0,
        },
        created_utc: utcNow(),
      };
      const manifestSha256 = await sha256(canonical(manifest));
      state = {
        manifest,
        manifestSha256,
        items: loaded.items,
        events: [],
        previousHash: manifestSha256,
        lastMonotonicNs: 0,
        position: 0,
        currentItem: null,
        paused: false,
        busy: false,
        ended: false,
      };
      await record("session_start");
      document.querySelector("#pilot-setup").hidden = true;
      review.hidden = false;
      conditionBadge.textContent = `Condition: ${manifest.condition}`;
      await showCurrent();
      setStatus("Session running. Respond to each item or skip it.");
    } catch (error) {
      setStatus(`Cannot begin: ${error.message}`, true);
    }
  };

  manifestInput.addEventListener("change", async () => {
    loaded = null;
    beginButton.disabled = true;
    try {
      const file = manifestInput.files && manifestInput.files[0];
      if (!file) throw new Error("select a manifest JSON file");
      loaded = validateManifest(JSON.parse(await file.text()));
      manifestSummary.textContent = `${loaded.condition}: ${loaded.items.length} label-blind items; order and cohort digests accepted.`;
      beginButton.disabled = false;
      setStatus("Manifest accepted. Confirm the pseudonymous session ID and rate.");
    } catch (error) {
      manifestSummary.textContent = "No manifest loaded.";
      setStatus(`Manifest rejected: ${error.message}`, true);
    }
  });

  beginButton.addEventListener("click", begin);
  skipButton.addEventListener("click", () => { skip().catch((error) => setStatus(`Skip failed: ${error.message}`, true)); });
  pauseButton.addEventListener("click", () => { togglePause().catch((error) => setStatus(`Pause/resume failed: ${error.message}`, true)); });
  downloadButton.addEventListener("click", () => { download().catch((error) => setStatus(`Download failed: ${error.message}`, true)); });

  window.addEventListener("beforeunload", (event) => {
    if (state && !state.ended) {
      event.preventDefault();
      event.returnValue = "The measured session is not sealed.";
    }
  });
})();
