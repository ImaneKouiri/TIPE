import numpy as np
import time
import math

class aphysix():
    def __init__(self) -> None:
        self.g = 9.8
        self.c = 0.002  # drag coefficient


    def get_data(self, initial_angle, initial_velocity):
        x = np.linspace(0.1, 400, 1000)
        y = x * np.tan(initial_angle) - (self.g * x**2) / (2 * initial_velocity**2 * np.cos(initial_angle)**2) * ((-1 - 2*self.c*x + np.exp(2*self.c*x)) / (0.5 * (2*self.c*x)**2))
        return np.max(x), np.max(y), np.column_stack((x, y))
        #return x, y
        
    def get_angle_from_distance(self, distance, initial_velocity):
        theta = 0.5*np.arcsin((self.g*distance)/(initial_velocity**2)*((-1-2*self.c*distance+np.exp(2*self.c*distance))/(0.5*((2*self.c*distance)**2))))
        return theta
