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
    PhysicsStatusCritical,

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

impl DecisionReason {
    /// Returns a human-readable explanation for the decision reason.
    pub fn description(&self) -> &'static str {
        match self {
            Self::PhysicsStatusSafe =>
                "Physics Engine reported a safe physical state.",

            Self::PhysicsStatusWarning =>
                "Physics Engine reported a warning physical state.",

            Self::PhysicsStatusCritical =>
                "Physics Engine reported a critical physical state.",

            Self::CatastrophicFailure =>
                "Physics Engine predicted a catastrophic physical failure.",

            Self::PressureLimitExceeded =>
                "Predicted pressure exceeds the configured safe pressure limit.",

            Self::FlowLimitExceeded =>
                "Predicted flow exceeds the configured safe flow limit.",

            Self::PumpSpeedExceeded =>
                "Predicted pump speed exceeds the configured safe pump speed limit.",

            Self::InvalidPhysicalState =>
                "The physical state returned by the Physics Engine is invalid.",

            Self::InvalidInput =>
                "The Decision Engine received invalid input.",

            Self::MissingPhysicsData =>
                "Required physics data is missing.",

            Self::UnknownPhysicsStatus =>
                "The Physics Engine returned an unknown or unavailable status.",
        }
    }
}