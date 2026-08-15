use std::fmt;

/// Errors that can occur while processing a Decision Engine request.
#[derive(Debug)]
pub enum DecisionError {
    InvalidInput(String),
    JsonError(String),
}

impl fmt::Display for DecisionError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            DecisionError::InvalidInput(message) => {
                write!(formatter, "Invalid input: {message}")
            }

            DecisionError::JsonError(message) => {
                write!(formatter, "JSON error: {message}")
            }
        }
    }
}

impl std::error::Error for DecisionError {}

impl From<serde_json::Error> for DecisionError {
    fn from(error: serde_json::Error) -> Self {
        DecisionError::JsonError(error.to_string())
    }
}