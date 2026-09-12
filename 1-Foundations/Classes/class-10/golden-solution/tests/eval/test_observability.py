import time

from widgetware_sdr.eval.observability import ObservabilityRecorder, stage_timer


def test_explain_final_status_reads_the_last_recorded_stage() -> None:
    recorder = ObservabilityRecorder()
    recorder.record("req-1", "acme-001", "researching", "ok", 12.0)
    recorder.record("req-1", "acme-001", "qualifying", "ok", 8.0)
    recorder.record("req-1", "acme-001", "blocked", "error", 1.0)

    explanation = recorder.explain_final_status("req-1")
    assert "blocked" in explanation
    assert "error" in explanation


def test_unknown_request_id_is_explained_honestly() -> None:
    recorder = ObservabilityRecorder()
    assert "no events recorded" in recorder.explain_final_status("does-not-exist")


def test_stage_timer_records_a_positive_latency() -> None:
    recorder = ObservabilityRecorder()
    with stage_timer(recorder, "req-2", "acme-001", "researching") as t:
        time.sleep(0.001)
    assert t.latency_ms > 0
    events = recorder.events_for_request("req-2")
    assert events[0].status == "ok"


def test_stage_timer_records_error_status_on_exception() -> None:
    recorder = ObservabilityRecorder()
    try:
        with stage_timer(recorder, "req-3", "acme-001", "qualifying"):
            raise ValueError("boom")
    except ValueError:
        pass
    events = recorder.events_for_request("req-3")
    assert events[0].status == "error"


def test_total_latency_sums_all_stages() -> None:
    recorder = ObservabilityRecorder()
    recorder.record("req-4", "acme-001", "researching", "ok", 10.0)
    recorder.record("req-4", "acme-001", "qualifying", "ok", 20.0)
    assert recorder.total_latency_ms("req-4") == 30.0
