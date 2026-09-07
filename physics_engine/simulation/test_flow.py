from flow_calculator import FlowCalculator


calculator = FlowCalculator(max_flow_lpm=100.0)

# Test 1: Pump at 2500 RPM, valve 50% open
state = calculator.get_flow_state(
    pump_speed_rpm=2500,
    valve_position_percent=50,
)

print("Flow State:")
print(state)

# Test 2: Pump at maximum speed, valve fully open
state = calculator.get_flow_state(
    pump_speed_rpm=5000,
    valve_position_percent=100,
)

print("\nMaximum Flow State:")
print(state)