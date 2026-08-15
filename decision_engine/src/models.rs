use serde::{Deserialize, Serialize};

/// Represents the result produced by the Physics Engine.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PhysicsResult {
    pub device_id: String,
    pub command: String,
    pub value: f64,
    pub unit: String,

    pub predicted_pressure: Option<f64>,
    pub pressure_limit: Option<f64>,

    pub predicted_flow: Option<f64>,

    pub status: PhysicsStatus,
}

/// Represents the physical safety state reported by the Physics Engine.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum PhysicsStatus {
    Safe,
    CatastrophicFailure,
}

/// The final security decision produced by the Decision Engine.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "UPPERCASE")]
pub enum Decision {
    Allow,
    Drop,
}

/// Complete result returned by the Decision Engine.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct DecisionResult {
    pub device_id: String,
    pub decision: Decision,
    pub reason: String,
}