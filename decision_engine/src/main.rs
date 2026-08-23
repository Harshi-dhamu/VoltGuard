mod decision;
mod error;
mod models;

use std::io::{self, Read};

use decision::DecisionEngine;
use models::PhysicsResult;

fn main() {
    if let Err(error) = run() {
        eprintln!("Decision Engine error: {}", error);
        std::process::exit(1);
    }
}

/// Reads a PhysicsResult from stdin, evaluates it,
/// and writes the DecisionResult as JSON to stdout.
fn run() -> Result<(), Box<dyn std::error::Error>> {
    let mut input = String::new();

    io::stdin().read_to_string(&mut input)?;

    if input.trim().is_empty() {
        return Err("input JSON cannot be empty".into());
    }

    let physics_result: PhysicsResult = serde_json::from_str(&input)?;

    let engine = DecisionEngine::new();

    let decision_result = engine.evaluate(&physics_result)?;

    let output = serde_json::to_string_pretty(&decision_result)?;

    println!("{}", output);

    Ok(())
}