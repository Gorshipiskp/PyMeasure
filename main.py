from typing import Literal


class Measurement:
    __slots__: tuple[str] = ('meass',)

    def __init__(self, **init_meass) -> None:
        self.meass: dict[str, int] = {meas: val for meas, val in init_meass.items() if val != 0}

    def __operate__(self, other: "Measurement", type_op: Literal[1, -1]) -> "Measurement":
        new_meass: dict[str, int] = self.meass.copy()

        for meas, val in other.meass.items():
            new_meass[meas] = new_meass.get(meas, 0) + val * type_op
        return Measurement(**new_meass)

    def __mul__(self, other: "Measurement") -> "Measurement":
        return self.__operate__(other, 1)

    def __truediv__(self, other: "Measurement") -> "Measurement":
        return self.__operate__(other, -1)

    def __pow__(self, power: int) -> "Measurement":
        new_meass: dict[str, int] = {key: val * power for key, val in self.meass.items()}
        return Measurement(**new_meass)

    def __eq__(self, other: "Measurement") -> bool:
        return self.meass == other.meass

    def __ne__(self, other: "Measurement") -> bool:
        return self.meass != other.meass

    def __latex__(self) -> str:
        srtd_pos = (i for i in self.meass.keys() if self.meass[i] > 0)
        srtd_neg = sorted([i for i in self.meass.keys() if self.meass[i] < 0], key=self.meass.get, reverse=True)

        srtd_positives = f' {chr(92)}cdot '.join(f'{el}{f"^{{{self.meass[el]}}}" if self.meass[el] != 1 else ""}' for el in srtd_pos)
        srtd_negatives = f' {chr(92)}cdot '.join(f'{el}{f"^{{{-self.meass[el]}}}" if self.meass[el] != 1 else ""}' for el in srtd_neg)

        return f"{chr(92)}small{chr(92)}frac{{{srtd_positives}}}{{{srtd_negatives}}}"

    def __str__(self) -> str:
        srtd: list[str] = sorted(self.meass.keys(), key=self.meass.get, reverse=True)
        return ' * '.join(f'{el}{f"^{self.meass[el]}" if self.meass[el] != 1 else ""}' for el in srtd)

    def __repr__(self) -> str:
        return f"M{self.meass}"


class MeasNum:
    __slots__: tuple[str] = ('meas', 'val')

    def __init__(self, val: int | float, **init_meass) -> None:
        self.meas: Measurement = Measurement(**init_meass)
        self.val: int | float = val

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

    def __eq__(self, other: "MeasNum") -> bool:
        return self.meas == other.meas and self.val == other.val

    def __ne__(self, other: "MeasNum") -> bool:
        return self.meas != other.meas and self.val != other.val

    def __str__(self) -> str:
        return f"{self.val} {self.meas}"

    def __latex__(self) -> str:
        return f"{self.val} {self.meas.__latex__()}"
