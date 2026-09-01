use decision_engine::decision::DecisionEngine;
use decision_engine::models::{
    Decision,
    PhysicsResult,
    PhysicsStatus,
};
use std::time::Instant;

fn safe_result() -> PhysicsResult {
    PhysicsResult {
        device_id: "PUMP_01".to_string(),
        command: "SET_SPEED".to_string(),

        // Original command fields
        value: 1500.0,
        unit: "RPM".to_string(),

        // Current physical values
        pressure: Some(80.0),
        flow: Some(200.0),
        pump_speed: Some(1500.0),

        // Predicted values and limits
        predicted_pressure: Some(80.0),
        pressure_limit: Some(100.0),

        predicted_flow: Some(200.0),
        flow_limit: Some(300.0),

        pump_speed_limit: Some(3000.0),

        status: PhysicsStatus::Safe,
    }
}

#[test]
fn decision_engine_performance_test() {
    let engine = DecisionEngine::new();
    let physics = safe_result();

    let iterations = 10_000;

    let start = Instant::now();

    for _ in 0..iterations {
        let result = engine
            .evaluate(&physics)
            .expect("evaluation should succeed");

        assert_eq!(result.decision, Decision::Allow);
    }

    let elapsed = start.elapsed();

    println!(
        "Processed {} decisions in {:?}",
        iterations,
        elapsed
    );

    println!(
        "Average time per decision: {:?}",
        elapsed / iterations
    );
}