from main import MeasNum


def pressure_calc(force: MeasNum, square: MeasNum) -> MeasNum:
    return force / square


force = MeasNum(500, N=1)
square = MeasNum(20, m=2)

pressure = pressure_calc(force, square)

print(pressure)                   # 25.0 N * m^-2
print(pressure.__latex__())       # 25.0 N \cdot m^{-2}
print(pressure.meas)              # N * m^-2
print(pressure.meas.__latex__())  # N \cdot m^{-2}
