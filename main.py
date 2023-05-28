import random


class Car:
    def __init__(self, offset):
        self.time_offset = offset


class TrafficSimulation:
    def __init__(self, n=0, m=0, fd_arrival_time=12, sd_arrival_time=5, passing_cars_cooldown=2, red_light_time=55):
        self.n = n  # Продолжительность зелёного сигнала на первом направлении
        self.m = m  # Продолжительность зелёного сигнала на втором направлении
        self.elapsed_time = 0  # Прошедшее время симуляции

        self.first_direction_queue = []  # Очередь для хранения прибывающих автомобилей
        self.second_direction_queue = []  # Очередь для хранения прибывающих автомобилей

        self.first_direction_traffic_light = 0  # Сигнал светофора на первом направлении (0 - красный, 1 - зелёный)
        self.second_direction_traffic_light = 0  # Сигнал светофора на втором направлении (0 - красный, 1 - зелёный)

        self.first_direction_arrival_time = fd_arrival_time  # Скорость прибытия машин на первом направлении
        self.second_direction_arrival_time = sd_arrival_time  # Скорость прибытия машин на втором направлении

        self.cars_cooldown = passing_cars_cooldown  # Задержка проезда машин на зелёный сигнал светофора
        self.red_light_time = red_light_time  # Сколько времени красный сигнал горел на оба направления

        self.total_waiting_time = 0  # Суммарное время ожидания
        self.car_count = 0  # Количество проехавших машин

    # Создаёт на каждую вторую секунду симуляции по машине в каждую очередь
    def generate_car_arrivals(self, simulation_duration):
        first_direction_arrival = second_direction_arrival = 0

        while not len(self.first_direction_queue) or self.first_direction_queue[-1].time_offset <= simulation_duration \
                or self.second_direction_queue[-1].time_offset <= simulation_duration:

            self.first_direction_queue.append(Car(
                first_direction_arrival := (first_direction_arrival + random.expovariate(1 / 12))))
            self.second_direction_queue.append(Car(
                second_direction_arrival := (second_direction_arrival + random.expovariate(1 / 5))))

    def simulate(self, simulation_duration):
        self.generate_car_arrivals(simulation_duration)

        while self.elapsed_time < simulation_duration:
            # Если горит зелёный сигнал на первом направлении
            if self.cars_cooldown <= self.elapsed_time % (self.n + self.m + self.red_light_time) < self.n:
                self.process_car(self.first_direction_queue)
                self.elapsed_time += self.cars_cooldown
            # Если горит зелёный сигнал на втором направлении
            elif self.elapsed_time % (self.n + self.m + self.red_light_time) >= \
                    self.n + self.red_light_time + self.cars_cooldown-1:
                self.process_car(self.second_direction_queue)
                self.elapsed_time += self.cars_cooldown
            else:
                self.elapsed_time += 1

        # После того как закончилось время симуляции, добавляем время ожидания тех машин, что так и не проехали
        self.add_all_cars_waiting_time()

    def process_car(self, direction):
        if direction[0].time_offset <= self.elapsed_time:
            self.total_waiting_time += (self.elapsed_time - direction[0].time_offset)
            self.car_count += 1
            direction.pop(0)

    def add_all_cars_waiting_time(self):
        for i in self.first_direction_queue:
            if i.time_offset <= self.elapsed_time:
                self.total_waiting_time += (self.elapsed_time - i.time_offset)
                self.car_count += 1
            else:
                break
        for i in self.second_direction_queue:
            if i.time_offset <= self.elapsed_time:
                self.total_waiting_time += (self.elapsed_time - i.time_offset)
                self.car_count += 1
            else:
                break

    def get_average_waiting_time(self):
        return self.total_waiting_time / self.car_count if self.car_count != 0 else float('inf')


# Test simulation with different values of n and m

optimal_n = 0
optimal_m = 0
min_avg_waiting_time = float('inf')
wait_time = []

for n in range(100):
    simulation = TrafficSimulation(46, 106)
    simulation.simulate(40_000)
    wait_time.append(simulation.get_average_waiting_time())

mean = sum(wait_time) / len(wait_time)

a = 0
for i in wait_time:
    a += (i - mean)**2

dispersion = a/100
print(dispersion, mean)

# for n in range(45, 46):
#     for m in range(103, 107):
#         simulation = TrafficSimulation(n, m)
#         simulation.simulate(1_000_000)
#         if simulation.get_average_waiting_time() < min_avg_waiting_time:
#             min_avg_waiting_time = simulation.get_average_waiting_time()
#             optimal_n = n
#             optimal_m = m

print("Optimal n:", optimal_n)
print("Optimal m:", optimal_m)
print("Minimum average waiting time:", min_avg_waiting_time)
