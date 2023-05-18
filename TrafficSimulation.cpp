#include <iostream>
#include <vector>
#include <cmath>
#include <random>

class Car {
public:
    Car(int offset) : time_offset(offset) {}

    int time_offset;
};

class TrafficSimulation {
public:
    TrafficSimulation(int n = 0, int m = 0, int fd_arrival_time = 12, int sd_arrival_time = 5,
                      int passing_cars_cooldown = 2, int red_light_time = 55)
        : n(n), m(m), elapsed_time(0), first_direction_arrival_time(fd_arrival_time),
          second_direction_arrival_time(sd_arrival_time), cars_cooldown(passing_cars_cooldown),
          red_light_time(red_light_time), total_waiting_time(0), car_count(0) {}

    void generate_car_arrivals(int simulation_duration) {
        int first_direction_arrival = 0;
        int second_direction_arrival = 0;

        for (int i = 0; i < simulation_duration / 3; ++i) {
            first_direction_queue.push_back(Car(first_direction_arrival +=
                                                 random_expovariate(1.0 / 12)));
            second_direction_queue.push_back(Car(second_direction_arrival +=
                                                  random_expovariate(1.0 / 5)));
        }
    }

    void simulate(int simulation_duration) {
        generate_car_arrivals(simulation_duration);

        while (elapsed_time < simulation_duration) {
            if (cars_cooldown <= elapsed_time % (n + m + red_light_time) && elapsed_time % (n + m + red_light_time) < n) {
                process_car(first_direction_queue);
                elapsed_time += cars_cooldown;
            }
            else if (elapsed_time % (n + m + red_light_time) >= n + red_light_time + cars_cooldown - 1) {
                process_car(second_direction_queue);
                elapsed_time += cars_cooldown;
            }
            else {
                elapsed_time++;
            }
        }

        add_all_cars_waiting_time();
    }

    void process_car(std::vector<Car>& direction) {
        if (direction[0].time_offset <= elapsed_time) {
            total_waiting_time += (elapsed_time - direction[0].time_offset);
            car_count++;
            direction.erase(direction.begin());
        }
    }

    void add_all_cars_waiting_time() {
        for (const auto& car : first_direction_queue) {
            if (car.time_offset <= elapsed_time) {
                total_waiting_time += (elapsed_time - car.time_offset);
                car_count++;
            }
            else {
                break;
            }
        }
        for (const auto& car : second_direction_queue) {
            if (car.time_offset <= elapsed_time) {
                total_waiting_time += (elapsed_time - car.time_offset);
                car_count++;
            }
            else {
                break;
            }
        }
    }

    double get_average_waiting_time() {
        return (car_count != 0) ? (total_waiting_time / car_count) : INFINITY;
    }

private:
    std::vector<Car> first_direction_queue;
    std::vector<Car> second_direction_queue;
    int n;
    int m;
    int elapsed_time;
    int first_direction_arrival_time;
    int second_direction_arrival_time;
    int cars_cooldown;
    int red_light_time;
    double total_waiting_time;
    int car_count;

    double random_expovariate(double rate) {
        std::random_device rd;
        std::default_random_engine generator(rd());
        std::exponential_distribution<double> distribution(rate);
        return distribution(generator);
    }
};

int main() {
    int optimal_n = 0;
    int optimal_m = 0;
    int sum_in_n = 0;
    int min_n, max_n, min_m, max_m, simulating_time;
    double min_avg_waiting_time = INFINITY;
    std::cout << "Enter minimum simulation n: ";
    std::cin >> min_n;
    std::cout << "Enter maximum simulation n: ";
    std::cin >> max_n;

    std::cout << "Enter minimum simulation m: ";
    std::cin >> min_m;
    std::cout << "Enter maximum simulation m: ";
    std::cin >> max_m;

    std::cout << "Enter simulation time: ";
    std::cin >> simulating_time;

    for (int n = min_n; n < max_n; ++n) {
        for (int m = min_m; m < max_m; ++m) {
            TrafficSimulation simulation(n, m);
            simulation.simulate(simulating_time);
            double avg_waiting_time = simulation.get_average_waiting_time();
            std::cout << "n: " << n << " | m: " << m << "| average waiting time: " << avg_waiting_time << std::endl;
            sum_in_n += avg_waiting_time;
            if (avg_waiting_time < min_avg_waiting_time) {
                min_avg_waiting_time = avg_waiting_time;
                optimal_n = n;
                optimal_m = m;
            }
        }
        std::cout << n << " average time " << (sum_in_n/(max_n-min_n)) << std::endl;
        sum_in_n = 0;
    }

    std::cout << "Optimal n: " << optimal_n << std::endl;
    std::cout << "Optimal m: " << optimal_m << std::endl;
    std::cout << "Minimum average waiting time: " << min_avg_waiting_time << std::endl;

    return 0;
}
