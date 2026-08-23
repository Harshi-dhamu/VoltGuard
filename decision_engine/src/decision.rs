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
/// Evaluates physical safety results and determines whether
/// an industrial command should be allowed or dropped.
#[derive(Debug, Default)]
pub struct DecisionEngine;

impl DecisionEngine {
    /// Creates a new Decision Engine.
    pub fn new() -> Self {
        Self
    }

    /// Evaluates a Physics Engine result.
    ///
    /// Decision order:
    ///
    /// 1. Validate the input.
    /// 2. Reject catastrophic physical states.
    /// 3. Apply physical safety rules.
    /// 4. Apply the remaining status policy.
    pub fn evaluate(
        &self,
        physics_result: &PhysicsResult,
    ) -> Result<DecisionResult, DecisionError> {
        self.validate_input(physics_result)?;

        if physics_result.status == PhysicsStatus::CatastrophicFailure {
            return Ok(self.create_drop_result(
                physics_result,
                DecisionReason::CatastrophicFailure,
            ));
        }

        if let Some(reason) = self.check_pressure_rule(physics_result)? {
            return Ok(self.create_drop_result(physics_result, reason));
        }

        if let Some(reason) = self.check_flow_rule(physics_result)? {
            return Ok(self.create_drop_result(physics_result, reason));
        }

        if let Some(reason) = self.check_pump_speed_rule(physics_result)? {
            return Ok(self.create_drop_result(physics_result, reason));
        }

        if let Some(reason) = self.check_physical_state(physics_result) {
            return Ok(self.create_drop_result(physics_result, reason));
        }

        match physics_result.status {
            PhysicsStatus::Safe => Ok(DecisionResult {
                device_id: physics_result.device_id.clone(),
                decision: Decision::Allow,
                reason: DecisionReason::PhysicsStatusSafe,
            }),

            PhysicsStatus::Warning => Ok(self.create_drop_result(
                physics_result,
                DecisionReason::PhysicsStatusWarning,
            )),

            PhysicsStatus::CatastrophicFailure => Ok(self.create_drop_result(
                physics_result,
                DecisionReason::CatastrophicFailure,
            )),
        }
    }

    /// Checks whether predicted pressure exceeds the configured limit.
    fn check_pressure_rule(
        &self,
        physics_result: &PhysicsResult,
    ) -> Result<Option<DecisionReason>, DecisionError> {
        match (
            physics_result.predicted_pressure,
            physics_result.pressure_limit,
        ) {
            (Some(predicted), Some(limit)) => {
                if !predicted.is_finite() || !limit.is_finite() {
                    return Err(DecisionError::InvalidInput(
                        "pressure values must be finite".to_string(),
                    ));
                }

                if predicted > limit {
                    return Ok(Some(DecisionReason::PressureLimitExceeded));
                }

                Ok(None)
            }

            (None, None) => Ok(None),

            _ => Err(DecisionError::InvalidInput(
                "predicted_pressure and pressure_limit must be provided together"
                    .to_string(),
            )),
        }
    }

    /// Checks whether predicted flow exceeds the configured limit.
    fn check_flow_rule(
        &self,
        physics_result: &PhysicsResult,
    ) -> Result<Option<DecisionReason>, DecisionError> {
        match (
            physics_result.predicted_flow,
            physics_result.flow_limit,
        ) {
            (Some(predicted), Some(limit)) => {
                if !predicted.is_finite() || !limit.is_finite() {
                    return Err(DecisionError::InvalidInput(
                        "flow values must be finite".to_string(),
                    ));
                }

                if predicted > limit {
                    return Ok(Some(DecisionReason::FlowLimitExceeded));
                }

                Ok(None)
            }

            (None, None) => Ok(None),

            _ => Err(DecisionError::InvalidInput(
                "predicted_flow and flow_limit must be provided together"
                    .to_string(),
            )),
        }
    }

    /// Checks whether pump speed exceeds the configured limit.
    fn check_pump_speed_rule(
        &self,
        physics_result: &PhysicsResult,
    ) -> Result<Option<DecisionReason>, DecisionError> {
        match (
            physics_result.pump_speed,
            physics_result.pump_speed_limit,
        ) {
            (Some(speed), Some(limit)) => {
                if !speed.is_finite() || !limit.is_finite() {
                    return Err(DecisionError::InvalidInput(
                        "pump speed values must be finite".to_string(),
                    ));
                }

                if speed > limit {
                    return Ok(Some(DecisionReason::PumpSpeedExceeded));
                }

                Ok(None)
            }

            (None, None) => Ok(None),

            _ => Err(DecisionError::InvalidInput(
                "pump_speed and pump_speed_limit must be provided together"
                    .to_string(),
            )),
        }
    }

    /// Checks for obviously invalid physical states.
    ///
    /// Negative physical quantities are rejected because they are
    /// invalid for the positive-valued quantities represented here.
    fn check_physical_state(
        &self,
        physics_result: &PhysicsResult,
    ) -> Option<DecisionReason> {
        if physics_result
            .predicted_pressure
            .is_some_and(|value| value < 0.0)
        {
            return Some(DecisionReason::InvalidPhysicalState);
        }

        if physics_result
            .predicted_flow
            .is_some_and(|value| value < 0.0)
        {
            return Some(DecisionReason::InvalidPhysicalState);
        }

        if physics_result
            .pump_speed
            .is_some_and(|value| value < 0.0)
        {
            return Some(DecisionReason::InvalidPhysicalState);
        }

        None
    }

    /// Creates a DROP result with the supplied reason.
    fn create_drop_result(
        &self,
        physics_result: &PhysicsResult,
        reason: DecisionReason,
    ) -> DecisionResult {
        DecisionResult {
            device_id: physics_result.device_id.clone(),
            decision: Decision::Drop,
            reason,
        }
    }

    /// Performs basic input validation.
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
            .evaluate(&create_safe_result())
            .expect("safe result should produce a decision");

        assert_eq!(result.decision, Decision::Allow);
        assert_eq!(
            result.reason,
            DecisionReason::PhysicsStatusSafe
        );
    }

    #[test]
    fn pressure_above_limit_should_drop() {
        let engine = DecisionEngine::new();

        let mut input = create_safe_result();
        input.predicted_pressure = Some(101.0);

        let result = engine
            .evaluate(&input)
            .expect("pressure violation should produce a decision");

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(
            result.reason,
            DecisionReason::PressureLimitExceeded
        );
    }

    #[test]
    fn flow_above_limit_should_drop() {
        let engine = DecisionEngine::new();

        let mut input = create_safe_result();
        input.predicted_flow = Some(301.0);

        let result = engine
            .evaluate(&input)
            .expect("flow violation should produce a decision");

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(
            result.reason,
            DecisionReason::FlowLimitExceeded
        );
    }

    #[test]
    fn pump_speed_above_limit_should_drop() {
        let engine = DecisionEngine::new();

        let mut input = create_safe_result();
        input.pump_speed = Some(3001.0);

        let result = engine
            .evaluate(&input)
            .expect("pump speed violation should produce a decision");

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(
            result.reason,
            DecisionReason::PumpSpeedExceeded
        );
    }

    #[test]
    fn negative_pressure_should_drop() {
        let engine = DecisionEngine::new();

        let mut input = create_safe_result();
        input.predicted_pressure = Some(-1.0);

        let result = engine
            .evaluate(&input)
            .expect("invalid physical state should produce a decision");

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(
            result.reason,
            DecisionReason::InvalidPhysicalState
        );
    }

    #[test]
    fn catastrophic_failure_should_drop() {
        let engine = DecisionEngine::new();

        let mut input = create_safe_result();
        input.status = PhysicsStatus::CatastrophicFailure;

        let result = engine
            .evaluate(&input)
            .expect("catastrophic state should produce a decision");

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(
            result.reason,
            DecisionReason::CatastrophicFailure
        );
    }

    #[test]
    fn boundary_pressure_equal_to_limit_should_allow() {
        let engine = DecisionEngine::new();

        let mut input = create_safe_result();
        input.predicted_pressure = Some(100.0);

        let result = engine
            .evaluate(&input)
            .expect("boundary pressure should produce a decision");

        assert_eq!(result.decision, Decision::Allow);
    }

    #[test]
    fn missing_pressure_pair_should_be_rejected() {
        let engine = DecisionEngine::new();

        let mut input = create_safe_result();
        input.predicted_pressure = None;

        let result = engine.evaluate(&input);

        assert!(result.is_err());
    }
}