import math
from abc import abstractclassmethod


class SignalGenerator(object):
    def __init__(self, ampl=1.0, freq=1.0, offs=0.0) -> None:
        self.amplitude = ampl
        self.frequency = freq
        self.offset = offs

    @abstractclassmethod
    def _solve(self, dt):
        pass

    def generate(self, time):
        return self.amplitude * self._solve(time * self.frequency) + self.offset


class SignalGeneratorMeander(SignalGenerator):
    def _solve(self, t):
        retValue = math.sin(2.0 * math.pi * t)
        if retValue != 0:
            retValue = (1.0 / retValue) * abs(retValue)
        return retValue


class SignalGeneratorWave(SignalGenerator):
    def _solve(self, t):
        return math.sin(2.0 * math.pi * t)


class SignalGeneratorSaw(SignalGenerator):
    def _solve(self, t):
        return (math.pi * 0.2) * math.asin(math.sin(2.0 * math.pi * t))