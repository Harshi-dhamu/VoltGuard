mod decision;
mod error;
mod models;

use std::io::{self, Read};

use decision::DecisionEngine;
use models::PhysicsResult;

fn main() {
    let exit_code = match run() {
        Ok(()) => 0,
        Err(error) => {
            eprintln!("Decision Engine error: {}", error);
            1
        }
    };

    std::process::exit(exit_code);
}

/// Reads PhysicsResult JSON from stdin and produces a DecisionResult JSON.
fn run() -> Result<(), Box<dyn std::error::Error>> {
    let mut input = String::new();

    io::stdin().read_to_string(&mut input)?;

    if input.trim().is_empty() {
        return Err("input JSON cannot be empty".into());
    }

    let physics_result: PhysicsResult = serde_json::from_str(&input)?;

    let engine = DecisionEngine::new();

    let decision_result = engine.evaluate_fail_closed(&physics_result);

    let output = serde_json::to_string_pretty(&decision_result)?;

    println!("{}", output);

    Ok(())
}