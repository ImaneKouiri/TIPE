import numpy as np

k = 0 # "Spring" constant
x = 0 # Draw lenght
F = -k*x # Draw weight

m = 0 # Mass
g = 9.8 # Gravitational constant
h = 0 # Height

v = 0 # Velocity

# Constants
g = 9.81  # acceleration due to gravity, m/s^2
v0 = 87.03  # initial velocity, m/s
theta = np.pi / 6  # launch angle, radians
c = 0.002  # drag coefficient

elastic_potential_energy = 1/2 *k*x**2
kinetic_energy = 1/2*m*v**2

import time
import sys
import math

class aphysix():
    def __init__(self, spring_constant, arrow_mass) -> None:
        self.spring_constant = spring_constant
        self.arrow_mass = arrow_mass
        self.g = 9.8

    def elastic_potential_energy(self, draw_lenght):
        return 0.5 * self.spring_constant * (draw_lenght**2)
    
    def kinetic_energy(self, velocity):
        return 0.5 * self.arrow_mass * (velocity**2)
    
    def gravitational_energy(self, y):
        return self.arrow_mass*self.g*y
    
    def get_initial_velocity(self, draw_lenght):
        return math.sqrt((self.spring_constant/self.arrow_mass)*draw_lenght**2)
    
    def get_current_y(self, current_travel_time, initial_velocity, initial_angle):
        """
        function to get the current y in the plane. y expression:
            y = v0.sin(theta).t - 1/2.g.t²
        """
        first_term = initial_velocity*math.sin(initial_angle)*current_travel_time
        second_term = 1/2*self.g*(current_travel_time**2)
        return first_term - second_term
    
    def get_current_x(self, current_travel_time, initial_velocity, initial_angle):
        """
        function to get the current y in the plane. y expression:
            x = v0.cos(theta).t
        """
        return initial_velocity*math.cos(initial_angle)*current_travel_time

    def get_velocity(self, current_travel_time, initial_velocity, initial_angle):
        first_term = initial_velocity**2
        second_term = 2*initial_velocity*math.sin(initial_angle)*self.g*current_travel_time
        third_term = (self.g**2)*(current_travel_time**2)
        return math.sqrt(first_term-second_term+third_term)

    def step(self, draw_lenght, initial_angle, current_time):

        initial_velocity = self.get_initial_velocity(draw_lenght)
        initial_gravitational_energy = self.gravitational_energy(0)
        initial_kinetic_energy = self.kinetic_energy(initial_velocity)

        current_y = self.get_current_y(current_time, initial_velocity, initial_angle)
        current_x = self.get_current_x(current_time, initial_velocity, initial_angle)

        gravitational_energy = self.gravitational_energy(current_y)
        kinetic_energy = self.kinetic_energy(self.get_velocity(current_time, initial_velocity, initial_angle))
        ep_energy = gravitational_energy + kinetic_energy

        return (gravitational_energy, kinetic_energy, ep_energy, current_x, current_y)
    
    def get_data(self, initial_angle, initial_velocity):
        x = np.linspace(0.1, 400, 1000)
        y = x * np.tan(initial_angle) - (g * x**2) / (2 * initial_velocity**2 * np.cos(initial_angle)**2) * ((-1 - 2*c*x + np.exp(2*c*x)) / (0.5 * (2*c*x)**2))
        return np.max(x), np.max(y), np.column_stack((x, y))
        #return x, y
        


    def run(self, draw_lenght, initial_angle, step=1):

        points = []

        current_y = 0
        current_x = 0
        current_time = 0

        initial_velocity = self.get_initial_velocity(draw_lenght)
        initial_gravitational_energy = self.gravitational_energy(current_y)
        initial_kinetic_energy = self.kinetic_energy(initial_velocity)

        travel_time = 10
        end_time = time.time() + travel_time
        #decay_rate = 1 / (travel_time * 100)
        #decay_amount = decay_rate * initial_ep_energy

        ep_energy = self.elastic_potential_energy(draw_lenght)
        kinetic_energy = initial_kinetic_energy

        start_time = time.time()
        start = True
        while True:
            time.sleep(step)
            current_time += 0.05

            current_y = self.get_current_y(current_time, initial_velocity, initial_angle)
            current_x = self.get_current_x(current_time, initial_velocity, initial_angle)

            gravitational_energy = self.gravitational_energy(current_y)
            kinetic_energy = self.kinetic_energy(self.get_velocity(current_time, initial_velocity, initial_angle))
            ep_energy = gravitational_energy + kinetic_energy
            #gravitational_energy = ep_energy - kinetic_energy

            print(f"Gravitational energy: {gravitational_energy} | Kinetic energy: {kinetic_energy} | Elastic potential energy: {ep_energy} | X: {current_x} | Y: {current_y}", end="\r")
            
            points.append((gravitational_energy, kinetic_energy, ep_energy, current_x, current_y))
            if start:
                start = False                                                                
            if current_y <= 0 and not start:
                break

        print(f"Gravitational energy: {gravitational_energy} | Kinetic energy: {kinetic_energy} | Elastic potential energy: {ep_energy} | X: {current_x} | Y: {current_y}")
        time_taken = time.time() - start_time
        print(f"Time taken: {round(time_taken, 4)} seconds")
        return points


if __name__ == "__main__":

    draw_lenght = 0.5
    initial_angle = math.pi/4
    k = 600
    arrow_mass = 0.018

    archery = aphysix(k, arrow_mass)
    archery.run(draw_lenght, initial_angle, step=0)