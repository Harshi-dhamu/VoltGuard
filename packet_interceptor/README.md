# VoltGuard — Packet Interceptor Module

## Overview
The **Packet Interceptor** acts as the primary defense and intake engine for the VoltGuard industrial control system (ICS) security platform. It parses incoming Modbus TCP traffic, validates protocol integrity, normalizes commands into structured JSON models, pre-flags suspicious physical parameters, and forwards normalized payloads to the Physics Engine.

---

## Key Features
* **Modbus TCP Binary Parser:** Extracts MBAP headers, Unit IDs, Function Codes, Registers, and Payload Values.
* **Deep Validation Engine:** Enforces protocol compliance, valid function codes (`0x03`, `0x06`, `0x10`), and operational register boundaries (`1000–1999`).
* **Command Normalizer:** Maps raw register values to human-readable physical units (`RPM`, `%`, `PSI`).
* **Suspicious Parameter Pre-Flagging:** Flags physical anomalies exceeding safety operational thresholds.
* **Physics Engine Decoupled Interface:** Dispatches clean JSON payloads to downstream engines via clean interface callbacks.
* **Structured Logging:** Auto-logs pipeline activities to console output and `logs/interceptor.log`.

---

## Project Structure
```text
packet_interceptor/
├── logs/
│   └── interceptor.log
├── models/
│   └── modbus_packet.py
├── scripts/
│   ├── benchmark.py
│   └── mock_generator.py
├── src/
│   ├── logger.py
│   ├── main.py
│   ├── normalizer.py
│   ├── parser.py
│   ├── physics_interface.py
│   ├── suspicious_detector.py
│   └── validator.py
├── tests/
│   ├── test_attack_scenarios.py
│   ├── test_interceptor.py
│   └── test_physics_integration.py
└── README.md