use serde::{Deserialize, Serialize};

/// Result produced by the Physics Engine.
///
/// This structure represents the physical consequences predicted
/// for an industrial command.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PhysicsResult {
    pub device_id: String,
    pub command: String,
    pub value: f64,
    pub unit: String,

    pub predicted_pressure: Option<f64>,
    pub pressure_limit: Option<f64>,

    pub predicted_flow: Option<f64>,
    pub flow_limit: Option<f64>,

    pub pump_speed: Option<f64>,
    pub pump_speed_limit: Option<f64>,

    pub status: PhysicsStatus,
}

/// Physical safety state reported by the Physics Engine.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum PhysicsStatus {
    Safe,
    Warning,
    CatastrophicFailure,
}

/// Final security decision produced by the Decision Engine.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "UPPERCASE")]
pub enum Decision {
    Allow,
    Drop,
}

/// Explains why the Decision Engine produced a particular decision.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum DecisionReason {
    PhysicsStatusSafe,
    PhysicsStatusWarning,
    CatastrophicFailure,

    PressureLimitExceeded,
    FlowLimitExceeded,
    PumpSpeedExceeded,

    InvalidPhysicalState,
    InvalidInput,
    MissingPhysicsData,
    UnknownPhysicsStatus,
}

/// Complete decision returned by the Decision Engine.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct DecisionResult {
    pub device_id: String,
    pub decision: Decision,
    pub reason: DecisionReason,
}