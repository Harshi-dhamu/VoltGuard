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
/// Day 2 focuses on using strongly typed decision models.
/// Detailed physical safety rules will be expanded in later days.
#[derive(Debug, Default)]
pub struct DecisionEngine;

impl DecisionEngine {
    /// Creates a new Decision Engine.
    pub fn new() -> Self {
        Self
    }

    /// Evaluates a Physics Engine result.
    ///
    /// Current basic policy:
    /// - SAFE -> ALLOW
    /// - CATASTROPHIC_FAILURE -> DROP
    ///
    /// WARNING policy will be finalized as part of the later
    /// safety-rule implementation.
    pub fn evaluate(
        &self,
        physics_result: &PhysicsResult,
    ) -> Result<DecisionResult, DecisionError> {
        self.validate_input(physics_result)?;

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
    fn safe_status_uses_allow_decision_reason() {
        let engine = DecisionEngine::new();

        let result = engine
            .evaluate(&create_result(PhysicsStatus::Safe))
            .expect("safe result should be accepted");

        assert_eq!(result.decision, Decision::Allow);
        assert_eq!(
            result.reason,
            DecisionReason::PhysicsStatusSafe
        );
    }

    #[test]
    fn warning_status_has_explicit_decision_reason() {
        let engine = DecisionEngine::new();

        let result = engine
            .evaluate(&create_result(PhysicsStatus::Warning))
            .expect("warning result should produce a decision");

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(
            result.reason,
            DecisionReason::PhysicsStatusWarning
        );
    }

    #[test]
    fn catastrophic_status_uses_catastrophic_reason() {
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
    fn empty_device_id_should_be_rejected() {
        let engine = DecisionEngine::new();

        let mut input = create_result(PhysicsStatus::Safe);
        input.device_id.clear();

        let result = engine.evaluate(&input);

        assert!(result.is_err());
    }

    #[test]
    fn empty_command_should_be_rejected() {
        let engine = DecisionEngine::new();

        let mut input = create_result(PhysicsStatus::Safe);
        input.command.clear();

        let result = engine.evaluate(&input);

        assert!(result.is_err());
    }
}