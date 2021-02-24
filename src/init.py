import numpy as np
import random
import math
from src.human import Human, Status


def infect_random(humans, number_of_humans):
    """
    a random Human is selected and gets infected
    
    Args:
        number_of_humans (int): amount of humans in the simulation
        
    Returns:
        humans (list): list containing all humans
    """
    random_number = np.random.randint(int(number_of_humans))
    humans[random_number].infect()
    return humans

def make_vulnerable(humans, number_of_humans, number_vulnerable_humans, infection_radius, prob): 
    """
    A certain number of humans becomes gets more vulnerable, which makes it easier for him/her 
    to get infected.
    
    Args: 
        number_of_humans (int): total amount of humans in the simulation
        number_vulnerable_humans (int): amount of humans that are more vulnerable
        infection_radius (float): distance at which a human gets infected
        prob (float): probability of infection for standard humans
    
    Returns:
        humans (list): a list containing all humans (the ones that are more vulnerable and the 
        ones that are not)
    """
    while number_vulnerable_humans > 0:
        random_number = np.random.randint(int(number_of_humans))
        if humans[random_number].infection_radius == infection_radius:
            humans[random_number].infection_radius *= random.gauss(1.9, 0.2)
            humans[random_number].infection_probability *= random.gauss(1.9, 0.2)
            if humans[random_number].infection_probability >= 1:
                humans[random_number].infection_probability = 0.99
            number_vulnerable_humans -= 1
    return humans

def wear_mask(humans, number_of_humans, number_mask_humans, infection_radius, prob):
    """
    A specific number of humans wears a face mask now. Therefore the infection probability
    and the infection radius become smaller.
    
    Args: 
        number_of_humans (int): total amount of humans in the simulation
        number_mask_humans (int): amount of humans that are wearing a face mask
        prob (float): probability of infection for standard humans
    
    Returns:
        humans (list): a list containing all humans (the ones that are wearing a face 
        mask and the ones that are not)
    """
    while number_mask_humans > 0:
        random_number = np.random.randint(int(number_of_humans))
        if humans[random_number].infection_radius == infection_radius:
            humans[random_number].infection_radius *= random.gauss(0.45, 0.2)
            humans[random_number].infection_probability *= random.gauss(0.45, 0.2)
            number_mask_humans -= 1
    return humans

def init_sys(
    temperature,
    prob,
    number_of_humans,
    world_limit=100,
    infection_radius=5,
    min_distance=1.5,
):
    """
    initializes the simulation with a certain number of humans, makes sure the humans wont overlap
    and infects randomly one of them
    
    Args:
        temperature (float): temperature of the system, influcences velocity
        prob (float): probbability of a human getting infected (between 0 and 1)
        world_limit (float): length of the x and y axis
        infection_radius (float): maximum distance a human can infect another
        min_radius (float): minimmal distance between humans
        
    Returns:
        humans (list): list containing all humans
        energy (float): amount of movement in the system
    """

    if float(prob) > 1:
        raise ValueError("Wahrscheinlichkeit muss kleiner oder gleich 1 sein.")

    humans = []
    energy = 0

    while len(humans) < float(number_of_humans):
        # create location
        location_gen = np.random.rand(2)
        location = (world_limit - 2 * min_distance) * location_gen + [
            min_distance,
            min_distance,
        ]
        # check if two humans overlap
        overlap = False
        for s in humans:
            dist = math.dist(location, s.location)
            if dist < 2*min_distance:
                overlap = True
                break
        if overlap == False:
            # create velocity
            velocity_gen_x = random.gauss(0, 1)
            velocity_gen_y = random.gauss(0, 1)
            velocity = [velocity_gen_x * float(temperature), velocity_gen_y * float(temperature)]
            
            # create the human and put it in the list
            new_human = Human(
                location,
                velocity,
                infection_probability=prob,
                radius=min_distance,
                infection_radius=infection_radius,
                status=Status.SUCEPTIBLE,
                time_till_recovery=0,
            )
            # calculate energy
            energy += np.linalg.norm(new_human.velocity)**2

            humans.append(new_human)

    infect_random(humans, number_of_humans)
    return humans, energy
