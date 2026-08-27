mod decision;
mod error;
mod models;
mod physics_consumer;

use std::io::{self, Read};

use physics_consumer::PhysicsConsumer;

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

/// Reads Dhruti's Physics Engine JSON from stdin
/// and produces a DecisionResult JSON.
fn run() -> Result<(), Box<dyn std::error::Error>> {
    let mut input = String::new();

    io::stdin().read_to_string(&mut input)?;

    if input.trim().is_empty() {
        return Err("input JSON cannot be empty".into());
    }

    let consumer = PhysicsConsumer::new();

    let decision_result = consumer.evaluate_json(&input)?;

    let output = serde_json::to_string_pretty(&decision_result)?;

    println!("{}", output);

    Ok(())
}