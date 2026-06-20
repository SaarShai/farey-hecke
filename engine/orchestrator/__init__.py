"""Aletheia engine — orchestrator package.

Exposes the pipeline driver `run` and the provenance helpers
(`synthesize`, `make_run_id`, `RunRecord`). See engine/GOAL.md for the
shared interface contract and engine/README.md for the architecture.
"""

from .orchestrator import run, synthesize, make_run_id, RunRecord

__all__ = ["run", "synthesize", "make_run_id", "RunRecord"]
