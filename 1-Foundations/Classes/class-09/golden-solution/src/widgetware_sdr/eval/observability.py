"""Basic observability — Book 1, Chapter 10 (§10.6).

Captures request/workflow identifiers, stage names, state transitions,
and latency in a structured, inspectable form — enough to answer "why
did this case end in BLOCKED?" without reading logs by eye. This is a
local, in-memory recorder for the course; a real deployment would send
these events to Cloud Logging or an equivalent, not hold them in a
Python list.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ObservabilityEvent:
    request_id: str
    account_id: str
    stage: str
    status: str
    latency_ms: float
    details: dict[str, Any] = field(default_factory=dict)


class ObservabilityRecorder:
    """A small, local event log. Never records secrets or full sensitive
    payloads — only stage names, statuses, and timing, per §10.6's own
    caution.
    """

    def __init__(self) -> None:
        self._events: list[ObservabilityEvent] = []

    def record(
        self,
        request_id: str,
        account_id: str,
        stage: str,
        status: str,
        latency_ms: float,
        **details: Any,
    ) -> None:
        self._events.append(
            ObservabilityEvent(
                request_id=request_id,
                account_id=account_id,
                stage=stage,
                status=status,
                latency_ms=latency_ms,
                details=details,
            )
        )

    def events_for_request(self, request_id: str) -> list[ObservabilityEvent]:
        return [e for e in self._events if e.request_id == request_id]

    def explain_final_status(self, request_id: str) -> str:
        """Answer '§10.6: why did this case end in BLOCKED?' by reading
        the recorded stages, not by guessing.
        """
        events = self.events_for_request(request_id)
        if not events:
            return "no events recorded for this request_id"
        last = events[-1]
        return (
            f"ended at stage={last.stage!r} with status={last.status!r} "
            f"({len(events)} stage(s) recorded)"
        )

    def total_latency_ms(self, request_id: str) -> float:
        return sum(e.latency_ms for e in self.events_for_request(request_id))


class stage_timer:  # noqa: N801 — context manager named like a function deliberately
    """Small helper: `with stage_timer(recorder, request_id, account_id, "researching") as t: ...`
    then `t.latency_ms` is populated after the block exits.
    """

    def __init__(
        self, recorder: ObservabilityRecorder, request_id: str, account_id: str, stage: str
    ) -> None:
        self._recorder = recorder
        self._request_id = request_id
        self._account_id = account_id
        self._stage = stage
        self.latency_ms = 0.0
        self._start = 0.0

    def __enter__(self) -> "stage_timer":
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.latency_ms = (time.perf_counter() - self._start) * 1000
        status = "error" if exc_type else "ok"
        self._recorder.record(
            self._request_id, self._account_id, self._stage, status, self.latency_ms
        )
