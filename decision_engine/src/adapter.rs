





use crate::models::{Decision, DecisionReason, DecisionResult};
use serde::{Deserialize, Serialize};
use std::time::{SystemTime, UNIX_EPOCH};

/// Standardized event produced by the Decision Engine.
///
/// This follows the common IntegrationEvent-compatible structure
/// requested by the dashboard/integration team.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct IntegrationEvent {
    pub event_id: String,
    pub source_module: String,
    pub event_type: String,
    pub timestamp: String,
    pub severity: String,
    pub asset: String,
    pub message: String,
    pub payload: DecisionEventPayload,
}

/// Decision-specific information stored inside the event payload.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct DecisionEventPayload {
    pub decision: String,
    pub reason: String,
    pub source_event_id: Option<String>,
}

/// Adapter responsible for converting Decision Engine output
/// into the common IntegrationEvent-compatible format.
pub struct DecisionEventAdapter;

impl DecisionEventAdapter {
    /// Converts an existing DecisionResult into an integration event.
    pub fn create_event(
        decision_result: &DecisionResult,
        event_id: impl Into<String>,
        source_event_id: Option<String>,
    ) -> IntegrationEvent {
        let decision = match decision_result.decision {
            Decision::Allow => "ALLOW",
            Decision::Drop => "BLOCK",
        };

        let severity = match decision_result.decision {
            Decision::Allow => "LOW",
            Decision::Drop => "HIGH",
        };

        let reason = decision_reason_to_string(&decision_result.reason);

        let message = format!(
            "Security decision generated for {}: {}",
            decision_result.device_id,
            decision
        );

        IntegrationEvent {
            event_id: event_id.into(),
            source_module: "decision_engine".to_string(),
            event_type: "SECURITY_DECISION".to_string(),
            timestamp: current_timestamp(),
            severity: severity.to_string(),
            asset: decision_result.device_id.clone(),
            message,
            payload: DecisionEventPayload {
                decision: decision.to_string(),
                reason,
                source_event_id,
            },
        }
    }

    /// Converts the integration event into JSON.
    pub fn to_json(
        event: &IntegrationEvent,
    ) -> Result<String, serde_json::Error> {
        serde_json::to_string_pretty(event)
    }
}

/// Converts the internal DecisionReason enum into the
/// standardized reason string expected by the integration layer.
fn decision_reason_to_string(reason: &DecisionReason) -> String {
    match reason {
        DecisionReason::PhysicsStatusSafe => {
            "PHYSICS_STATUS_SAFE".to_string()
        }

        DecisionReason::PhysicsStatusWarning => {
            "PHYSICS_STATUS_WARNING".to_string()
        }

        DecisionReason::PhysicsStatusCritical => {
            "PHYSICS_STATUS_CRITICAL".to_string()
        }

        DecisionReason::CatastrophicFailure => {
            "CATASTROPHIC_FAILURE".to_string()
        }

        DecisionReason::PressureLimitExceeded => {
            "PRESSURE_LIMIT_EXCEEDED".to_string()
        }

        DecisionReason::FlowLimitExceeded => {
            "FLOW_LIMIT_EXCEEDED".to_string()
        }

        DecisionReason::PumpSpeedExceeded => {
            "PUMP_SPEED_EXCEEDED".to_string()
        }

        DecisionReason::InvalidPhysicalState => {
            "INVALID_PHYSICAL_STATE".to_string()
        }

        DecisionReason::InvalidInput => {
            "INVALID_INPUT".to_string()
        }

        DecisionReason::MissingPhysicsData => {
            "MISSING_PHYSICS_DATA".to_string()
        }

        DecisionReason::UnknownPhysicsStatus => {
            "UNKNOWN_PHYSICS_STATUS".to_string()
        }
    }
}

/// Generates a lightweight timestamp.
///
/// The integration layer can normalize this timestamp later
/// if it requires a specific date/time representation.
fn current_timestamp() -> String {
    match SystemTime::now().duration_since(UNIX_EPOCH) {
        Ok(duration) => duration.as_secs().to_string(),
        Err(_) => "0".to_string(),
    }
}


#[cfg(test)]
mod tests {
    use super::*;
    use crate::models::{
        Decision,
        DecisionReason,
        DecisionResult,
    };

    fn safe_result() -> DecisionResult {
        DecisionResult {
            device_id: "PUMP_01".to_string(),
            decision: Decision::Allow,
            reason: DecisionReason::PhysicsStatusSafe,
        }
    }

    fn pressure_failure_result() -> DecisionResult {
        DecisionResult {
            device_id: "PUMP_01".to_string(),
            decision: Decision::Drop,
            reason: DecisionReason::PressureLimitExceeded,
        }
    }

    #[test]
    fn allow_decision_creates_correct_event() {
        let result = safe_result();

        let event = DecisionEventAdapter::create_event(
            &result,
            "DEC-0001",
            Some("PKT-0001".to_string()),
        );

        assert_eq!(event.event_id, "DEC-0001");
        assert_eq!(event.source_module, "decision_engine");
        assert_eq!(event.event_type, "SECURITY_DECISION");
        assert_eq!(event.severity, "LOW");
        assert_eq!(event.asset, "PUMP_01");

        assert_eq!(event.payload.decision, "ALLOW");
        assert_eq!(
            event.payload.reason,
            "PHYSICS_STATUS_SAFE"
        );

        assert_eq!(
            event.payload.source_event_id,
            Some("PKT-0001".to_string())
        );
    }

    #[test]
    fn drop_decision_creates_block_event() {
        let result = pressure_failure_result();

        let event = DecisionEventAdapter::create_event(
            &result,
            "DEC-0002",
            Some("PKT-0002".to_string()),
        );

        assert_eq!(event.event_id, "DEC-0002");
        assert_eq!(event.source_module, "decision_engine");
        assert_eq!(event.event_type, "SECURITY_DECISION");
        assert_eq!(event.severity, "HIGH");
        assert_eq!(event.asset, "PUMP_01");

        assert_eq!(event.payload.decision, "BLOCK");
        assert_eq!(
            event.payload.reason,
            "PRESSURE_LIMIT_EXCEEDED"
        );
    }

    #[test]
    fn adapter_supports_missing_source_event_id() {
        let result = safe_result();

        let event = DecisionEventAdapter::create_event(
            &result,
            "DEC-0003",
            None,
        );

        assert_eq!(
            event.payload.source_event_id,
            None
        );
    }

    #[test]
    fn event_serializes_to_json() {
        let result = pressure_failure_result();

        let event = DecisionEventAdapter::create_event(
            &result,
            "DEC-0004",
            Some("PKT-0004".to_string()),
        );

        let json = DecisionEventAdapter::to_json(&event)
            .expect("event should serialize successfully");

        assert!(json.contains("\"event_id\""));
        assert!(json.contains("\"source_module\""));
        assert!(json.contains("\"event_type\""));
        assert!(json.contains("\"timestamp\""));
        assert!(json.contains("\"severity\""));
        assert!(json.contains("\"asset\""));
        assert!(json.contains("\"message\""));
        assert!(json.contains("\"payload\""));

        assert!(json.contains("\"decision\""));
        assert!(json.contains("\"reason\""));
        assert!(json.contains("PRESSURE_LIMIT_EXCEEDED"));
    }
}























