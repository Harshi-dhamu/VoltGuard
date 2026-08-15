mod decision;
mod error;
mod models;

use decision::DecisionEngine;
use models::PhysicsResult;
use std::io::{self, Read};

fn main() {
    let mut input = String::new();

    if let Err(error) = io::stdin().read_to_string(&mut input) {
        eprintln!("Failed to read input: {error}");
        std::process::exit(1);
    }

    if input.trim().is_empty() {
        eprintln!("No JSON input received.");
        std::process::exit(1);
    }

    let physics_result: PhysicsResult = match serde_json::from_str(&input) {
        Ok(result) => result,
        Err(error) => {
            eprintln!("Invalid JSON input: {error}");
            std::process::exit(1);
        }
    };

    let engine = DecisionEngine::new();

    match engine.evaluate(&physics_result) {
        Ok(decision) => {
            match serde_json::to_string_pretty(&decision) {
                Ok(json) => println!("{json}"),
                Err(error) => {
                    eprintln!("Failed to serialize decision: {error}");
                    std::process::exit(1);
                }
            }
        }

        Err(error) => {
            eprintln!("Decision Engine error: {error}");
            std::process::exit(1);
        }
    }
}