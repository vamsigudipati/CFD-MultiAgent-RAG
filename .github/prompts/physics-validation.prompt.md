---
description: "Run the full automated physics-validation checklist against a solver, ROM, or PINN change and report pass/fail."
agent: "agent"
argument-hint: "Name the changed file(s)/model checkpoint to validate"
tools: ["runTests", "search"]
---
# Automated Physics Validation

For the change the user names:

1. Load `docs/copilot/physics_validation_rules.md` and check each numbered rule against the current change. Skip rules that don't apply (state which, and why, in one line).
2. If a `pytest` regression/physics test already exists for this component, run it and report actual pass/fail — don't guess at results.
3. If no baseline/regression test exists yet, say so explicitly and propose the minimal test needed (following the Test Automation Standards in `.github/copilot-instructions.md`) rather than fabricating a validation result.
4. Produce the output table specified at the end of `docs/copilot/physics_validation_rules.md` ("What done looks like"): metric, baseline, new value, pass/fail vs. the 5% threshold.
5. If any rule fails, stop and report — do not proceed to suggest unrelated code changes.
