# VoltGuard Dashboard

The VoltGuard Dashboard is the operator-facing security monitoring interface for the VoltGuard OT/ICS security platform.

## Responsibilities

The dashboard will eventually provide:

- Security overview
- Network traffic monitoring
- Industrial asset visibility
- Security alert management
- Decision engine results
- Event logs
- System health
- Integrated security analytics

## Architecture

The dashboard is designed to remain independent from individual security engines.

Current Day 1 architecture:

Mock Data Provider
        ↓
Dashboard Widgets
        ↓
Main Dashboard

Target architecture:

Packet Interceptor
        ↓
Shared Data Contracts
        ↓
Physics Engine
        ↓
Decision Engine
        ↓
Integration Layer
        ↓
Dashboard

## Technology

- Python
- PyQt6

## Development Principle

UI components should remain reusable and independent from backend implementation details.