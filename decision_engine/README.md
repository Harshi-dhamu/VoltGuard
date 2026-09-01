# VoltGuard Decision Engine

The Decision Engine is responsible for evaluating Physics Engine results
and determining whether an industrial control command should be allowed
or blocked.

## Architecture

Physics Engine
      ↓
Physics Consumer
      ↓
Decision Engine
      ↓
Decision Event Adapter
      ↓
IntegrationEvent-compatible JSON

## Decision Rules

| Physics Status | Decision |
|---|---|
| NORMAL | ALLOW |
| WARNING | BLOCK |
| CRITICAL | BLOCK |
| UNKNOWN | BLOCK |

The Decision Engine follows a fail-closed approach. Invalid or
untrusted physics data results in a blocked decision.

## Safety Rules

The engine supports detection of:

- Pressure limit exceeded
- Flow limit exceeded
- Pump speed exceeded
- Invalid physical state
- Invalid input
- Missing physics data
- Unknown physics status

## Integration Event

The adapter produces the following top-level fields:

- event_id
- source_module
- event_type
- timestamp
- severity
- asset
- message
- payload

The Decision Engine uses:

source_module = "decision_engine"

event_type = "SECURITY_DECISION"

## Testing

Run:

cargo check
cargo test
cargo build --release

## Dashboard Integration

The Decision Engine remains independent from the dashboard.

The dashboard integration is handled externally through the
IntegrationEvent-compatible output.