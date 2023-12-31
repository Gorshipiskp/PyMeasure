class Measurement:
    __slots__ = ('meass',)

    def __init__(self, **init_meass):
        self.meass = init_meass
        self.zerclean()

    def zerclean(self):
        for meas, val in self.meass.copy().items():
            if val == 0:
                self.meass.pop(meas)

    def __operate__(self, other: "Measurement", type_op: int) -> "Measurement":
        new_meass: dict[str, int] = self.meass.copy()

        for meas, val in other.meass.items():
            new_meass[meas] = new_meass.get(meas, 0) + val * type_op
        return Measurement(**new_meass)

    def __mul__(self, other: "Measurement") -> "Measurement":
        return self.__operate__(other, 1)

    def __truediv__(self, other: "Measurement") -> "Measurement":
        return self.__operate__(other, -1)

    def __pow__(self, power: int) -> "Measurement":
        new_meass = self.meass.copy()

        for key in self.meass.keys():
            new_meass[key] *= power
        return Measurement(**new_meass)

    def __eq__(self, other: "Measurement"):
        return self.meass == other.meass

    def __ne__(self, other: "Measurement"):
        return self.meass != other.meass

    def __latex__(self) -> str:
        srtd = sorted(self.meass.keys(), key=self.meass.get, reverse=True)
        return f"""{f' {chr(92)}cdot '.join(f'{el}{f"^{{{self.meass[el]}}}" if self.meass[el] != 1 else ""}' for el in srtd)}"""

    def __str__(self) -> str:
        srtd = sorted(self.meass.keys(), key=self.meass.get, reverse=True)
        return f"""{' * '.join(f'{el}{f"^{self.meass[el]}" if self.meass[el] != 1 else ""}' for el in srtd)}"""

    def __repr__(self) -> str:
        return f"M{self.meass}"


class MeasNum:
    __slots__ = ('meas', 'val')

    def __init__(self, val: int | float, **init_meass) -> None:
        self.meas = Measurement(**init_meass)
        self.val = val

    def __add__(self, other: "MeasNum") -> "MeasNum":
        assert other.meas == self.meas, ValueError("Addition error – The units of the operands do not match")
        return MeasNum(self.val + other.val, **self.meas.meass)

    def __sub__(self, other: "MeasNum") -> "MeasNum":
        assert other.meas == self.meas, ValueError("Error during subtraction – The units of measurement of the "
                                                   "operands do not match")
        return MeasNum(self.val - other.val, **self.meas.meass)

    def __mul__(self, other: "MeasNum") -> "MeasNum":
        return MeasNum(self.val * other.val, **(self.meas * other.meas).meass)

    def __truediv__(self, other: "MeasNum") -> "MeasNum":
        return MeasNum(self.val / other.val, **(self.meas / other.meas).meass)

    def __pow__(self, power: int) -> "MeasNum":
        return MeasNum(self.val ** power, **(self.meas ** power).meass)

    def __eq__(self, other: "MeasNum"):
        return self.meas == other.meas and self.val == other.val

    def __ne__(self, other: "MeasNum"):
        return self.meas != other.meas and self.val != other.val

    def __str__(self) -> str:
        return f"{self.val} {self.meas}"

    def __latex__(self) -> str:
        return f"{self.val} {self.meas.__latex__()}"
