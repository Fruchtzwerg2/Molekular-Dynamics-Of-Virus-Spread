import math
import numpy as np
import random
from src.human import Human, Status

# constants for the potential
epsilon = 2
sigma = 7.5


def calculate_movement(humans, dt, energy):
    """
    calculates location, speed and acceleration in respect to the potential

    Args:
        humans (list): list of all humans
        dt (float): time step in which the movement is calculated
        energy (float): amount of movement

    Returns:
        humans (list): list of all humans
    """
    new_energy = 0
    old_humans = humans
    for i, h in enumerate(humans):
        new_location = h.location + dt * h.velocity + \
            0.5 * dt ** 2 * old_humans[i].acceleration
        calculate_interactions(humans, h, i)
        infection(humans, h, i)
        new_velocity = h.velocity + 0.5 * dt * h.acceleration
        # subtract the old value so that we are "starting the next calculation for the acceleration from 0"
        h.acceleration -= old_humans[i].acceleration

        # handle maximum velocity based on total energy
        new_energy += np.linalg.norm(new_velocity)**2
        factor = math.sqrt(energy / new_energy)
        new_velocity = new_velocity*factor

        # checks that single particles get too fast
        abs_speed = np.linalg.norm(new_velocity)**2
        factor_v = math.sqrt(abs_speed / energy)
        if factor_v > 3*(1/len(humans)):
            scaling = 0.03/factor_v
            new_velocity = new_velocity*scaling
        h.update(new_location, new_velocity)
    return humans


def random_walk(humans, dt, energy, temperature):
    """
    calculates location, speed and acceleration by adding random values to the speed

    Args:
        humans (list): list of all humans
        dt (float): time step in which the movement is calculated
        energy (float): amount of movement

    Returns:
        humans (list): list of all humans
    """
    new_energy = 0
    old_humans = humans
    for i, h in enumerate(humans):
        infection(humans, h, i)
        new_location = h.location + dt * h.velocity
        velocity_gen_x = random.gauss(0, 1)
        velocity_gen_y = random.gauss(0, 1)
        velocity_random = [
            velocity_gen_x * float(temperature)/15, velocity_gen_y * float(temperature)/15]
        new_velocity = h.velocity + velocity_random

        # handle maximum velocity based on total energy
        new_energy += np.linalg.norm(new_velocity)**2
        factor = math.sqrt(energy / new_energy)
        new_velocity = new_velocity*factor

        abs_speed = np.linalg.norm(new_velocity)**2
        factor_v = math.sqrt(abs_speed / energy)
        if factor_v > 3*(1/len(humans)):
            scaling = 0.03/factor_v
            new_velocity = new_velocity*scaling
        h.update(new_location, new_velocity)
    return humans


def calculate_interactions(humans, h, i):
    """
    calculates the force between 2 particles if they are near enough

    Args:
        humans (list): list of all humans
        i (index): index going through humans
        h (index): index going through humans
    """
    for p in humans[i + 1:]:
        dist = math.dist(h.location, p.location)
        if dist < 3 * h.radius and dist > 0:
            # calculate repulsion force
            ljp = lennard_jones(dist)
            force = ljp * ((h.location - p.location) / dist)
            h.acceleration += force
            p.acceleration -= force


def infection(humans, h, i):
    """
    infects humans within the infection radius of an infected human

    Args:
        humans (list): list of all humans
        i (index): index going through humans
        h (index): index going through humans
    """
    for p in humans[i + 1:]:
        dist = math.dist(h.location, p.location)
        if dist < h.infection_radius and dist > 0:
            if p.will_infect(h):
                h.infect()
        if dist < p.infection_radius and dist > 0:
            if h.will_infect(p):
                p.infect()


def lennard_jones(r):
    """
    calculates the force resulting from the potential

    Args:
        r (float): distance between two humans
    """
    # derivative of 4 * epsilon * ((sigma / r) ** 12 - (sigma / r) ** 6)
    return (-24 * epsilon * sigma ** 6 * (r ** 6 - 2 * sigma ** 6)) / (r ** 13)
