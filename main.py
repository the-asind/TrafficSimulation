import random
import matplotlib.pyplot as plt


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

        self.total_f = self.total_s = 0
        self.cars_f = self.cars_s = 0

        self.waiting_time_update_fd = []
        self.waiting_time_update_sd = []
        self.waiting_time_update = []

    # Создаёт на каждую вторую секунду симуляции по машине в каждую очередь
    def generate_car_arrivals(self, simulation_duration):
        first_direction_arrival = second_direction_arrival = 0

        while not len(self.first_direction_queue) or self.first_direction_queue[-1] <= simulation_duration \
                or self.second_direction_queue[-1] <= simulation_duration:
            self.first_direction_queue.append(
                first_direction_arrival := (first_direction_arrival + random.expovariate(1 / self.first_direction_arrival_time)))
            self.second_direction_queue.append(
                second_direction_arrival := (second_direction_arrival + random.expovariate(1 / self.second_direction_arrival_time)))

        print(self.n, self.m, len(self.first_direction_queue), len(self.second_direction_queue), "cars count generated")
        # self.generate_graph_of_cars_arriving()

    def generate_graph_of_cars_arriving(self):
        # Генерация значений оси x с использованием индексов массивов
        x = range(len(self.first_direction_queue))

        # Создание графика и добавление первого массива
        plt.plot(x, self.first_direction_queue, label='Время прибытия машин по первому направлению')

        # Добавление второго массива на график
        plt.plot(x, self.second_direction_queue, label='Время прибытия машин по второму направлению')

        # Добавление легенды
        plt.legend()

        # Добавление подписей осей
        plt.xlabel('Порядковый номер машины')
        plt.ylabel('Время прибытия от начала симуляции')

        # Отображение графика
        plt.show()

    def generate_graph_of_summary_waiting_time(self):
        # Генерация значений оси x с использованием индексов массивов
        x = range(len(self.waiting_time_update_fd))

        # Создание графика и добавление первого массива
        plt.plot(x, self.waiting_time_update_fd, label='Среднее время ожидания машин по первому направлению')

        # Добавление второго массива на график
        plt.plot(x, self.waiting_time_update_sd, label='Среднее время ожидания машин по второму направлению')

        # Добавление третьего массива на график
        plt.plot(x, self.waiting_time_update, label='Общее среднее время ожидания машин')

        # Добавление легенды
        plt.legend()

        # Добавление подписей осей
        plt.xlabel('Время с начала симуляции (сек)')
        plt.ylabel('Время ожидания (сек)')

        # Отображение графика
        plt.show()

    def simulate_q_schemes(self, simulation_duration):
        fd_queue_time_arrival = 0
        fd_delay = self.cars_cooldown
        fd_sum_waiting_time = 0
        fd_cars = 0
        fd_prev_green = 0

        sd_queue_time_arrival = 0
        sd_delay = self.cars_cooldown
        sd_sum_waiting_time = 0
        sd_cars = 0
        sd_prev_green = 0

        while True:
            fd_cars += 1
            fd_queue_time_arrival += random.expovariate(1 / self.first_direction_arrival_time)

            (isGreenNow, timeOfGreenStart) = find_nearest_green_light(fd_queue_time_arrival, 1)

            # Если светофор изменился, то обнуляем задержку
            if fd_prev_green != timeOfGreenStart:
                fd_delay = self.cars_cooldown

            if isGreenNow:
                # Если машина на зелёном и перед ней никого нет
                if timeOfGreenStart+fd_delay <= fd_queue_time_arrival:
                    fd_delay = fd_queue_time_arrival - timeOfGreenStart + self.cars_cooldown
                else:
                    pass  # TODO:

    def simulate_delta_t(self, simulation_duration):
        self.generate_car_arrivals(simulation_duration)
        cycle_duration = self.n + self.m + self.red_light_time * 2

        while self.elapsed_time < simulation_duration:
            # Если горит зелёный сигнал на первом направлении
            if self.elapsed_time % cycle_duration < self.n:
                self.process_car(self.first_direction_queue)
                self.elapsed_time += self.cars_cooldown

            # Если горит зелёный сигнал на втором направлении
            elif self.n + self.red_light_time < self.elapsed_time % cycle_duration < self.n + self.red_light_time + self.m:
                self.process_car(self.second_direction_queue)
                self.elapsed_time += self.cars_cooldown

            else:
                self.elapsed_time += self.cars_cooldown

            # self.waiting_time_update_fd.append((self.total_f / self.cars_f) if self.cars_f != 0 else 0)
            # self.waiting_time_update_sd.append((self.total_s / self.cars_s) if self.cars_s != 0 else 0)
            # self.waiting_time_update.append((self.total_waiting_time / self.car_count) if self.car_count != 0 else 0)

        # После того как закончилось время симуляции, добавляем время ожидания тех машин, что так и не проехали
        self.add_all_cars_waiting_time()

    def process_car(self, direction):
        if direction[0] <= self.elapsed_time:
            self.total_waiting_time += (self.elapsed_time - direction[0])
            self.car_count += 1

            if direction == self.first_direction_queue:
                self.total_f += (self.elapsed_time - direction[0])
                self.cars_f += 1

            else:
                self.total_s += (self.elapsed_time - direction[0])
                self.cars_s += 1

            direction.pop(0)

    def add_all_cars_waiting_time(self):
        # self.generate_graph_of_summary_waiting_time()
        for i in self.first_direction_queue:
            if i <= self.elapsed_time:
                self.total_waiting_time += (self.elapsed_time - i)
                self.car_count += 1
            else:
                break
        for i in self.second_direction_queue:
            if i <= self.elapsed_time:
                self.total_waiting_time += (self.elapsed_time - i)
                self.car_count += 1
            else:
                break

    def get_average_waiting_time(self):
        print("первое напр: машины сум./вр. ож. сум./ср.вр.ож", self.cars_f, self.total_f, self.total_f / self.cars_f)
        print("второе напр: машины сум./вр. ож. сум./ср.вр.ож", self.cars_s, self.total_s, self.total_s / self.cars_s)

        return self.total_waiting_time / self.car_count if self.car_count != 0 else float('inf')

    def get_all_these_things(self):
        return self.cars_f, self.total_f / self.cars_f, self.cars_s, self.total_s / self.cars_s


# Test simulation with different values of n and m

optimal_n = 0
optimal_m = 0
min_avg_waiting_time = float('inf')
wait_time = []
#
# for n in range(100):
#     simulation = TrafficSimulation(46, 106)
#     simulation.simulate(40_000)
#     wait_time.append(simulation.get_average_waiting_time())
#
# mean = sum(wait_time) / len(wait_time)
#
# a = 0
# for i in wait_time:
#     a += (i - mean)**2
#
# dispersion = a/100
# print(dispersion, mean)

# simulation = TrafficSimulation(47, 116)
# simulation.simulate_delta_t(1_000)
# print(simulation.get_average_waiting_time())

cars_f = wait_f = cars_s = wait_s = wait = cnt = 0
for n in range(53, 56):
    for m in range(144, 148):
        simulation = TrafficSimulation(n, m)
        simulation.simulate_delta_t(1_000)
        cars_f_temp, wait_f_temp, cars_s_temp, wait_s_temp = simulation.get_all_these_things()
        cars_f += cars_f_temp
        wait_f += wait_f_temp
        cars_s += cars_s_temp
        wait_s += wait_s_temp
        cnt += 1

        if simulation.get_average_waiting_time() < min_avg_waiting_time:
            min_avg_waiting_time = simulation.get_average_waiting_time()
            optimal_n = n
            optimal_m = m

print("Optimal n:", optimal_n)
print("Optimal m:", optimal_m)
print("Minimum average waiting time:", min_avg_waiting_time)
print("cars_f", cars_f/cnt, "wait_f", wait_f/cnt, "cars_s", cars_s/cnt, "wait_s", wait_s/cnt)
