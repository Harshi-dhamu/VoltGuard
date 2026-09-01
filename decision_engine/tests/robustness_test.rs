use decision_engine::adapter::DecisionEventAdapter;
use decision_engine::models::{
    Decision,
    DecisionReason,
    DecisionResult,
};
use decision_engine::physics_consumer::PhysicsConsumer;

fn normal_output() -> &'static str {
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
          "pump": {
            "status": "NORMAL"
          }
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

#[test]
fn empty_physics_output_should_fail_closed() {
    let consumer = PhysicsConsumer::new();

    let result = consumer.evaluate_json("");

    assert!(result.is_err());
}

#[test]
fn malformed_json_should_fail_closed() {
    let consumer = PhysicsConsumer::new();

    let result = consumer.evaluate_json("{ invalid json }");

    assert!(result.is_err());
}

#[test]
fn unknown_status_should_fail_closed() {
    let consumer = PhysicsConsumer::new();

    let input = normal_output().replace(
        "\"NORMAL\"",
        "\"UNKNOWN_STATUS\"",
    );

    let result = consumer
        .evaluate_json(&input)
        .expect("unknown status should still produce a fail-closed decision");

    assert_eq!(result.decision, Decision::Drop);
    assert_eq!(
        result.reason,
        DecisionReason::UnknownPhysicsStatus
    );
}

#[test]
fn non_finite_value_should_fail_closed() {
    let consumer = PhysicsConsumer::new();

    let input = normal_output().replace(
        "\"pump_speed_rpm\": 2500.0",
        "\"pump_speed_rpm\": 1e999",
    );

    let result = consumer.evaluate_json(&input);

    assert!(result.is_err());
}

#[test]
fn single_asset_should_be_used_as_decision_asset() {
    let consumer = PhysicsConsumer::new();

    let result = consumer
        .evaluate_json(normal_output())
        .expect("normal physics output should be valid");

    assert_eq!(result.device_id, "PUMP_01");
    assert_eq!(result.decision, Decision::Allow);
}

#[test]
fn adapter_allow_should_have_low_severity() {
    let result = DecisionResult {
        device_id: "PUMP_01".to_string(),
        decision: Decision::Allow,
        reason: DecisionReason::PhysicsStatusSafe,
    };

    let event = DecisionEventAdapter::create_event(
        &result,
        "DEC-0014",
        None,
    );

    assert_eq!(event.severity, "LOW");
    assert_eq!(event.payload.decision, "ALLOW");
    assert_eq!(event.event_type, "SECURITY_DECISION");
}

#[test]
fn adapter_drop_should_have_high_severity() {
    let result = DecisionResult {
        device_id: "PUMP_01".to_string(),
        decision: Decision::Drop,
        reason: DecisionReason::PressureLimitExceeded,
    };

    let event = DecisionEventAdapter::create_event(
        &result,
        "DEC-0015",
        None,
    );

    assert_eq!(event.severity, "HIGH");
    assert_eq!(event.payload.decision, "BLOCK");
    assert_eq!(
        event.payload.reason,
        "PRESSURE_LIMIT_EXCEEDED"
    );
}