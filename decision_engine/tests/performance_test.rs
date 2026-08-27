use decision_engine::decision::DecisionEngine;
use decision_engine::models::{
    PhysicsResult,
    PhysicsStatus,
};
use std::time::Instant;

fn safe_physics_result() -> PhysicsResult {
    PhysicsResult {
        device_id: "PUMP_01".to_string(),
        command: "SET_SPEED".to_string(),
        value: 1500.0,
        unit: "RPM".to_string(),

        predicted_pressure: Some(80.0),
        pressure_limit: Some(100.0),

        predicted_flow: Some(200.0),
        flow_limit: Some(300.0),

        pump_speed: Some(1500.0),
        pump_speed_limit: Some(3000.0),

        status: PhysicsStatus::Safe,
    }
}

#[test]
fn measure_decision_latency() {
    let engine = DecisionEngine::new();
    let physics_result = safe_physics_result();

    let iterations = 10_000;

    let start = Instant::now();

    for _ in 0..iterations {
        let result = engine.evaluate(&physics_result);

        assert!(result.is_ok());

        // Prevent the compiler from treating the result as unused.
        let _ = std::hint::black_box(result);
    }

    let elapsed = start.elapsed();

    let total_microseconds = elapsed.as_micros();
    let average_microseconds = total_microseconds as f64 / iterations as f64;
    let average_milliseconds = average_microseconds / 1000.0;

    println!(
        "\nDecision Engine performance:"
    );
    println!(
        "Iterations: {}",
        iterations
    );
    println!(
        "Total time: {:?}",
        elapsed
    );
    println!(
        "Average decision latency: {:.4} ms",
        average_milliseconds
    );

    assert!(
        average_milliseconds < 10.0,
        "Decision latency exceeded the 10 ms target"
    );
}