"""Capture the exact 400 error body from telemetry.googleapis.com."""
import os
import sys

os.environ["GOOGLE_CLOUD_PROJECT"] = "gen-lang-client-0546914885"

# Patch BEFORE importing ADK telemetry
from opentelemetry.exporter.otlp.proto.http import trace_exporter as te

_orig_export = te.OTLPSpanExporter._export


def _patched_export(self, serialized_data, timeout_sec=None):
    resp = _orig_export(self, serialized_data, timeout_sec)
    print(f"\n=== OTLP RESPONSE ===", flush=True)
    print(f"Status: {resp.status_code}", flush=True)
    print(f"Body: {resp.text[:3000]}", flush=True)
    print(f"Endpoint: {self._endpoint}", flush=True)
    print("=====================\n", flush=True)
    return resp


te.OTLPSpanExporter._export = _patched_export

import importlib.util, pathlib

spec = importlib.util.spec_from_file_location(
    "replay_events",
    pathlib.Path("class-02C-work/replay_events.py"),
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

sys.argv = [
    "replay_events.py",
    "class-02C-work/events.jsonl",
    "--project-id", "gen-lang-client-0546914885",
    "--speed", "4",
]
mod.main()
