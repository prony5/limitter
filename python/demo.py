import limiter as lim
import generator as gen

import random
import numpy as np
import matplotlib.pyplot as plot

dt = 0.01
ampl = 50
freq = 0.1
ofs = 50

l = lim.Limiter(0, 100, 1000, 50, 100)
g = gen.SignalGeneratorMeander(ampl, freq, ofs)
#g = gen.SignalGeneratorWave(ampl, freq, ofs)
#g = gen.SignalGeneratorSaw(ampl, freq, ofs)

time = np.arange(-dt, 10, dt)
signal = [g.generate(t) + random.random() * 0 for t in time]
# result = [(l.solve(dt, x),l.est_vel,l.est_acc) for x in signal]
result = [(l.solve(dt, x)) for x in signal]

plot.plot(time, signal)
plot.plot(time, result[0:])
plot.xlabel("Time")
plot.grid(True, which="both")
plot.axhline(y=0, color="k")
plot.show()