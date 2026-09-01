use decision_engine::adapter::DecisionEventAdapter;
use decision_engine::physics_consumer::PhysicsConsumer;

fn normal_physics_json() -> &'static str {
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
          },
          "pipe_pressure": {
            "status": "NORMAL"
          },
          "tank": {
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
          },
          "VALVE_01": {
            "asset_type": "VALVE",
            "health_status": "NORMAL"
          },
          "PIPE_01": {
            "asset_type": "PIPE",
            "health_status": "NORMAL"
          },
          "TANK_01": {
            "asset_type": "TANK",
            "health_status": "NORMAL"
          }
        }
      },
      "health_summary": {
        "system_status": "NORMAL",
        "total_assets": 4,
        "normal_assets": 4,
        "warning_assets": 0,
        "critical_assets": 0
      }
    }
    "#
}

fn critical_physics_json() -> String {
    normal_physics_json().replace(
        "\"overall_status\": \"NORMAL\"",
        "\"overall_status\": \"CRITICAL\"",
    )
}

fn invalid_physics_json() -> &'static str {
    r#"{ invalid json }"#
}

#[test]
fn safe_physics_to_allow_event() {
    let consumer = PhysicsConsumer::new();

    let decision = consumer
        .evaluate_json(normal_physics_json())
        .expect("normal physics result should be valid");

    assert_eq!(decision.decision.to_string(), "ALLOW");

    let event = DecisionEventAdapter::create_event(
        &decision,
        "DEC-E2E-001",
        Some("PKT-0001".to_string()),
    );

    assert_eq!(event.source_module, "decision_engine");
    assert_eq!(event.event_type, "SECURITY_DECISION");
    assert_eq!(event.payload.decision, "ALLOW");
    assert_eq!(event.asset, "SYSTEM");
}

#[test]
fn critical_physics_to_block_event() {
    let consumer = PhysicsConsumer::new();

    let physics = critical_physics_json();

    let decision = consumer
        .evaluate_json(&physics)
        .expect("critical physics result should be valid");

    assert_eq!(decision.decision.to_string(), "DROP");

    let event = DecisionEventAdapter::create_event(
        &decision,
        "DEC-E2E-002",
        Some("PKT-0002".to_string()),
    );

    assert_eq!(event.source_module, "decision_engine");
    assert_eq!(event.event_type, "SECURITY_DECISION");
    assert_eq!(event.payload.decision, "BLOCK");
    assert_eq!(event.severity, "HIGH");
}

#[test]
fn invalid_physics_fails_closed() {
    let consumer = PhysicsConsumer::new();

    let result = consumer.evaluate_json(invalid_physics_json());

    assert!(result.is_err());
}

#[test]
fn warning_physics_to_block_event() {
    let consumer = PhysicsConsumer::new();

    let physics = normal_physics_json()
        .replace(
            "\"overall_status\": \"NORMAL\"",
            "\"overall_status\": \"WARNING\"",
        );

    let decision = consumer
        .evaluate_json(&physics)
        .expect("warning physics result should be valid");

    assert_eq!(decision.decision.to_string(), "DROP");

    let event = DecisionEventAdapter::create_event(
        &decision,
        "DEC-E2E-003",
        Some("PKT-0003".to_string()),
    );

    assert_eq!(event.payload.decision, "BLOCK");
    assert_eq!(event.event_type, "SECURITY_DECISION");
}