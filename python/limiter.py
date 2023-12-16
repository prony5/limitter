class Limiter(object):
    est_value = 0.0
    est_vel = 0.0
    est_acc = 0.0

    __ready = True
    __last_value = 0.0

    def __init__(self, low=-1.0, high=1.0, vel=1.0, acc=0.1, dcc=0.1) -> None:
        self.lim_min = low
        self.lim_max = high
        self.lim_vel = vel
        self.lim_acc = acc
        self.lim_dcc = dcc

    def solve(self, dt, value):
        ddt = 1 / max(self.lim_acc, self.lim_dcc)
        steps = int(dt/ddt)

        for i in range(max(1, steps)):
            dt = ddt if steps > 0 else dt
            value = self.lim_min if value < self.lim_min else value
            value = self.lim_max if value > self.lim_max else value

            if self.__ready and self.__last_value == value:
                return value

            self.__ready = False
            self.__last_value = value

            lim_acc = self.lim_acc if self.est_vel >=0 else self.lim_dcc

            # ускорение в сторону задания в зависимости от того по какую сторону от задания мы находимся
            self.est_acc = lim_acc if value > self.est_value else -lim_acc

            dist = abs(value - self.est_value)
            # прогнозируем когда будем торомозить на максимальном ускорении, только в том случае, если мы приближаемся к заданию а не отдаляемся
            if (dist < self.est_vel * self.est_vel / 2.0 / lim_acc + abs(self.est_vel) * dt) and (dist - abs(value - self.est_valueLast) < 0):
                self.est_acc = -self.est_acc

            self.est_vel += self.est_acc * dt
            if self.est_vel > self.lim_vel:
                self.est_vel = self.lim_vel
            if self.est_vel < -self.lim_vel:
                self.est_vel = -self.lim_vel

            self.est_valueLast = self.est_value
            self.est_value += self.est_vel * dt + self.est_acc * dt * dt / 2.0

            # если пересекли задание и скорость упала до околонулевой, то точка достигнута
            valueComplete = ((self.est_value - value) > 0.0 and (self.est_valueLast - value) <
                             0.0) or ((self.est_value - value) < 0.0 and (self.est_valueLast - value) > 0.0)
            if valueComplete and (abs(self.est_vel) < (lim_acc * dt * 2)):
                self.__ready = True
                self.est_value = value
                self.est_vel = 0
                self.est_acc = 0

        self.est_value = self.lim_min if self.est_value < self.lim_min else self.est_value
        self.est_value = self.lim_max if self.est_value > self.lim_max else self.est_value
        return self.est_value
