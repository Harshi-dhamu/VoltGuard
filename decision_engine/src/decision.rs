use crate::error::DecisionError;
use crate::models::{
    Decision,
    DecisionResult,
    PhysicsResult,
    PhysicsStatus,
};

/// Core Decision Engine.
///
/// The engine receives a Physics Engine result and produces
/// a deterministic ALLOW or DROP decision.
#[derive(Debug, Default)]
pub struct DecisionEngine;

impl DecisionEngine {
    /// Creates a new Decision Engine.
    pub fn new() -> Self {
        Self
    }

    /// Evaluates a Physics Engine result.
    ///
    /// Day 1 rules:
    /// - SAFE -> ALLOW
    /// - CATASTROPHIC_FAILURE -> DROP
    pub fn evaluate(
        &self,
        physics_result: &PhysicsResult,
    ) -> Result<DecisionResult, DecisionError> {
        self.validate_input(physics_result)?;

        let (decision, reason) = match physics_result.status {
            PhysicsStatus::Safe => {
                (Decision::Allow, "PHYSICS_STATUS_SAFE")
            }

            PhysicsStatus::CatastrophicFailure => {
                (Decision::Drop, "CATASTROPHIC_FAILURE")
            }
        };

        Ok(DecisionResult {
            device_id: physics_result.device_id.clone(),
            decision,
            reason: reason.to_string(),
        })
    }

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

    fn create_safe_result() -> PhysicsResult {
        PhysicsResult {
            device_id: "PUMP_01".to_string(),
            command: "SET_SPEED".to_string(),
            value: 1500.0,
            unit: "RPM".to_string(),
            predicted_pressure: Some(80.0),
            pressure_limit: Some(100.0),
            predicted_flow: Some(200.0),
            status: PhysicsStatus::Safe,
        }
    }

    fn create_catastrophic_result() -> PhysicsResult {
        PhysicsResult {
            device_id: "PUMP_01".to_string(),
            command: "SET_SPEED".to_string(),
            value: 50000.0,
            unit: "RPM".to_string(),
            predicted_pressure: Some(250.0),
            pressure_limit: Some(100.0),
            predicted_flow: Some(450.0),
            status: PhysicsStatus::CatastrophicFailure,
        }
    }

    #[test]
    fn safe_result_should_allow() {
        let engine = DecisionEngine::new();

        let result = engine
            .evaluate(&create_safe_result())
            .expect("safe input should produce a decision");

        assert_eq!(result.decision, Decision::Allow);
        assert_eq!(result.reason, "PHYSICS_STATUS_SAFE");
    }

    #[test]
    fn catastrophic_result_should_drop() {
        let engine = DecisionEngine::new();

        let result = engine
            .evaluate(&create_catastrophic_result())
            .expect("catastrophic input should produce a decision");

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(result.reason, "CATASTROPHIC_FAILURE");
    }

    #[test]
    fn empty_device_id_should_be_rejected() {
        let engine = DecisionEngine::new();

        let mut input = create_safe_result();
        input.device_id = String::new();

        let result = engine.evaluate(&input);

        assert!(result.is_err());
    }

    #[test]
    fn empty_command_should_be_rejected() {
        let engine = DecisionEngine::new();

        let mut input = create_safe_result();
        input.command = String::new();

        let result = engine.evaluate(&input);

        assert!(result.is_err());
    }
}