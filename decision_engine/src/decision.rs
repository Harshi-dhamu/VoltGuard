use crate::error::DecisionError;
use crate::models::{
    Decision,
    DecisionReason,
    DecisionResult,
    PhysicsResult,
    PhysicsStatus,
};

/// Core deterministic Decision Engine.
///
/// The engine evaluates physical safety information and produces
/// an explicit ALLOW or DROP decision with a machine-readable reason.
#[derive(Debug, Default)]
pub struct DecisionEngine;

impl DecisionEngine {
    /// Creates a new Decision Engine.
    pub fn new() -> Self {
        Self
    }

    /// Evaluates a Physics Engine result.
    ///
    /// Decision priority:
    ///
    /// 1. Validate required input.
    /// 2. Detect invalid physical values.
    /// 3. Check explicit physical safety limits.
    /// 4. Evaluate the Physics Engine status.
    /// 5. Fail closed for unknown conditions.
    pub fn evaluate(
        &self,
        result: &PhysicsResult,
    ) -> Result<DecisionResult, DecisionError> {
        self.validate_input(result)?;

        if self.pressure_exceeded(result) {
            return Ok(self.drop(
                &result.device_id,
                DecisionReason::PressureLimitExceeded,
            ));
        }

        if self.flow_exceeded(result) {
            return Ok(self.drop(
                &result.device_id,
                DecisionReason::FlowLimitExceeded,
            ));
        }

        if self.pump_speed_exceeded(result) {
            return Ok(self.drop(
                &result.device_id,
                DecisionReason::PumpSpeedExceeded,
            ));
        }

        match result.status {
            PhysicsStatus::Safe => Ok(self.allow(
                &result.device_id,
                DecisionReason::PhysicsStatusSafe,
            )),

            PhysicsStatus::Warning => Ok(self.drop(
                &result.device_id,
                DecisionReason::PhysicsStatusWarning,
            )),

            PhysicsStatus::CatastrophicFailure => Ok(self.drop(
                &result.device_id,
                DecisionReason::CatastrophicFailure,
            )),
        }
    }

    /// Creates an ALLOW decision.
    fn allow(
        &self,
        device_id: &str,
        reason: DecisionReason,
    ) -> DecisionResult {
        DecisionResult {
            device_id: device_id.to_string(),
            decision: Decision::Allow,
            reason,
        }
    }

    /// Creates a DROP decision.
    fn drop(
        &self,
        device_id: &str,
        reason: DecisionReason,
    ) -> DecisionResult {
        DecisionResult {
            device_id: device_id.to_string(),
            decision: Decision::Drop,
            reason,
        }
    }

    fn validate_input(
        &self,
        result: &PhysicsResult,
    ) -> Result<(), DecisionError> {
        if result.device_id.trim().is_empty() {
            return Err(DecisionError::InvalidInput(
                "device_id cannot be empty".to_string(),
            ));
        }

        if result.command.trim().is_empty() {
            return Err(DecisionError::InvalidInput(
                "command cannot be empty".to_string(),
            ));
        }

        if !result.value.is_finite() {
            return Err(DecisionError::InvalidInput(
                "command value must be finite".to_string(),
            ));
        }

        Ok(())
    }

    fn pressure_exceeded(&self, result: &PhysicsResult) -> bool {
        match (result.predicted_pressure, result.pressure_limit) {
            (Some(predicted), Some(limit)) => predicted > limit,
            _ => false,
        }
    }

    fn flow_exceeded(&self, result: &PhysicsResult) -> bool {
        match (result.predicted_flow, result.flow_limit) {
            (Some(predicted), Some(limit)) => predicted > limit,
            _ => false,
        }
    }

    fn pump_speed_exceeded(&self, result: &PhysicsResult) -> bool {
        match (result.pump_speed, result.pump_speed_limit) {
            (Some(speed), Some(limit)) => speed > limit,
            _ => false,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn safe_result() -> PhysicsResult {
        PhysicsResult {
            device_id: "PUMP_01".to_string(),
            command: "SET_SPEED".to_string(),
            value: 1500.0,
            unit: "RPM".to_string(),

            predicted_pressure: Some(80.0),
            pressure_limit: Some(100.0),

            predicted_flow: Some(200.0),
            flow_limit: Some(300.0),

            pump_speed: Some(1500.0),
            pump_speed_limit: Some(3000.0),

            status: PhysicsStatus::Safe,
        }
    }

    #[test]
    fn safe_result_should_allow() {
        let engine = DecisionEngine::new();

        let result = engine
            .evaluate(&safe_result())
            .expect("safe result should be valid");

        assert_eq!(result.decision, Decision::Allow);
        assert_eq!(result.reason, DecisionReason::PhysicsStatusSafe);
    }

    #[test]
    fn pressure_violation_should_have_specific_reason() {
        let engine = DecisionEngine::new();

        let mut physics = safe_result();
        physics.predicted_pressure = Some(150.0);

        let result = engine
            .evaluate(&physics)
            .expect("physics result should be valid");

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(
            result.reason,
            DecisionReason::PressureLimitExceeded
        );
    }

    #[test]
    fn flow_violation_should_have_specific_reason() {
        let engine = DecisionEngine::new();

        let mut physics = safe_result();
        physics.predicted_flow = Some(350.0);

        let result = engine
            .evaluate(&physics)
            .expect("physics result should be valid");

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(
            result.reason,
            DecisionReason::FlowLimitExceeded
        );
    }

    #[test]
    fn pump_speed_violation_should_have_specific_reason() {
        let engine = DecisionEngine::new();

        let mut physics = safe_result();
        physics.pump_speed = Some(4000.0);

        let result = engine
            .evaluate(&physics)
            .expect("physics result should be valid");

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(
            result.reason,
            DecisionReason::PumpSpeedExceeded
        );
    }

    #[test]
    fn catastrophic_failure_should_have_specific_reason() {
        let engine = DecisionEngine::new();

        let mut physics = safe_result();
        physics.status = PhysicsStatus::CatastrophicFailure;

        let result = engine
            .evaluate(&physics)
            .expect("physics result should be valid");

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(
            result.reason,
            DecisionReason::CatastrophicFailure
        );
    }

    #[test]
    fn warning_should_have_specific_reason() {
        let engine = DecisionEngine::new();

        let mut physics = safe_result();
        physics.status = PhysicsStatus::Warning;

        let result = engine
            .evaluate(&physics)
            .expect("physics result should be valid");

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(
            result.reason,
            DecisionReason::PhysicsStatusWarning
        );
    }

    #[test]
    fn boundary_pressure_value_should_be_allowed() {
        let engine = DecisionEngine::new();

        let mut physics = safe_result();
        physics.predicted_pressure = Some(100.0);

        let result = engine
            .evaluate(&physics)
            .expect("boundary value should be valid");

        assert_eq!(result.decision, Decision::Allow);
    }

    #[test]
    fn empty_device_id_should_be_rejected() {
        let engine = DecisionEngine::new();

        let mut physics = safe_result();
        physics.device_id.clear();

        let result = engine.evaluate(&physics);

        assert!(result.is_err());
    }

    #[test]
    fn empty_command_should_be_rejected() {
        let engine = DecisionEngine::new();

        let mut physics = safe_result();
        physics.command.clear();

        let result = engine.evaluate(&physics);

        assert!(result.is_err());
    }
}