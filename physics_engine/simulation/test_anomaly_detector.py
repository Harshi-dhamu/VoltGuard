import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from physics_engine.simulation.anomaly_detector import AnomalyDetector


def main():
    detector = AnomalyDetector()

    print("=== VoltGuard Anomaly Detector Test ===")

    # =========================================================
    # TEST 1: NORMAL CONDITION
    # =========================================================

    normal_result = detector.detect(
        flow_data={
            "pump_speed_rpm": 2500,
            "pump_flow_lpm": 50.0,
            "actual_flow_lpm": 25.0,
        },
        tank_data={
            "final_level_liters": 5250.0,
        },
        safety_data={
            "checks": {
                "pipe_pressure": {
                    "status": "NORMAL",
                }
            }
        },
    )

    print("\n--- TEST 1: NORMAL CONDITION ---")
    print(normal_result)

    assert normal_result["anomaly_detected"] is False
    assert normal_result["anomaly_count"] == 0
    assert normal_result["anomaly_score"] == 0.0
    assert normal_result["severity"] == "LOW"

    print("PASS")


    # =========================================================
    # TEST 2: LOW FLOW ANOMALY
    # =========================================================

    low_flow_result = detector.detect(
        flow_data={
            "pump_speed_rpm": 3000,
            "pump_flow_lpm": 60.0,
            "actual_flow_lpm": 10.0,
        },
        tank_data={
            "final_level_liters": 5250.0,
        },
        safety_data={
            "checks": {
                "pipe_pressure": {
                    "status": "NORMAL",
                }
            }
        },
    )

    print("\n--- TEST 2: LOW FLOW ANOMALY ---")
    print(low_flow_result)

    assert low_flow_result["anomaly_detected"] is True
    assert low_flow_result["anomaly_count"] == 1
    assert low_flow_result["anomalies"][0]["type"] == "FLOW_ANOMALY"
    assert low_flow_result["anomaly_score"] == 0.82
    assert low_flow_result["severity"] == "CRITICAL"

    print("PASS")


    # =========================================================
    # TEST 3: HIGH PUMP SPEED
    # =========================================================

    pump_speed_result = detector.detect(
        flow_data={
            "pump_speed_rpm": 5500,
            "pump_flow_lpm": 100.0,
            "actual_flow_lpm": 50.0,
        },
        tank_data={
            "final_level_liters": 5000.0,
        },
        safety_data={
            "checks": {
                "pipe_pressure": {
                    "status": "NORMAL",
                }
            }
        },
    )

    print("\n--- TEST 3: HIGH PUMP SPEED ANOMALY ---")
    print(pump_speed_result)

    assert pump_speed_result["anomaly_detected"] is True
    assert pump_speed_result["anomaly_count"] == 1
    assert pump_speed_result["anomalies"][0]["type"] == "PUMP_SPEED_ANOMALY"
    assert pump_speed_result["anomaly_score"] == 0.95
    assert pump_speed_result["severity"] == "CRITICAL"

    print("PASS")


    # =========================================================
    # TEST 4: CRITICAL PIPE PRESSURE
    # =========================================================

    pressure_result = detector.detect(
        flow_data={
            "pump_speed_rpm": 4000,
            "pump_flow_lpm": 80.0,
            "actual_flow_lpm": 40.0,
        },
        tank_data={
            "final_level_liters": 5400.0,
        },
        safety_data={
            "checks": {
                "pipe_pressure": {
                    "status": "CRITICAL",
                    "message": "Pipe pressure exceeds the safe limit.",
                }
            }
        },
    )

    print("\n--- TEST 4: CRITICAL PRESSURE ANOMALY ---")
    print(pressure_result)

    assert pressure_result["anomaly_detected"] is True
    assert pressure_result["anomaly_count"] == 1
    assert pressure_result["anomalies"][0]["type"] == "PRESSURE_ANOMALY"
    assert pressure_result["anomaly_score"] == 0.94
    assert pressure_result["severity"] == "CRITICAL"

    print("PASS")


    # =========================================================
    # FINAL RESULT
    # =========================================================

    print("\n==============================================")
    print("=== ALL ANOMALY DETECTOR TESTS PASSED ===")
    print("==============================================")


if __name__ == "__main__":
    main()