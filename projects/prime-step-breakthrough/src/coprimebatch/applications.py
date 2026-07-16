"""Compact, claim-scoped application demonstrations for prefix balance.

The presets describe categorical inventories.  They deliberately do not
materialize one :class:`BalanceItem` per occurrence: the million-scale quota
constructor accepts the returned ``counts`` mapping directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

__all__ = [
    "APPLICATION_PRESET_IDS",
    "ApplicationPreset",
    "application_preset",
    "application_preset_payload",
    "application_presets",
]


@dataclass(frozen=True, slots=True)
class ApplicationPreset:
    """Immutable description of one synthetic categorical workload."""

    preset_id: str
    title: str
    domain: str
    status: str
    counts: tuple[tuple[str, int], ...]
    feature_axes: tuple[str, ...]
    item_schema: str
    operational_question: str
    baseline: str
    negative_control: str
    theorem_scope: str
    comparison_set: str
    limitations: tuple[str, ...]
    source_urls: tuple[str, ...]

    @property
    def total_items(self) -> int:
        return sum(count for _category, count in self.counts)

    @property
    def category_count(self) -> int:
        return len(self.counts)

    def counts_dict(self) -> dict[str, int]:
        """Return a fresh mapping suitable for ``quota_order``."""

        return dict(self.counts)

    def to_payload(self) -> dict[str, object]:
        """Return a fresh JSON-ready representation."""

        return {
            "preset_id": self.preset_id,
            "title": self.title,
            "domain": self.domain,
            "status": self.status,
            "counts": self.counts_dict(),
            "total_items": self.total_items,
            "category_count": self.category_count,
            "metadata": {
                "feature_axes": list(self.feature_axes),
                "item_schema": self.item_schema,
                "operational_question": self.operational_question,
                "baseline": self.baseline,
                "negative_control": self.negative_control,
                "theorem_scope": self.theorem_scope,
                "comparison_set": self.comparison_set,
                "limitations": list(self.limitations),
                "source_urls": list(self.source_urls),
            },
        }


def _rendering_preset() -> ApplicationPreset:
    regions = ("tile-row-0", "tile-row-1", "tile-row-2", "tile-row-3")
    strata = ("sample-stratum-0", "sample-stratum-1", "sample-stratum-2", "sample-stratum-3")
    matrix = (
        (208, 224, 240, 256),
        (232, 248, 264, 280),
        (240, 256, 272, 288),
        (248, 264, 280, 296),
    )
    counts = tuple(
        (f"{region}|{stratum}", matrix[row][column])
        for row, region in enumerate(regions)
        for column, stratum in enumerate(strata)
    )
    return ApplicationPreset(
        preset_id="rendering-progressive-joint-cells",
        title="Progressive rendering joint-cell benchmark",
        domain="rendering",
        status="benchmark-ready demonstration",
        counts=counts,
        feature_axes=("screen tile row", "predeclared sample stratum"),
        item_schema=(
            "An already-created render-sample job carrying a screen-tile-row "
            "label and an upstream sampler-stratum label."
        ),
        operational_question=(
            "If work stops at an arbitrary prefix, how far can each declared "
            "joint cell lag or lead its final inventory proportion?"
        ),
        baseline="Stable input order and seeded random shuffle.",
        negative_control=(
            "Assign adversarial radiance or continuous sample coordinates within "
            "each joint cell; categorical balance then leaves image error uncontrolled."
        ),
        theorem_scope="unconstrained categorical strict factor below 3",
        comparison_set="all permutations of the same 4,096 labeled jobs",
        limitations=(
            "Controls only the 16 declared joint-cell counts at every prefix.",
            "Does not control continuous sample geometry, radiance, occlusion, path type, or full star discrepancy.",
            "Does not establish lower image error, faster convergence, final-image improvement, or renderer integration.",
        ),
        source_urls=(
            "https://graphics.pixar.com/library/ProgressiveMultiJitteredSampling/",
            "https://pbr-book.org/4ed/Sampling_and_Reconstruction/Stratified_Sampler",
        ),
    )


def _finance_preset() -> ApplicationPreset:
    return_bins = tuple(f"return-shock-q{index}" for index in range(1, 5))
    volatility_bins = tuple(f"volatility-q{index}" for index in range(1, 5))
    liquidity_bins = tuple(f"liquidity-q{index}" for index in range(1, 5))
    counts = tuple(
        (
            f"{return_bin}|{volatility_bin}|{liquidity_bin}",
            736 + 64 * (return_index + volatility_index + liquidity_index),
        )
        for return_index, return_bin in enumerate(return_bins)
        for volatility_index, volatility_bin in enumerate(volatility_bins)
        for liquidity_index, liquidity_bin in enumerate(liquidity_bins)
    )
    return ApplicationPreset(
        preset_id="finance-scenario-cells",
        title="Financial scenario-cell sequencing demonstration",
        domain="finance",
        status="demonstration only",
        counts=counts,
        feature_axes=("return-shock bin", "volatility bin", "liquidity bin"),
        item_schema=(
            "A synthetic scenario already generated and labeled by an upstream "
            "risk engine; this preset supplies labels and counts, not scenarios."
        ),
        operational_question=(
            "During an interruptible scenario run, how representative is the "
            "processed prefix of the final declared 64-cell inventory?"
        ),
        baseline="Stable generator order and seeded random shuffle.",
        negative_control=(
            "Place all extreme losses inside one cell while preserving cell labels; "
            "the prefix-count certificate then says nothing about loss-estimator error."
        ),
        theorem_scope="unconstrained categorical strict factor below 3",
        comparison_set="all permutations of the same 65,536 synthetic labeled scenarios",
        limitations=(
            "Controls only declared scenario-cell frequencies, not losses or probability weights.",
            "Does not control tail coverage, dependence, Value-at-Risk, expected shortfall, pricing error, or model risk.",
            "Has no bank integration, backtest, regulatory validation, monetary-savings evidence, or production status.",
        ),
        source_urls=(
            "https://business.columbia.edu/faculty/research/monte-carlo-methods-financial-engineering",
            "https://www.bis.org/bcbs/publ/d400.pdf",
        ),
    )


def _laboratory_preset() -> ApplicationPreset:
    matrices = tuple(f"specimen-matrix-{index}" for index in range(1, 5))
    batches = tuple(f"instrument-batch-{index}" for index in range(1, 5))
    windows = ("processing-window-1", "processing-window-2")
    counts = tuple(
        (
            f"{matrix}|{batch}|{window}",
            9 + 2 * (matrix_index + batch_index) + 2 * window_index,
        )
        for matrix_index, matrix in enumerate(matrices)
        for batch_index, batch in enumerate(batches)
        for window_index, window in enumerate(windows)
    )
    return ApplicationPreset(
        preset_id="laboratory-prerandomized-strata",
        title="Pre-randomized laboratory inventory sequencing demonstration",
        domain="laboratory",
        status="demonstration only; never treatment allocation",
        counts=counts,
        feature_axes=("specimen matrix", "instrument batch", "processing window"),
        item_schema=(
            "An existing specimen or assay job whose treatment assignment, if any, "
            "and experimental randomization were fixed before this sequencing step."
        ),
        operational_question=(
            "If assay processing is interrupted, how representative is the processed "
            "prefix of the final declared inventory strata?"
        ),
        baseline="The protocol-approved run order and a seeded within-protocol random shuffle.",
        negative_control=(
            "Impose an unmeasured time drift or adversarial outcomes within every cell; "
            "declared-stratum balance then does not remove bias."
        ),
        theorem_scope="unconstrained categorical strict factor below 3",
        comparison_set="all permutations of the same 512 pre-randomized jobs",
        limitations=(
            "Sequences existing jobs only; it never assigns subjects, specimens, or treatments.",
            "Does not replace randomization, blinding, blocking, a protocol, or a statistical analysis plan.",
            "Does not control unmeasured covariates, time drift, contamination, outcomes, causal validity, or clinical validity.",
            "If a protocol restricts order, use the constrained solver and its a-posteriori certificate instead of this unconstrained preset.",
            "Has no laboratory-system integration, wet-lab validation, regulatory review, or observed error reduction.",
        ),
        source_urls=(
            "https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm",
            "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e9-statistical-principles-clinical-trials",
        ),
    )


_BUILDERS: Final = {
    "rendering-progressive-joint-cells": _rendering_preset,
    "finance-scenario-cells": _finance_preset,
    "laboratory-prerandomized-strata": _laboratory_preset,
}

APPLICATION_PRESET_IDS: Final[tuple[str, ...]] = tuple(_BUILDERS)


def application_preset(preset_id: str) -> ApplicationPreset:
    """Construct one preset by stable identifier."""

    if not isinstance(preset_id, str):
        raise TypeError("preset_id must be a string")
    try:
        preset = _BUILDERS[preset_id]()
    except KeyError as exc:
        choices = ", ".join(APPLICATION_PRESET_IDS)
        raise KeyError(f"unknown application preset {preset_id!r}; choose one of: {choices}") from exc
    _validate_preset(preset)
    return preset


def application_presets() -> tuple[ApplicationPreset, ...]:
    """Construct all presets in stable registry order."""

    return tuple(application_preset(preset_id) for preset_id in APPLICATION_PRESET_IDS)


def application_preset_payload(preset_id: str) -> dict[str, object]:
    """Return one fresh compact payload for CLI, HTTP, or browser use."""

    return application_preset(preset_id).to_payload()


def _validate_preset(preset: ApplicationPreset) -> None:
    if not preset.counts:
        raise AssertionError(f"{preset.preset_id}: empty categorical inventory")
    categories = tuple(category for category, _count in preset.counts)
    if len(set(categories)) != len(categories):
        raise AssertionError(f"{preset.preset_id}: duplicate category")
    if any(not category or isinstance(count, bool) or not isinstance(count, int) or count <= 0 for category, count in preset.counts):
        raise AssertionError(f"{preset.preset_id}: categories must have positive integer counts")
    if "demonstration" not in preset.status:
        raise AssertionError(f"{preset.preset_id}: application status must be explicit")
