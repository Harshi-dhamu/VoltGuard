from pump import Pump
from valve import Valve
from pipe import Pipe
from tank import Tank


pump = Pump()
pump.set_speed(2500)
print("Pump:", pump.get_state())

valve = Valve()
valve.set_position(50)
print("Valve:", valve.get_state())

pipe = Pipe()
print("Pipe:", pipe.get_state())

tank = Tank()
tank.set_level(5000)
print("Tank:", tank.get_state())