(() => {
  "use strict";

  const status = document.querySelector("#status");
  const setStatus = (message, error = false) => {
    status.textContent = message;
    status.classList.toggle("error", error);
  };

  const show = (target, value) => {
    const node = document.querySelector(target);
    node.textContent = typeof value === "string" ? value : JSON.stringify(value, null, 2);
    node.focus();
  };

  const post = async (path, body) => {
    const response = await fetch(path, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(body),
    });
    const data = await response.json().catch(() => ({error: "Server returned invalid JSON"}));
    if (!response.ok) throw new Error(data.error || `Request failed (${response.status})`);
    return data;
  };

  const numbers = (text) => text.split(",").map((item) => Number(item.trim()));
  const rationals = (text) => text.split(",").map((item) => item.trim()).filter(Boolean);
  const run = async (target, label, request) => {
    setStatus(`${label} running…`);
    try {
      show(target, await request());
      setStatus(`${label} complete.`);
    } catch (error) {
      show(target, `Error: ${error.message}`);
      setStatus(`${label} failed.`, true);
    }
  };

  const balanceForm = document.querySelector("#balance-form");
  const balanceResult = document.querySelector("#balance-result");
  const balanceMode = document.querySelector("#balance-mode");
  const balancePreset = document.querySelector("#balance-preset");
  const balanceCounts = document.querySelector("#balance-counts");
  const balanceProblem = document.querySelector("#balance-problem");
  const balanceSolver = document.querySelector("#balance-solver");
  const compactInputs = {
    fixed_blocks: document.querySelector("#balance-fixed-blocks"),
    pinned_prefix: document.querySelector("#balance-pinned-prefix"),
    pinned_suffix: document.querySelector("#balance-pinned-suffix"),
    precedence: document.querySelector("#balance-precedence"),
  };

  const presetNotes = {
    generic: "Generic categorical inventory. Category names must be unique and counts must be nonnegative integers.",
    "rendering-progressive-joint-cells": "Demonstration only: 4,096 items in 16 declared rendering cells. It balances progressive prefixes, not final all-items accuracy.",
    "finance-scenario-cells": "Demonstration only: 65,536 items in 64 synthetic finance-scenario cells. Real use requires data integration, model-risk review, and domain validation.",
    "laboratory-prerandomized-strata": "Demonstration only: 512 items in 32 pre-randomized laboratory strata. Real use requires protocol integration and independent scientific validation.",
  };

  const text = (selector, value) => {
    document.querySelector(selector).textContent = value;
  };

  const fractionText = (value) => {
    if (value === null || value === undefined) return "Not available";
    if (typeof value === "object" && typeof value.fraction === "string") {
      return value.fraction;
    }
    if (typeof value === "boolean") return value ? "Yes" : "No";
    if (typeof value === "object") return JSON.stringify(value);
    return String(value);
  };

  const firstDefined = (...values) => values.find((value) => value !== undefined && value !== null);

  const parseCounts = (source) => {
    const counts = Object.create(null);
    const entries = source.split(/[\n,]+/).map((entry) => entry.trim()).filter(Boolean);
    if (entries.length === 0) throw new Error("Enter at least one category count.");
    entries.forEach((entry) => {
      const separator = entry.indexOf("=");
      if (separator < 1) throw new Error(`Invalid count '${entry}'; use name=count.`);
      const name = entry.slice(0, separator).trim();
      const rawCount = entry.slice(separator + 1).trim();
      if (!name) throw new Error("Category names cannot be empty.");
      if (Object.prototype.hasOwnProperty.call(counts, name)) {
        throw new Error(`Duplicate category '${name}'.`);
      }
      if (!/^(0|[1-9][0-9]*)$/.test(rawCount)) {
        throw new Error(`Count for '${name}' must be a nonnegative integer.`);
      }
      const count = Number(rawCount);
      if (!Number.isSafeInteger(count)) {
        throw new Error(`Count for '${name}' exceeds the browser's safe-integer range.`);
      }
      counts[name] = count;
    });
    return counts;
  };

  const parseJsonArray = (source, label) => {
    const value = JSON.parse(source);
    if (!Array.isArray(value)) throw new Error(`${label} must be a JSON array.`);
    return value;
  };

  const appendLimitation = (list, message) => {
    const item = document.createElement("li");
    item.textContent = message;
    list.append(item);
  };

  const clearChildren = (node) => {
    while (node.firstChild) node.removeChild(node.firstChild);
  };

  const safeList = (value) => {
    if (Array.isArray(value)) return value.map((item) => fractionText(item));
    if (value === undefined || value === null) return [];
    return [fractionText(value)];
  };

  const previewValueText = (value) => {
    if (
      value
      && typeof value === "object"
      && typeof value.category === "string"
      && Number.isInteger(value.occurrence)
    ) {
      return `${value.category} #${value.occurrence}`;
    }
    return fractionText(value);
  };

  const previewList = (value) => {
    if (Array.isArray(value)) return value.map(previewValueText);
    if (value === undefined || value === null) return [];
    return [previewValueText(value)];
  };

  const renderBalance = (data, requestContext) => {
    const result = data && data.result && typeof data.result === "object" ? data.result : data;
    const metrics = result.metrics && typeof result.metrics === "object" ? result.metrics : {};
    const guarantee = result.guarantee && typeof result.guarantee === "object" ? result.guarantee : {};
    const inventory = result.inventory && typeof result.inventory === "object" ? result.inventory : {};
    const application = result.application && typeof result.application === "object"
      ? result.application
      : (data.application && typeof data.application === "object" ? data.application : {});
    const applicationMetadata = application.metadata && typeof application.metadata === "object"
      ? application.metadata
      : {};
    const transport = firstDefined(result.order, data.order_transport, data.transport, result.order_transport, result.transport, {});
    const explanation = result.explanation && typeof result.explanation === "object" ? result.explanation : {};
    const upper = firstDefined(metrics.max_discrepancy, metrics.upper_bound, result.upper_bound, result.max_discrepancy, data.upper_bound);
    const lower = firstDefined(metrics.lower_bound, result.lower_bound, data.lower_bound);
    const additive = firstDefined(metrics.additive_gap, result.additive_gap, data.additive_gap);
    const ratio = firstDefined(metrics.ratio_bound, result.ratio_bound, data.ratio_bound);
    const primaryOptimum = firstDefined(
      guarantee.primary_optimum_proved,
      guarantee.exact_optimum,
      result.primary_optimum_proved,
      result.exact_optimum,
      data.primary_optimum_proved,
      data.exact_optimum,
    );
    const scope = firstDefined(guarantee.scope, result.guarantee_scope, data.guarantee_scope);
    const comparison = firstDefined(guarantee.comparison_set, result.comparison_set, data.comparison_set);
    const feasibility = firstDefined(result.feasibility, data.feasibility);
    const rawPreview = firstDefined(
      transport.preview,
      data.order_preview,
      result.order_preview,
      Array.isArray(result.order) ? result.order.slice(0, 24) : undefined,
      Array.isArray(result.order_codes) ? result.order_codes.slice(0, 24) : undefined,
    );
    const preview = rawPreview && !Array.isArray(rawPreview) && typeof rawPreview === "object"
      ? [
        ...previewList(rawPreview.head),
        ...(previewList(rawPreview.tail).length ? ["…", ...previewList(rawPreview.tail)] : []),
      ]
      : rawPreview;
    const digest = firstDefined(
      transport.sha256,
      transport.digest,
      data.order_sha256,
      data.order_digest,
      result.order_sha256,
      result.order_digest,
    );
    const orderCount = firstDefined(
      transport.count,
      transport.length,
      transport.total_items,
      inventory.total_items,
      data.order_count,
      data.position_count,
      result.order_count,
      Array.isArray(result.order) ? result.order.length : undefined,
      result.counts && Array.isArray(result.counts)
        ? result.counts.reduce((sum, count) => sum + Number(count), 0)
        : undefined,
    );

    text("#balance-result-summary", firstDefined(
      data.summary,
      result.summary,
      result.algorithm ? `Completed with ${result.algorithm}.` : "Prefix-balance certificate received.",
    ));
    text("#balance-feasibility", feasibility === undefined ? "No separate feasibility field returned" : fractionText(feasibility));
    text("#balance-guarantee-scope", fractionText(scope));
    text("#balance-comparison-set", fractionText(comparison));
    text("#balance-primary-optimum", fractionText(primaryOptimum));
    text("#balance-upper-bound", fractionText(upper));
    text("#balance-lower-bound", fractionText(lower));
    text("#balance-additive-gap", fractionText(additive));
    text("#balance-ratio-bound", ratio === undefined || ratio === null ? "Not available (for example, when L = 0)" : fractionText(ratio));
    text("#balance-order-count", fractionText(orderCount));
    text("#balance-order-preview", preview === undefined ? "Not available" : previewList(preview).join(" → "));
    text("#balance-order-digest", fractionText(digest));
    text("#balance-constraints", fractionText(firstDefined(
      result.constraint_pressure,
      data.constraint_pressure,
      explanation.constraint_pressure,
      explanation.constraints,
      application.status,
      applicationMetadata.operational_question,
      result.feasibility,
    )));

    const limitations = document.querySelector("#balance-limitations");
    clearChildren(limitations);
    const suppliedLimitations = [
      ...safeList(data.limitations),
      ...safeList(result.limitations),
      ...safeList(explanation.limitations),
      ...safeList(application.limitations),
      ...safeList(applicationMetadata.limitations),
      ...safeList(data.warnings),
    ];
    suppliedLimitations.forEach((message) => appendLimitation(limitations, message));
    if (requestContext.mode === "problem" && requestContext.solver === "constrained") {
      appendLimitation(limitations, "The constrained constructor reports an a-posteriori interval; it does not inherit the categorical factor below 3.");
    }
    if (requestContext.preset === "rendering-progressive-joint-cells") {
      appendLimitation(limitations, "Rendering use concerns progressive prefixes, not final all-items accuracy.");
    }
    if (requestContext.preset === "finance-scenario-cells") {
      appendLimitation(limitations, "Finance is a demonstration requiring real integration, model-risk review, and validation; no financial outcome is established.");
    }
    if (requestContext.preset === "laboratory-prerandomized-strata") {
      appendLimitation(limitations, "Laboratory batching is a demonstration requiring protocol integration and independent scientific validation; no clinical outcome is established.");
    }
    if (!limitations.firstChild) {
      appendLimitation(limitations, "The certificate applies only to the displayed objective and comparison set.");
    }
    text("#balance-raw", JSON.stringify(data, null, 2));
  };

  const clearBalanceCertificate = (summary) => {
    text("#balance-result-summary", summary);
    [
      "#balance-feasibility",
      "#balance-guarantee-scope",
      "#balance-comparison-set",
      "#balance-primary-optimum",
      "#balance-upper-bound",
      "#balance-lower-bound",
      "#balance-additive-gap",
      "#balance-ratio-bound",
      "#balance-order-count",
      "#balance-order-preview",
      "#balance-order-digest",
      "#balance-constraints",
    ].forEach((selector) => text(selector, "Not available"));
    const limitations = document.querySelector("#balance-limitations");
    clearChildren(limitations);
    appendLimitation(limitations, "No certificate is available for this failed request.");
  };

  const syncBalanceInputs = () => {
    const ordinaryCounts = balanceMode.value === "counts";
    const compactCounts = balanceMode.value === "constrained-counts";
    const countsMode = ordinaryCounts || compactCounts;
    const generic = balancePreset.value === "generic";
    document.querySelector("#balance-preset-field").hidden = !ordinaryCounts;
    document.querySelector("#balance-counts-fields").hidden = !countsMode || (ordinaryCounts && !generic);
    document.querySelector("#balance-compact-fields").hidden = !compactCounts;
    document.querySelector("#balance-problem-fields").hidden = countsMode;
    balancePreset.disabled = !ordinaryCounts;
    balanceCounts.disabled = !countsMode || (ordinaryCounts && !generic);
    balanceCounts.required = compactCounts || (ordinaryCounts && generic);
    Object.values(compactInputs).forEach((input) => {
      input.disabled = !compactCounts;
      input.required = compactCounts;
    });
    balanceProblem.disabled = countsMode;
    balanceProblem.required = !countsMode;
    balanceSolver.disabled = countsMode;
    text(
      "#balance-preset-note",
      compactCounts
        ? "These compact counts are combined with the occurrence constraints below; application presets are disabled in this mode."
        : presetNotes[balancePreset.value],
    );
  };

  balanceMode.addEventListener("change", syncBalanceInputs);
  balancePreset.addEventListener("change", syncBalanceInputs);
  syncBalanceInputs();

  balanceForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const ordinaryCounts = balanceMode.value === "counts";
    const compactCounts = balanceMode.value === "constrained-counts";
    const countsMode = ordinaryCounts || compactCounts;
    const preset = ordinaryCounts ? balancePreset.value : null;
    const requestContext = {
      mode: compactCounts ? "constrained-quota" : (countsMode ? "counts" : "problem"),
      preset,
      solver: compactCounts ? "constrained-quota" : (countsMode ? "quota" : balanceSolver.value),
    };
    let body;
    try {
      if (compactCounts) {
        body = {
          mode: "constrained-quota",
          counts: parseCounts(balanceCounts.value),
          constraints: {
            fixed_blocks: parseJsonArray(compactInputs.fixed_blocks.value, "Fixed blocks"),
            pinned_prefix: parseJsonArray(compactInputs.pinned_prefix.value, "Pinned prefix"),
            pinned_suffix: parseJsonArray(compactInputs.pinned_suffix.value, "Pinned suffix"),
            precedence: parseJsonArray(compactInputs.precedence.value, "Precedence"),
          },
        };
      } else if (ordinaryCounts) {
        body = preset === "generic"
          ? {mode: "quota", counts: parseCounts(balanceCounts.value)}
          : {mode: "quota", preset};
      } else {
        const problem = JSON.parse(balanceProblem.value);
        if (!problem || typeof problem !== "object" || Array.isArray(problem)) {
          throw new Error("Problem JSON must be an object.");
        }
        body = {mode: balanceSolver.value, problem};
      }
    } catch (error) {
      clearBalanceCertificate(`Input error: ${error.message}`);
      text("#balance-raw", "No request sent.");
      setStatus("Prefix Balance input is invalid.", true);
      balanceResult.focus();
      return;
    }

    balanceResult.setAttribute("aria-busy", "true");
    document.querySelector("#balance-submit").disabled = true;
    setStatus("Prefix Balance running…");
    try {
      const data = await post("/api/balance", body);
      renderBalance(data, requestContext);
      setStatus("Prefix Balance complete.");
    } catch (error) {
      clearBalanceCertificate(`Error: ${error.message}`);
      text("#balance-raw", "No successful response.");
      setStatus("Prefix Balance failed.", true);
    } finally {
      balanceResult.setAttribute("aria-busy", "false");
      document.querySelector("#balance-submit").disabled = false;
      balanceResult.focus();
    }
  });

  document.querySelector("#certificate-form").addEventListener("submit", (event) => {
    event.preventDefault();
    run("#certificate-result", "Certificate", () => post("/api/certificate", {
      denominators: numbers(document.querySelector("#denominators").value),
      exact: document.querySelector("#certificate-exact").checked,
    }));
  });

  document.querySelector("#optimizer-form").addEventListener("submit", (event) => {
    event.preventDefault();
    const start = Number(document.querySelector("#candidate-start").value);
    const stop = Number(document.querySelector("#candidate-stop").value);
    run("#optimizer-result", "Benchmark", () => post("/api/optimize", {
      benchmark: true,
      start, stop,
      layers: Number(document.querySelector("#layers").value),
      seed: Number(document.querySelector("#seed").value),
    }));
  });

  document.querySelector("#shift-form").addEventListener("submit", (event) => {
    event.preventDefault();
    run("#shift-result", "Moments", () => post("/api/shift", {
      p: Number(document.querySelector("#prime").value),
      max_order: Number(document.querySelector("#max-order").value),
      exact: true,
    }));
  });

  const syncGapSource = () => {
    const source = document.querySelector('input[name="gap-source"]:checked').value;
    const supplied = source === "supplied";
    const gapValues = document.querySelector("#gap-values");
    const fareyOrder = document.querySelector("#farey-order");
    gapValues.disabled = !supplied;
    gapValues.required = supplied;
    fareyOrder.disabled = supplied;
    fareyOrder.required = !supplied;
  };

  document.querySelectorAll('input[name="gap-source"]').forEach((input) => {
    input.addEventListener("change", syncGapSource);
  });
  syncGapSource();

  document.querySelector("#gaps-form").addEventListener("submit", (event) => {
    event.preventDefault();
    const source = document.querySelector('input[name="gap-source"]:checked').value;
    const body = {exact: document.querySelector("#gaps-exact").checked};
    if (source === "farey") {
      body.farey_order = Number(document.querySelector("#farey-order").value);
    } else {
      body.gaps = rationals(document.querySelector("#gap-values").value);
    }
    run("#gaps-result", "Two-sided gap certificate", () => post("/api/gaps", body));
  });
})();
