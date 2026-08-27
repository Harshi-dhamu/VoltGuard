use crate::decision::DecisionEngine;
use crate::error::DecisionError;
use crate::models::{
    Decision,
    DecisionReason,
    DecisionResult,
};

use serde::Deserialize;
use std::collections::HashMap;

/// Status values currently produced by Dhruti's Physics Engine.
///
/// Dhruti's Physics Engine reports NORMAL, WARNING and CRITICAL.
/// UNKNOWN is used by this consumer when a status is missing,
/// empty or not recognized.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PhysicsEngineStatus {
    Normal,
    Warning,
    Critical,
    Unknown,
}

impl PhysicsEngineStatus {
    /// Converts a Physics Engine status string into a strongly typed status.
    ///
    /// Unknown or unavailable values are deliberately mapped to UNKNOWN
    /// so that the Decision Engine can fail closed.
    pub fn from_str(value: Option<&str>) -> Self {
        match value.map(str::trim).map(|value| value.to_uppercase()) {
            Some(value) if value == "NORMAL" => Self::Normal,
            Some(value) if value == "WARNING" => Self::Warning,
            Some(value) if value == "CRITICAL" => Self::Critical,
            _ => Self::Unknown,
        }
    }
}

/// Flow information produced by Dhruti's Physics Engine.
#[derive(Debug, Clone, Deserialize)]
pub struct FlowData {
    pub pump_speed_rpm: f64,
    pub valve_position_percent: f64,
    pub pump_flow_lpm: f64,
    pub actual_flow_lpm: f64,
}

/// Tank information produced by Dhruti's Physics Engine.
#[derive(Debug, Clone, Deserialize)]
pub struct TankData {
    pub final_level_liters: f64,
    pub final_fill_percentage: f64,
}

/// Safety check for an individual physical component.
#[derive(Debug, Clone, Deserialize)]
pub struct SafetyCheck {
    pub status: String,
}

/// Safety information produced by Dhruti's Physics Engine.
#[derive(Debug, Clone, Deserialize)]
pub struct SafetyData {
    pub overall_status: String,
    pub checks: HashMap<String, SafetyCheck>,
}

/// Asset information from the Physics Engine telemetry.
#[derive(Debug, Clone, Deserialize)]
pub struct AssetData {
    pub asset_type: String,
    pub health_status: String,
}

/// Telemetry information produced by Dhruti's Physics Engine.
#[derive(Debug, Clone, Deserialize)]
pub struct TelemetryData {
    pub system_status: String,
    pub assets: HashMap<String, AssetData>,
}

/// Health summary produced by the Physics Engine.
#[derive(Debug, Clone, Deserialize)]
pub struct HealthSummary {
    pub system_status: String,
    pub total_assets: u32,
    pub normal_assets: u32,
    pub warning_assets: u32,
    pub critical_assets: u32,
}

/// Actual structured output currently produced by Dhruti's Physics Engine.
#[derive(Debug, Clone, Deserialize)]
pub struct DhrutiPhysicsOutput {
    pub flow: FlowData,
    pub tank: TankData,
    pub safety: SafetyData,
    pub telemetry: TelemetryData,
    pub health_summary: HealthSummary,
}

/// Consumes Dhruti's Physics Engine output and converts it into
/// a Decision Engine result.
///
/// The consumer is intentionally kept separate from the core
/// DecisionEngine so that future Physics Engine schema changes
/// can be handled here without rewriting the decision rules.
#[derive(Debug, Default)]
pub struct PhysicsConsumer;

impl PhysicsConsumer {
    /// Creates a new Physics Engine consumer.
    pub fn new() -> Self {
        Self
    }

    /// Parses Dhruti's JSON output.
    pub fn parse_json(
        &self,
        input: &str,
    ) -> Result<DhrutiPhysicsOutput, DecisionError> {
        if input.trim().is_empty() {
            return Err(DecisionError::InvalidInput(
                "physics engine output cannot be empty".to_string(),
            ));
        }

        let output: DhrutiPhysicsOutput = serde_json::from_str(input)?;

        self.validate_output(&output)?;

        Ok(output)
    }

    /// Consumes Dhruti's JSON output and produces a security decision.
    ///
    /// Safety policy:
    ///
    /// NORMAL   -> ALLOW
    /// WARNING  -> DROP
    /// CRITICAL -> DROP
    /// UNKNOWN  -> DROP
    pub fn evaluate_json(
        &self,
        input: &str,
    ) -> Result<DecisionResult, DecisionError> {
        let physics_output = self.parse_json(input)?;

        self.evaluate_output(&physics_output)
    }

    /// Evaluates an already parsed Physics Engine output.
    pub fn evaluate_output(
        &self,
        output: &DhrutiPhysicsOutput,
    ) -> Result<DecisionResult, DecisionError> {
        let status = PhysicsEngineStatus::from_str(
            Some(output.safety.overall_status.as_str()),
        );

        let device_id = self.resolve_device_id(output);

        match status {
            PhysicsEngineStatus::Normal => Ok(DecisionResult {
                device_id,
                decision: Decision::Allow,
                reason: DecisionReason::PhysicsStatusSafe,
            }),

            PhysicsEngineStatus::Warning => Ok(DecisionResult {
                device_id,
                decision: Decision::Drop,
                reason: DecisionReason::PhysicsStatusWarning,
            }),

            PhysicsEngineStatus::Critical => Ok(DecisionResult {
                device_id,
                decision: Decision::Drop,
                reason: DecisionReason::PhysicsStatusCritical,
            }),

            PhysicsEngineStatus::Unknown => Ok(DecisionResult {
                device_id,
                decision: Decision::Drop,
                reason: DecisionReason::UnknownPhysicsStatus,
            }),
        }
    }

    /// Validates numeric values coming from the Physics Engine.
    ///
    /// We do not reproduce Physics Engine safety calculations here.
    /// We only ensure that received numeric data is valid enough to trust.
    fn validate_output(
        &self,
        output: &DhrutiPhysicsOutput,
    ) -> Result<(), DecisionError> {
        let numeric_values = [
            output.flow.pump_speed_rpm,
            output.flow.valve_position_percent,
            output.flow.pump_flow_lpm,
            output.flow.actual_flow_lpm,
            output.tank.final_level_liters,
            output.tank.final_fill_percentage,
        ];

        if numeric_values.iter().any(|value| !value.is_finite()) {
            return Err(DecisionError::InvalidInput(
                "physics engine output contains a non-finite numeric value"
                    .to_string(),
            ));
        }

        Ok(())
    }

    /// Resolves the affected asset for the DecisionResult.
    ///
    /// The current Physics Engine output does not contain a dedicated
    /// command/device identifier at the top level. Therefore, when
    /// exactly one asset exists, its identifier is used.
    ///
    /// For multiple assets, SYSTEM is used because the current schema
    /// represents an integrated system result rather than a specific
    /// command target.
    fn resolve_device_id(
        &self,
        output: &DhrutiPhysicsOutput,
    ) -> String {
        if output.telemetry.assets.len() == 1 {
            if let Some(device_id) = output.telemetry.assets.keys().next() {
                return device_id.clone();
            }
        }

        "SYSTEM".to_string()
    }
}

/// Keeps the core DecisionEngine referenced by this integration layer.
///
/// This function will be useful when the existing PhysicsResult contract
/// and Dhruti's final command-level output are unified during later
/// integration work.
pub fn decision_engine_available() -> DecisionEngine {
    DecisionEngine::new()
}

#[cfg(test)]
mod tests {
    use super::*;

    fn normal_output() -> &'static str {
        r#"
        {
          "flow": {
            "pump_speed_rpm": 2500.0,
            "valve_position_percent": 50.0,
            "pump_flow_lpm": 50.0,
            "actual_flow_lpm": 25.0
          },
          "tank": {
            "final_level_liters": 5250.0,
            "final_fill_percentage": 52.5
          },
          "safety": {
            "overall_status": "NORMAL",
            "checks": {
              "pump": {
                "status": "NORMAL"
              },
              "pipe_pressure": {
                "status": "NORMAL"
              },
              "tank": {
                "status": "NORMAL"
              }
            }
          },
          "telemetry": {
            "system_status": "NORMAL",
            "assets": {
              "PUMP_01": {
                "asset_type": "PUMP",
                "health_status": "NORMAL"
              },
              "VALVE_01": {
                "asset_type": "VALVE",
                "health_status": "NORMAL"
              },
              "PIPE_01": {
                "asset_type": "PIPE",
                "health_status": "NORMAL"
              },
              "TANK_01": {
                "asset_type": "TANK",
                "health_status": "NORMAL"
              }
            }
          },
          "health_summary": {
            "system_status": "NORMAL",
            "total_assets": 4,
            "normal_assets": 4,
            "warning_assets": 0,
            "critical_assets": 0
          }
        }
        "#
    }

    fn output_with_status(status: &str) -> String {
        normal_output().replace("\"NORMAL\"", &format!("\"{}\"", status))
    }

    #[test]
    fn normal_physics_result_should_allow() {
        let consumer = PhysicsConsumer::new();

        let result = consumer
            .evaluate_json(normal_output())
            .expect("normal output should be valid");

        assert_eq!(result.decision, Decision::Allow);
        assert_eq!(result.reason, DecisionReason::PhysicsStatusSafe);
        assert_eq!(result.device_id, "SYSTEM");
    }

    #[test]
    fn warning_physics_result_should_drop() {
        let consumer = PhysicsConsumer::new();

        let input = output_with_status("WARNING");

        let result = consumer
            .evaluate_json(&input)
            .expect("warning output should be valid");

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(result.reason, DecisionReason::PhysicsStatusWarning);
    }

    #[test]
    fn critical_physics_result_should_drop() {
        let consumer = PhysicsConsumer::new();

        let input = output_with_status("CRITICAL");

        let result = consumer
            .evaluate_json(&input)
            .expect("critical output should be valid");

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(result.reason, DecisionReason::PhysicsStatusCritical);
    }

    #[test]
    fn unknown_physics_status_should_drop() {
        let consumer = PhysicsConsumer::new();

        let input = output_with_status("SOMETHING_UNKNOWN");

        let result = consumer
            .evaluate_json(&input)
            .expect("unknown status should still be represented");

        assert_eq!(result.decision, Decision::Drop);
        assert_eq!(result.reason, DecisionReason::UnknownPhysicsStatus);
    }

    #[test]
    fn malformed_json_should_return_error() {
        let consumer = PhysicsConsumer::new();

        let result = consumer.evaluate_json("{ invalid json");

        assert!(result.is_err());
    }

    #[test]
    fn non_finite_physics_value_should_return_error() {
        let consumer = PhysicsConsumer::new();

        let input = normal_output().replace(
            "\"pump_speed_rpm\": 2500.0",
            "\"pump_speed_rpm\": 1e999"
        );

        let result = consumer.evaluate_json(&input);

        assert!(result.is_err());
    }
}