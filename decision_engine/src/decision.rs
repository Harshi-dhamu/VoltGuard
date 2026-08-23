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
/// The Decision Engine follows a fail-closed security model:
///
/// - Trusted SAFE result -> ALLOW
/// - Physical safety violation -> DROP
/// - CATASTROPHIC_FAILURE -> DROP
/// - Invalid PhysicsResult -> DROP
///
/// The engine does not silently allow an untrusted result.
#[derive(Debug, Default)]
pub struct DecisionEngine;

impl DecisionEngine {
    /// Creates a new Decision Engine.
    pub fn new() -> Self {
        Self
    }

    /// Evaluates a trusted PhysicsResult.
    ///
    /// Returns an error if the input cannot be trusted.
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

    /// Fail-closed evaluation.
    ///
    /// If the PhysicsResult is invalid, this method returns DROP
    /// instead of allowing the command.
    ///
    /// This method is intended for the security decision boundary.
    pub fn evaluate_fail_closed(
        &self,
        physics_result: &PhysicsResult,
    ) -> DecisionResult {
        match self.evaluate(physics_result) {
            Ok(result) => result,

            Err(_) => DecisionResult {
                device_id: if physics_result.device_id.trim().is_empty() {
                    "UNKNOWN".to_string()
                } else {
                    physics_result.device_id.clone()
                },
                decision: Decision::Drop,
                reason: DecisionReason::InvalidInput,
            },
        }
    }

    /// Validates the basic structure and values of a PhysicsResult.
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

        self.validate_optional_value(
            physics_result.predicted_pressure,
            "predicted_pressure",
        )?;

        self.validate_optional_value(
            physics_result.pressure_limit,
            "pressure_limit",
        )?;

        self.validate_optional_value(
            physics_result.predicted_flow,
            "predicted_flow",
        )?;

        self.validate_optional_value(
            physics_result.flow_limit,
            "flow_limit",
        )?;

        self.validate_optional_value(
            physics_result.pump_speed,
            "pump_speed",
        )?;

        self.validate_optional_value(
            physics_result.pump_speed_limit,
            "pump_speed_limit",
        )?;

        Ok(())
    }

    /// Validates an optional numeric physical value.
    fn validate_optional_value(
        &self,
        value: Option<f64>,
        field_name: &str,
    ) -> Result<(), DecisionError> {
        if let Some(value) = value {
            if !value.is_finite() {
                return Err(DecisionError::InvalidInput(format!(
                    "{} must be finite",
                    field_name
                )));
            }
        }

        Ok(())
    }

    /// Checks pressure safety.
    fn check_pressure_rule(
        &self,
        physics_result: &PhysicsResult,
    ) -> Result<Option<DecisionReason>, DecisionError> {
        match (
            physics_result.predicted_pressure,
            physics_result.pressure_limit,
        ) {
            (Some(predicted), Some(limit)) => {
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

    /// Checks flow safety.
    fn check_flow_rule(
        &self,
        physics_result: &PhysicsResult,
    ) -> Result<Option<DecisionReason>, DecisionError> {
        match (
            physics_result.predicted_flow,
            physics_result.flow_limit,
        ) {
            (Some(predicted), Some(limit)) => {
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

    /// Checks pump-speed safety.
    fn check_pump_speed_rule(
        &self,
        physics_result: &PhysicsResult,
    ) -> Result<Option<DecisionReason>, DecisionError> {
        match (
            physics_result.pump_speed,
            physics_result.pump_speed_limit,
        ) {
            (Some(speed), Some(limit)) => {
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

    /// Checks for invalid physical states.
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

        if physics_result
            .pressure_limit
            .is_some_and(|value| value < 0.0)
        {
            return Some(DecisionReason::InvalidPhysicalState);
        }

        if physics_result
            .flow_limit
            .is_some_and(|value| value < 0.0)
        {
            return Some(DecisionReason::InvalidPhysicalState);
        }

        if physics_result
            .pump_speed_limit
            .is_some_and(|value| value < 0.0)
        {
            return Some(DecisionReason::InvalidPhysicalState);
        }

        None
    }

    /// Creates a DROP result.
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
            .expect("safe result should be valid");

        assert_eq!(result.decision, Decision::Allow);
    }

    #[test]
    fn catastrophic_result_should_drop() {
        let engine = DecisionEngine::new();

        let mut input = create_safe_result();
        input.status = PhysicsStatus::CatastrophicFailure;

        let result = engine
            .evaluate(&input)
            .expect("catastrophic result should be valid");

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(
            result.reason,
            DecisionReason::CatastrophicFailure
        );
    }

    #[test]
    fn invalid_device_id_should_fail_closed() {
        let engine = DecisionEngine::new();

        let mut input = create_safe_result();
        input.device_id = String::new();

        let result = engine.evaluate_fail_closed(&input);

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(
            result.reason,
            DecisionReason::InvalidInput
        );
    }

    #[test]
    fn invalid_command_should_fail_closed() {
        let engine = DecisionEngine::new();

        let mut input = create_safe_result();
        input.command = String::new();

        let result = engine.evaluate_fail_closed(&input);

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(
            result.reason,
            DecisionReason::InvalidInput
        );
    }

    #[test]
    fn nan_command_value_should_fail_closed() {
        let engine = DecisionEngine::new();

        let mut input = create_safe_result();
        input.value = f64::NAN;

        let result = engine.evaluate_fail_closed(&input);

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(
            result.reason,
            DecisionReason::InvalidInput
        );
    }

    #[test]
    fn infinite_pressure_should_fail_closed() {
        let engine = DecisionEngine::new();

        let mut input = create_safe_result();
        input.predicted_pressure = Some(f64::INFINITY);

        let result = engine.evaluate_fail_closed(&input);

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(
            result.reason,
            DecisionReason::InvalidInput
        );
    }

    #[test]
    fn missing_pressure_limit_should_fail_closed() {
        let engine = DecisionEngine::new();

        let mut input = create_safe_result();
        input.pressure_limit = None;

        let result = engine.evaluate_fail_closed(&input);

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(
            result.reason,
            DecisionReason::InvalidInput
        );
    }

    #[test]
    fn missing_flow_limit_should_fail_closed() {
        let engine = DecisionEngine::new();

        let mut input = create_safe_result();
        input.flow_limit = None;

        let result = engine.evaluate_fail_closed(&input);

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(
            result.reason,
            DecisionReason::InvalidInput
        );
    }

    #[test]
    fn missing_pump_speed_limit_should_fail_closed() {
        let engine = DecisionEngine::new();

        let mut input = create_safe_result();
        input.pump_speed_limit = None;

        let result = engine.evaluate_fail_closed(&input);

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(
            result.reason,
            DecisionReason::InvalidInput
        );
    }

    #[test]
    fn negative_physical_value_should_drop() {
        let engine = DecisionEngine::new();

        let mut input = create_safe_result();
        input.predicted_flow = Some(-10.0);

        let result = engine
            .evaluate(&input)
            .expect("negative physical state should be handled");

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(
            result.reason,
            DecisionReason::InvalidPhysicalState
        );
    }
}