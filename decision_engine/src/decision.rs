use crate::error::DecisionError;
use crate::models::{
    Decision,
    DecisionReason,
    DecisionResult,
    PhysicsResult,
    PhysicsStatus,
};

/// Core Decision Engine.
///
/// The Decision Engine evaluates the physical safety result
/// produced by the Physics Engine and returns a security decision.
///
/// Day 3 implements the core deterministic rules:
/// - SAFE -> ALLOW
/// - CATASTROPHIC_FAILURE -> DROP
#[derive(Debug, Default)]
pub struct DecisionEngine;

impl DecisionEngine {
    /// Creates a new Decision Engine.
    pub fn new() -> Self {
        Self
    }

    /// Evaluates a Physics Engine result.
    ///
    /// The decision is deterministic:
    ///
    /// SAFE
    ///     -> ALLOW
    ///
    /// CATASTROPHIC_FAILURE
    ///     -> DROP
    ///
    /// WARNING is currently handled conservatively as DROP.
    /// More detailed physical safety rules will be added on Day 4.
    pub fn evaluate(
        &self,
        physics_result: &PhysicsResult,
    ) -> Result<DecisionResult, DecisionError> {
        self.validate_input(physics_result)?;

        self.evaluate_status(physics_result)
    }

    /// Applies the core status-based decision rules.
    fn evaluate_status(
        &self,
        physics_result: &PhysicsResult,
    ) -> Result<DecisionResult, DecisionError> {
        let (decision, reason) = match physics_result.status {
            PhysicsStatus::Safe => (
                Decision::Allow,
                DecisionReason::PhysicsStatusSafe,
            ),

            PhysicsStatus::Warning => (
                Decision::Drop,
                DecisionReason::PhysicsStatusWarning,
            ),

            PhysicsStatus::CatastrophicFailure => (
                Decision::Drop,
                DecisionReason::CatastrophicFailure,
            ),
        };

        Ok(DecisionResult {
            device_id: physics_result.device_id.clone(),
            decision,
            reason,
        })
    }

    /// Performs basic structural validation of the Physics Engine result.
    ///
    /// More comprehensive fail-closed validation will be added on Day 6.
    fn validate_input(
        &self,
        physics_result: &PhysicsResult,
    ) -> Result<(), DecisionError> {
        if physics_result.device_id.trim().is_empty() {
            return Err(DecisionError::InvalidInput(
                "device_id cannot be empty".to_string(),
            ));
        }

        if physics_result.command.trim().is_empty() {
            return Err(DecisionError::InvalidInput(
                "command cannot be empty".to_string(),
            ));
        }

        if physics_result.unit.trim().is_empty() {
            return Err(DecisionError::InvalidInput(
                "unit cannot be empty".to_string(),
            ));
        }

        if !physics_result.value.is_finite() {
            return Err(DecisionError::InvalidInput(
                "command value must be finite".to_string(),
            ));
        }

        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn create_result(status: PhysicsStatus) -> PhysicsResult {
        PhysicsResult {
            device_id: "PUMP_01".to_string(),
            command: "SET_SPEED".to_string(),
            value: 1500.0,
            unit: "RPM".to_string(),
            predicted_pressure: Some(80.0),
            pressure_limit: Some(100.0),
            predicted_flow: Some(200.0),
            status,
        }
    }

    #[test]
    fn safe_status_should_allow() {
        let engine = DecisionEngine::new();

        let result = engine
            .evaluate(&create_result(PhysicsStatus::Safe))
            .expect("SAFE result should produce a decision");

        assert_eq!(result.decision, Decision::Allow);
        assert_eq!(
            result.reason,
            DecisionReason::PhysicsStatusSafe
        );
    }

    #[test]
    fn catastrophic_failure_should_drop() {
        let engine = DecisionEngine::new();

        let result = engine
            .evaluate(&create_result(PhysicsStatus::CatastrophicFailure))
            .expect("catastrophic result should produce a decision");

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(
            result.reason,
            DecisionReason::CatastrophicFailure
        );
    }

    #[test]
    fn warning_should_drop_conservatively() {
        let engine = DecisionEngine::new();

        let result = engine
            .evaluate(&create_result(PhysicsStatus::Warning))
            .expect("WARNING result should produce a decision");

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(
            result.reason,
            DecisionReason::PhysicsStatusWarning
        );
    }

    #[test]
    fn safe_status_should_not_drop() {
        let engine = DecisionEngine::new();

        let result = engine
            .evaluate(&create_result(PhysicsStatus::Safe))
            .expect("SAFE result should produce a decision");

        assert_ne!(result.decision, Decision::Drop);
    }

    #[test]
    fn catastrophic_failure_should_not_allow() {
        let engine = DecisionEngine::new();

        let result = engine
            .evaluate(&create_result(PhysicsStatus::CatastrophicFailure))
            .expect("catastrophic result should produce a decision");

        assert_ne!(result.decision, Decision::Allow);
    }
}