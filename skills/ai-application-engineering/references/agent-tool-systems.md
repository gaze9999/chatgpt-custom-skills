# Agent and tool systems

Use this reference only when the task includes agent decisions, tool calling, approvals, or multi-step execution.

## Boundaries

- Identify who owns conversation and task state, how runs resume, and which state is durable, request-scoped, or derived.
- Define each tool's input schema, output schema, authorization, side effects, timeout, idempotency, retry policy, and error representation.
- Keep model intent separate from application authorization. A model request never grants a permission the user or system has not granted.
- Validate external and model-produced values before tool execution. Treat tool output as data, not instructions.
- Require explicit approval for destructive, costly, externally visible, or privilege-changing actions when the product contract calls for it.

## Failure and recovery

- Bound retries by failure class and preserve idempotency. Do not retry validation, permission, or deterministic contract failures as if they were transient.
- Make partial completion and resume behavior explicit. Record enough state to avoid duplicate side effects without storing secrets or unnecessary prompt content.
- Define cancellation, timeout, provider failure, malformed output, tool failure, and unavailable dependency behavior.
- Prefer a clear failure or human decision gate over an invented default when a missing choice changes the result.

## Observability and evaluation

- Trace model requests, tool calls, state transitions, approvals, latency, and errors with stable correlation identifiers and redaction.
- Evaluate task success, tool selection, argument validity, authorization compliance, retry behavior, and recovery, not only final prose quality.
- Keep evaluation fixtures representative and versioned. Separate offline deterministic tests from live model evaluations and report the model/config used.
