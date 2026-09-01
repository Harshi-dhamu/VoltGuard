use decision_engine::adapter::DecisionEventAdapter;
use decision_engine::models::Decision;
use decision_engine::physics_consumer::PhysicsConsumer;

fn normal_physics() -> &'static str {
    r#"
    {
      "flow": {
        "pump_speed_rpm": 2500.0,
        "valve_position_percent": 50.0,
        "pump_flow_lpm": 50.0,
        "actual_flow_lpm": 25.0
      },
      "tank": {
        "final_level_liters": 5250.0,
        "final_fill_percentage": 52.5
      },
      "safety": {
        "overall_status": "NORMAL",
        "checks": {
          "pump": {"status": "NORMAL"},
          "pipe_pressure": {"status": "NORMAL"},
          "tank": {"status": "NORMAL"}
        }
      },
      "telemetry": {
        "system_status": "NORMAL",
        "assets": {
          "PUMP_01": {
            "asset_type": "PUMP",
            "health_status": "NORMAL"
          }
        }
      },
      "health_summary": {
        "system_status": "NORMAL",
        "total_assets": 1,
        "normal_assets": 1,
        "warning_assets": 0,
        "critical_assets": 0
      }
    }
    "#
}

fn physics_with_status(status: &str) -> String {
    normal_physics().replace(
        "\"NORMAL\"",
        &format!("\"{}\"", status)
    )
}

#[test]
fn normal_pump_command_should_allow() {
    let consumer = PhysicsConsumer::new();

    let result = consumer
        .evaluate_json(normal_physics())
        .expect("normal command should be valid");

    assert_eq!(result.decision, Decision::Allow);

    let event = DecisionEventAdapter::create_event(
        &result,
        "ATTACK-0001",
        Some("PKT-NORMAL-001".to_string()),
    );

    assert_eq!(event.payload.decision, "ALLOW");
    assert_eq!(event.severity, "LOW");
}

#[test]
fn high_pressure_scenario_should_block() {
    let consumer = PhysicsConsumer::new();

    let input = physics_with_status("CRITICAL");

    let result = consumer
        .evaluate_json(&input)
        .expect("critical physics result should be valid");

    assert_eq!(result.decision, Decision::Drop);

    let event = DecisionEventAdapter::create_event(
        &result,
        "ATTACK-0002",
        Some("PKT-HIGH-PRESSURE-001".to_string()),
    );

    assert_eq!(event.payload.decision, "BLOCK");
    assert_eq!(event.severity, "HIGH");
}

#[test]
fn extreme_flow_scenario_should_block() {
    let consumer = PhysicsConsumer::new();

    let input = physics_with_status("CRITICAL");

    let result = consumer
        .evaluate_json(&input)
        .expect("extreme flow result should be valid");

    assert_eq!(result.decision, Decision::Drop);

    let event = DecisionEventAdapter::create_event(
        &result,
        "ATTACK-0003",
        Some("PKT-EXTREME-FLOW-001".to_string()),
    );

    assert_eq!(event.payload.decision, "BLOCK");
    assert_eq!(event.severity, "HIGH");
}

#[test]
fn invalid_command_should_block() {
    let consumer = PhysicsConsumer::new();

    let result = consumer.evaluate_json(
        "{ invalid command"
    );

    assert!(result.is_err());
}