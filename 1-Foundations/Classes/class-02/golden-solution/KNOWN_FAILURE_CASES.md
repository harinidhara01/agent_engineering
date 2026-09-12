# Known Failure Cases — Class 2 Checkpoint

## Carried forward from Class 1

- `expected_qualification_direction` and `rationale` in `tests/fixtures/expected/*.yaml` are still hand-derived predictions, unverified by any qualification agent (that starts Class 5+).
- The three scenario accounts are still illustrative, not a representative dataset.

## New at this checkpoint

### 1. "Resists injection" here means structural isolation, not model behavior

`test_a_malicious_note_cannot_override_system_instructions` proves the malicious text can never occupy the same position as system instructions in the assembled prompt. It proves nothing about whether a real Gemini call, given this exact assembled prompt, would actually ignore the embedded instruction. That claim is untestable until Class 3 makes a real model call, and even then, one passing test is evidence, not a guarantee, for every possible injection phrasing.

### 2. `meets_minimum_employee_count: null` vs. `false` is a real, easy-to-reintroduce bug class

`tests/fixtures/expected/meridian-003.yaml` deliberately encodes "unknown" as `null`, distinct from "fails the criterion" (`false`). `context_builder.py` itself does not yet enforce this distinction anywhere — it only carries `employee_count: None` through unmodified. A future chapter's qualification logic that does `employee_count >= minimum_employee_count` without a null check first will silently evaluate `None >= 5000` and raise a `TypeError` in Python — or, worse, in a language that permits it, silently coerce to a wrong boolean. This checkpoint's tests catch the data going in correctly; they do not yet catch a future consumer handling it incorrectly.

### 3. Business config drift is not detected by any test at this checkpoint

`config/icp.yaml`, `docs/widgetware-business-brief.md`, and `tests/fixtures/expected/*.yaml`'s `icp_match` sections must all agree by hand. Nothing here fails loudly if `config/icp.yaml`'s `minimum_employee_count` is edited without updating the other two — a genuine, currently-unclosed gap. Consider this a candidate for a Class 4+ contract test once schemas exist.

### 4. `context_builder.py` reads YAML files with no schema validation

`load_config()` will happily return whatever a malformed `config/*.yaml` file contains, including a wrong type or a missing key, and fail with a raw `KeyError` deep inside `build_context()` rather than a clear, named error. Structured contract validation for configuration itself is out of scope for Book 1 and is not solved anywhere in this course.
