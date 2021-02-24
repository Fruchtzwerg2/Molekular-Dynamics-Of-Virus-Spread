from enum import Enum 
import numpy as np


class Status(Enum):
    """
    Represents the status (S, I, R) of human
    """

    SUCEPTIBLE = 0
    INFECTED = 1
    RECOVERED = 2


status_colors = {
    Status.SUCEPTIBLE: "#0000df",
    Status.INFECTED: "#df0000",
    Status.RECOVERED: "#4a4a4a",
}


class Human:
    """
    Humans can be suceptible (S), infected (I) or recovered (R).
    They have a location (x and y) that determines their movement
    when combined with the potential.
    When moving they are given new coordinates. Upon assignment
    a human object checks if it is moving outside the given bounds.
    If so, the human calculates a new position like if it was
    bouncing off the boundary.
    """

    def __init__(
        self,
        location,
        velocity,
        infection_probability=0.1,
        radius=1.26,
        infection_radius=20,
        status=Status.SUCEPTIBLE,
        time_till_recovery=0,
    ):
        """
        initialises the human

        Args:
            location (tuple): position of the human 
            velocity (tuple): velocity of the human
            infection_probbability (float): probbability of getting infected (between 0 and 1)
            radius (float): radius of the circle shown in the graphic
            infection_radius (float): maximum distance a human can infect another
            status (class attribute): status of health (suceptible, infected, recovered) 
            time_till_recovery (float): time till the human is recovered from infection

        Attr:
            self._x (float): x-position
            self._y (float): x-position 
            self._vx (float): velocity in x direction
            self._vy (float): velocity in y direction
            self._ax (float): acceleration in x direction
            self._ay (float): acceleration in y direction
            self.radius (float): radius of the circle shown in the graphic
            self.infection_radius (float):  maximum distance a human can infect another
            self.infection_probability (float): probbability of getting infected (between 0 and 1)
            self.status (class attribute): status of health (suceptible, infected, recovered) 
            self.time_till_recovery (float): time till the human is recovered from infection
        """
        self._x = location[0]
        self._y = location[1]
        self._vx = velocity[0]
        self._vy = velocity[1]
        self._ax = 0.0
        self._ay = 0.0
        self.radius = radius
        self.infection_radius = infection_radius
        self.infection_probability = infection_probability
        self.status = status
        self.time_till_recovery = time_till_recovery

    @property
    def location(self):
        """
        location of the point as tuple

        Returns:
            location (array): current location
        """
        return np.array((self._x, self._y))

    @location.setter
    def location(self, new_location):
        """
        sets a new location and makes sure the human is already partily out of the graphic

        Args:
            new_location (tuple): changed location
        """
        x = new_location[0]
        y = new_location[1]
        if x >= 100 - self.radius:
            x = 100 - self.radius
        if x <= self.radius:
            x = self.radius
        if y >= 100 - self.radius:
            y = 100 - self.radius
        if y <= self.radius:
            y = self.radius
        self._x = round(x, 3)
        self._y = round(y, 3)

    @property
    def velocity(self):
        """
        velocity of the point as tuple
        Returns:
            lvelocity (array): current velocity
        """
        return np.array((self._vx, self._vy))

    @velocity.setter
    def velocity(self, new_velocity):
        """
        sets a new velocity for the human and creates a bounce off the walls if they are hit

        Args:
            new_velocity (tuple): changed velocity
        """
        vx = new_velocity[0]
        vy = new_velocity[1]
        if self._x <= self.radius and vx < 0:
            vx *= -1
        elif self._x >= 100 - self.radius and vx > 0:
            vx *= -1
        if self._y <= self.radius and vy < 0:
            vy *= -1
        elif self._y >= 100 - self.radius and vy > 0:
            vy *= -1
        self._vx = vx
        self._vy = vy

    @property
    def acceleration(self):
        """
        acceleration of the point as tuple

        Returns:
            acceleration (array): current acceleration
        """
        return np.array((self._ax, self._ay))

    @acceleration.setter
    def acceleration(self, new_acceleration):
        """
        sets a new acceleration for the human

        Args:
            new_acceleration (tuple): changed acceleration
        """
        self._ax = new_acceleration[0]
        self._ay = new_acceleration[1]

    @property
    def color(self):
        """
        gives the color corresponding to the health status

        Returns:
            status_colors (string): color code 
        """
        return status_colors[self.status]

    def infect(self, time_till_recovery=200):
        """
        sets status to infected and changes the time till recovery

        Args:
            time_till_recovery (float): time of the infection
        """
        self.status = Status.INFECTED
        self.time_till_recovery = time_till_recovery

    def update(self, new_location, new_velocity):
        """
        updates a human, it is given a new location, velocity,
        if infected the human will count down the time_till_recovery
        until at zero to set the status to RECOVERED.

        Args:
            new_location (tuple): changed velocity
            new_velocity (tuple): changed velocity
        """
        self.velocity = new_velocity
        self.location = new_location
        if self.is_infected():
            self.time_till_recovery -= 1
            if self.time_till_recovery <= 0:
                self.status = Status.RECOVERED

    def is_suceptible(self):
        """returns True is human is suceptible"""
        return self.status == Status.SUCEPTIBLE

    def is_infected(self):
        """returns True is human is infected"""
        return self.status == Status.INFECTED

    def is_recovered(self):
        """returns True is human is recovered"""
        return self.status == Status.RECOVERED

    def set_location(self, x, y, world_lim=100):
        """
        If a Human would have it's origin outside the boundaries, 
        it will be moved inside.
        """
        if x + self.radius > world_lim:
            x = world_lim - self.radius
        if x < self.radius:
            x = self.radius 
        if y + self.radius > world_lim:
            y = world_lim - self.radius
        if y < self.radius:
            y = self.radius
        self._x = round(x, 3)
        self._y = round(y, 3)

    def bounce(self, x, y, vx, vy, world_lim=100):
        """
        Calculates the new velocity of a Human that hit a boundary.
        """
        if (x < self.radius) or (x + self.radius > world_lim):
            vx *= -1
        if (y < self.radius) or (y + self.radius > world_lim):
            vy *= -1
        self._vx = vx
        self._vy = vy
        self.set_location(x, y)

    def will_infect(self, other_human):
        """
        checks if another human gets infected

        Args:
            other_human (object): human within the infection radius
        """
        return self.is_infected() and other_human.is_suceptible() and np.random.rand() <= self.infection_probability
