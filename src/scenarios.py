import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
import math
import time
import random
import numpy as np

from src.human import Status
import src.init as init
import src.simulation as sim


# global variables that will influence the simulation, including default values
world_limit = 100
time_step = 0.0001
plot_refresh_rate = 20


# global lists the simulation will work with
# lists used by almost all scenarios
global_humans = []
inf = []
suc = []
rec = []
steps = []
# lists used by the cities scenario
humans_city1 = []
humans_city2 = []
humans_city3 = []
# lists used by the vulnerable scenario
inf_mask = []
suc_mask = []
rec_mask = []
inf_vulnerable = []
suc_vulnerable = []
rec_vulnerable = []
# lists used by the quarantine scenario
quarantine_humans = []
qua = []


# standard scenario
def scenario_basic(plot=plt, show=False):
    """
    creates the basic scenario

    Args:
        plot: plot to show
        show (bool): variable if graphic should be shown

    Returns:
        plot: plot to show
        ani_humans: animation of the humans
        ani_stack: animation of the stackplot
    """
    # variables that influence the simulation
    prob, infection_radius, number_of_humans, temperature = ask_for_input()

    # plot setup
    fig = plot.figure(figsize=(10, 4))

    # humans
    plot_humans = fig.add_subplot(1, 2, 1)
    plot_humans.axes.xaxis.set_visible(False)
    plot_humans.axes.yaxis.set_visible(False)

    # stackplot
    plot_stack = fig.add_subplot(1, 2, 2)
    plot_stack.set_frame_on(False)
    plot_stack.axes.xaxis.set_visible(False)
    plot_stack.axes.yaxis.set_visible(False)

    # setting up the list of humans
    global_humans, energy = init.init_sys(
        temperature,
        prob,
        number_of_humans,
        infection_radius=infection_radius,
        world_limit=world_limit,
    )

    inf = []
    suc = []
    rec = []
    steps = []

    # animation of the movement of humans
    ani_humans = animation.FuncAnimation(
        fig,
        scenario_basic_animation,
        fargs=[global_humans, plot_humans, time_step, energy],
        interval=plot_refresh_rate,
    )

    # animation of the stackplot
    ani_stack = animation.FuncAnimation(
        fig,
        stack_animation,
        fargs=[global_humans, plot_stack, time_step,
               inf, rec, suc, steps, number_of_humans],
        interval=plot_refresh_rate)

    if show:
        plot.show()
    return plot, ani_humans, ani_stack


# scenario randomwalk
def scenario_randomwalk(plot=plt, show=False):
    """
    creates the random walk scenario

    Args:
        plot: plot to show
        show (bool): variable if graphic should be shown

    Returns:
        plot: plot to show
        ani_humans: animation of the humans
        ani_stack: animation of the stackplot
    """
    # variables that influence the simulation
    prob, infection_radius, number_of_humans, temperature = ask_for_input()

    # plot setup
    fig = plot.figure(figsize=(10, 4))

    # humans
    plot_humans = fig.add_subplot(1, 2, 1)
    plot_humans.axes.xaxis.set_visible(False)
    plot_humans.axes.yaxis.set_visible(False)

    # stackplot
    plot_stack = fig.add_subplot(1, 2, 2)
    plot_stack.set_frame_on(False)
    plot_stack.axes.xaxis.set_visible(False)
    plot_stack.axes.yaxis.set_visible(False)

    global_humans, energy = init.init_sys(
        temperature,
        prob,
        number_of_humans,
        infection_radius=infection_radius,
        world_limit=world_limit,
    )

    inf = []
    suc = []
    rec = []
    steps = []

    # animation of the movement of humans
    ani_humans = animation.FuncAnimation(
        fig,
        scenario_random_animation,
        fargs=[global_humans, plot_humans, time_step, energy, temperature],
        interval=plot_refresh_rate,
    )

    # animation of the stackplot
    ani_stack = animation.FuncAnimation(
        fig,
        stack_animation,
        fargs=[global_humans, plot_stack, time_step,
               inf, rec, suc, steps, number_of_humans],
        interval=plot_refresh_rate)

    if show:
        plot.show()
    return plot, ani_humans, ani_stack


# scenario cities
def scenario_cities(plot=plt, show=False):
    """
    creates scenario with three cities

    Args:
        plot: plot to show
        show (bool): variable if graphic should be shown

    Returns:
        plot: plot to show
        ani_city1: animation of city number 1
        ani_city2: animation of city number 2
        ani_city3: animation of city number 3
        ani_stack: animation of the stackplot
    """
    # variables that influence the simulation
    prob, infection_radius, number_of_humans, temperature = ask_for_input()

    # plot setup
    fig = plot.figure(figsize=(10, 8))

    # city1
    plot_city1 = fig.add_subplot(2, 2, 1)
    plot_city1.axes.xaxis.set_visible(False)
    plot_city1.axes.yaxis.set_visible(False)

    # city2
    plot_city2 = fig.add_subplot(2, 2, 2)
    plot_city2.axes.xaxis.set_visible(False)
    plot_city2.axes.yaxis.set_visible(False)

    # city3
    plot_city3 = fig.add_subplot(2, 2, 3)
    plot_city3.axes.xaxis.set_visible(False)
    plot_city3.axes.yaxis.set_visible(False)

    # stackplot
    plot_stack1 = fig.add_subplot(2, 2, 4)
    plot_stack1.set_frame_on(False)
    plot_stack1.axes.xaxis.set_visible(False)
    plot_stack1.axes.yaxis.set_visible(False)

    humans_city1, energy1 = init.init_sys(
        temperature,
        prob,
        number_of_humans,
        infection_radius=infection_radius,
        world_limit=world_limit,
    )
    humans_city2, energy2 = init.init_sys(
        temperature,
        prob,
        number_of_humans,
        infection_radius=infection_radius,
        world_limit=world_limit,
    )
    humans_city3, energy3 = init.init_sys(
        temperature,
        prob,
        number_of_humans,
        infection_radius=infection_radius,
        world_limit=world_limit,
    )
    # setting all humans in city 2 and 3 to succeptible
    for h in humans_city2:
        h.status = Status.SUCEPTIBLE
    for h in humans_city3:
        h.status = Status.SUCEPTIBLE

    # setup for city1
    ani_city1 = animation.FuncAnimation(
        fig,
        scenario_cities_animation,
        fargs=[humans_city1, humans_city2, humans_city3,
               plot_city1, time_step, energy1, steps],
        interval=plot_refresh_rate,
    )

    # setup for city2
    ani_city2 = animation.FuncAnimation(
        fig,
        scenario_cities_animation,
        fargs=[humans_city2, humans_city1, humans_city3,
               plot_city2, time_step, energy2, steps],
        interval=plot_refresh_rate,
    )

    # setup for city3
    ani_city3 = animation.FuncAnimation(
        fig,
        scenario_cities_animation,
        fargs=[humans_city3, humans_city2, humans_city1,
               plot_city3, time_step, energy3, steps],
        interval=plot_refresh_rate,
    )

    # setup for stackplot
    ani_stack = animation.FuncAnimation(
        fig,
        stack_animation_cities,
        fargs=[humans_city1, humans_city3, humans_city2,
               plot_stack1, time_step, inf, rec, suc, steps],
        interval=plot_refresh_rate)

    if show:
        plot.show()
    return plot, ani_city1, ani_city2, ani_city3, ani_stack

# scenario vulnerable
def scenario_mask_vulnerable(plot=plt, show=False):
    """
    creates scenario with different groups that are more or less vulnerable

    Args:
        plot: plot to show
        show (bool): variable if graphic should be shown

    Returns:
        plot: plot to show
        ani_humans: animation of the humans
        ani_stack: animation of the stackplot
    """
    # variables that influence the simulation
    prob, infection_radius, number_of_humans, temperature, number_vulnerable_humans, number_humans_with_mask = ask_for_different_input()
    number_standard_humans = number_of_humans - \
        number_vulnerable_humans - number_humans_with_mask

    # plot setup
    fig = plot.figure(figsize=(10, 4))

    # for healthy and vulnerable humans
    plot_humans = fig.add_subplot(1, 2, 1)
    plot_humans.axes.xaxis.set_visible(False)
    plot_humans.axes.yaxis.set_visible(False)

    # for stackplot
    plot_stack = fig.add_subplot(1, 2, 2)
    plot_stack.set_frame_on(False)
    plot_stack.axes.xaxis.set_visible(False)
    plot_stack.axes.yaxis.set_visible(False)

    # setting up the list of humans
    global_humans, energy = init.init_sys(
        temperature,
        prob,
        number_of_humans,
        infection_radius=infection_radius,
        world_limit=world_limit,
    )

    global_humans = init.make_vulnerable(
        global_humans, number_of_humans, number_vulnerable_humans, infection_radius, prob)
    global_humans = init.wear_mask(
        global_humans, number_of_humans, number_humans_with_mask, infection_radius, prob)

    inf = []
    suc = []
    rec = []

    inf_mask = []
    suc_mask = []
    rec_mask = []

    inf_vulnerable = []
    suc_vulnerable = []
    rec_vulnerable = []

    steps = []

    # animation of the movement of humans
    ani_humans = animation.FuncAnimation(
        fig,
        scenario_basic_animation,
        fargs=[global_humans, plot_humans, time_step, energy],
        interval=plot_refresh_rate,
    )

    # animation of the stackplot
    ani_stack = animation.FuncAnimation(
        fig,
        stack_animation_mask_vulnerable,
        fargs=[
            global_humans,
            plot_stack,
            time_step,
            inf_vulnerable, inf, inf_mask,
            rec_vulnerable, rec, rec_mask,
            suc_vulnerable, suc, suc_mask,
            steps,
            number_of_humans,
            infection_radius],
        interval=plot_refresh_rate)

    if show:
        plot.show()
    return plot, ani_humans, ani_stack


# scenario quarantine
def scenario_quarantine(plot=plt, show=False):
    """
    creates scenario where infected humans get quarantined

    Args:
        plot: plot to show
        show (bool): variable if graphic should be shown

    Returns:
        plot: plot to show
        ani_humans: animation of the humans
        ani_stack: animation of the stackplot
    """
    # variables that influence the simulation
    world_limit = 100
    infection_radius = 5
    time_step = 0.0001
    plot_refresh_rate = 20
    prob = 1
    number_of_humans = 50
    temperature = 10000
    #prob, number_of_humans, temperature = ask_for_input()
    detection_probability = ask_for_even_more_input() * time_step

    # plot setup
    fig = plot.figure(figsize=(10, 4))

    # for humans
    plot_humans = fig.add_subplot(2, 2, 1)
    plot_humans.axes.xaxis.set_visible(False)
    plot_humans.axes.yaxis.set_visible(False)

    # for quarantine
    plot_quarantine = fig.add_subplot(2, 2, 2)
    plot_quarantine.set_frame_on(False)
    plot_quarantine.axes.xaxis.set_visible(False)
    plot_quarantine.axes.yaxis.set_visible(False)

    # for stackplot
    plot_stack = fig.add_subplot(2, 2, 3)
    plot_stack.set_frame_on(False)
    plot_stack.axes.xaxis.set_visible(False)
    plot_stack.axes.yaxis.set_visible(False)

    # setting up the list of humans
    global_humans, energy = init.init_sys(
        temperature,
        prob,
        number_of_humans,
        infection_radius=infection_radius,
        world_limit=world_limit,
    )

    inf = []
    suc = []
    rec = []
    steps = []

    # animation of the movement of humans
    ani_humans = animation.FuncAnimation(
        fig,
        scenario_basic_animation,
        fargs=[global_humans, plot_humans, time_step, energy],
        interval=plot_refresh_rate,
    )

    # animation for quarantine number
    ani_quarantine = animation.FuncAnimation(
        fig,
        quarantine_animation,
        fargs=[global_humans, quarantine_humans,
               detection_probability, plot_quarantine],
        interval=plot_refresh_rate
    )

    # animation of the stackplot
    ani_stack = animation.FuncAnimation(
        fig,
        stack_animation_quarantine,
        fargs=[global_humans, quarantine_humans, plot_stack,
               time_step, inf, rec, suc, steps, number_of_humans],
        interval=plot_refresh_rate)

    if show:
        plot.show()
    return plot, ani_humans, ani_stack, ani_quarantine


# animations
def scenario_basic_animation(i, humans, subplot, time_step, energy):
    """
    updates human every timestep

    Args:
        humans (list): list of all humans
        subplot (plot): plot that gets animated
        time_step (float): timestep in which movement is calculated
        energy (float): amount of movement
    """
    new_energy = 0
    xs = []
    ys = []
    colors = []

    # set colors
    for h in humans:
        xs.append(float(h._x))
        ys.append(float(h._y))
        colors.append(h.color)

    subplot.clear()
    subplot.scatter(xs, ys, s=25, c=colors)
    subplot.set_ylim(0, 100)
    subplot.set_xlim(0, 100)
    global_humans = sim.calculate_movement(humans, time_step, energy)


def scenario_random_animation(i, humans, subplot, time_step, energy, temperature):
    """
    updates human every timestep

    Args:
        humans (list): list of all humans
        subplot (plot): plot that gets animated
        time_step (float): timestep in which movement is calculated
        energy (float): amount of movement
        temperature (float) influences speed of the humans
    """
    new_energy = 0
    xs = []
    ys = []
    colors = []

    for h in humans:
        xs.append(float(h._x))
        ys.append(float(h._y))
        colors.append(h.color)

    subplot.clear()
    subplot.scatter(xs, ys, s=25, c=colors)
    subplot.set_ylim(0, 100)
    subplot.set_xlim(0, 100)
    global_humans = sim.random_walk(humans, time_step, energy, temperature)


def scenario_cities_animation(i, humans, others1, others2, subplot, time_step, energy, steps):
    """
    updates the hmans everytimestep and moves every few steps humans from city to city

    Args:
        humans (list): list of all humans in the animated city
        others1 (list): list of all humans in the one of the other two cities
        others2 (list): list of all humans in the one of the other two cities
        subplot (plot): plot that gets animated
        time_step (float): timestep in which movement is calculated
        energy (float): amount of movement
        temperature (float): influences speed of the humans
        steps (list): list containing all time_steps from the past
    """
    new_energy = 0
    xs = []
    ys = []
    colors = []

    for h in humans:
        xs.append(float(h._x))
        ys.append(float(h._y))
        colors.append(h.color)

    subplot.clear()
    subplot.scatter(xs, ys, s=25, c=colors)
    subplot.set_ylim(0, 100)
    subplot.set_xlim(0, 100)
    global_humans = sim.calculate_movement(humans, time_step, energy)

    # Particles moving from city to city
    if len(steps) % 25 == False and len(steps) != 0:
        random_number1 = random.randint(0, len(humans)-1)
        random_number2 = random.randint(0, len(humans)-1)
        while random_number1 == random_number2:
            random_number2 = random.randint(0, len(humans)-1)
        if random_number1 != random_number2:
            others1.append(humans[random_number1])
            others2.append(humans[random_number2])
            if random_number1 > random_number2:
                del humans[random_number1]
                del humans[random_number2]
            if random_number2 > random_number1:
                del humans[random_number2]
                del humans[random_number1]


def quarantine_animation(i, humans, quarantined, detection_probability, plot):
    """
    updates human every timestep

    Args:
        humans (list): list of all humans
        quarantined (list): ist of quarantined humans
        plot (plot): plot that gets animated
    """
    for h in humans:
        if h.is_infected() and np.random.rand() < detection_probability:
            humans.remove(h)
            quarantined.append(h)

    for q in quarantined:
      # update only the recovery for people in quarantine
        q.update(q.location, q.velocity)
        if q.is_recovered():
            quarantined.remove(q)
            humans.append(q)

    global_humans = humans
    quarantine_humans = quarantined

    plot.clear()
    plot.text(0, 0.5, "Quarantined: " + str(len(quarantined)), size=20,
              bbox=dict(boxstyle="square", ec=(0.9, 0.68, 0.12), fc=(1., 0.78, 0.22)))


def stack_animation_cities(i, humans1, humans2, humans3, test, time_step, inf, rec, suc, steps):
    """
    updates the stackplot every timestep

    Args:
        humans1 (list): list of all humans in city number 1
        humans2 (list): list of all humans in city number 2
        humans3 (list): list of all humans in city number 3
        test: plot that gets animated
        time_step (float): timestep in which movement is calculated
        inf (list): list containing the amount of infected humans at all past timestep
        rec (list): list containing the amount of recovered humans at all past timestep
        suc (list): list containing the amount of suceptible humans at all past timestep
        steps (list): list containing all time_steps from the past
    """
    global_humans = humans1+humans2+humans3
    step_counter = len(suc)
    steps.append(time_step*step_counter)
    suc_s = 0
    inf_s = 0
    rec_s = 0
    for h in global_humans:
        if h.status == Status.SUCEPTIBLE:
            suc_s += 1
        if h.status == Status.INFECTED:
            inf_s += 1
        if h.status == Status.RECOVERED:
            rec_s += 1
    suc.append(suc_s)
    inf.append(inf_s)
    rec.append(rec_s)
    test.clear()
    test.set_ylim(0, len(global_humans))
    test.stackplot(steps, inf, rec, suc, colors=[
                   '#df0000', '#4a4a4a', '#0000df'])

    label1 = 'infected'
    label2 = 'recovered'
    label3 = 'succeptable'
    p1 = Rectangle((0, 0), 1, 1, fc='#df0000')
    p2 = Rectangle((0, 0), 1, 1, fc='#4a4a4a')
    p3 = Rectangle((0, 0), 1, 1, fc='#0000df')
    legend = test.legend([p1, p2, p3], [label1, label2, label3],
                         loc="lower center", bbox_to_anchor=(-0.12, -0.15), ncol=3)


def stack_animation_mask_vulnerable(
        i,
        humans,
        test,
        time_step,
        inf_vulnerable, inf, inf_mask,
        rec_vulnerable, rec, rec_mask,
        suc_vulnerable, suc, suc_mask,
        steps,
        number_of_humans,
        infection_radius):
    """
    updates the stackplot every timestep

    Args:
        humans (list): list of all humans in the animated city
        test: plot that gets animated
        time_step (float): timestep in which movement is calculated
        inf (list): list containing the amount of regular infected humans at all past timestep
        rec (list): list containing the amount of regular recovered humans at all past timestep
        suc (list): list containing the amount of regular suceptible humans at all past timestep
        inf_vulnerable (list): list containing the amount of infected vulnerable humans at all past timestep
        rec_vulnerable (list): list containing the amount of recovered vulnerable humans at all past timestep
        suc_vulnerable (list): list containing the amount of suceptible vulnerable humans at all past timestep
        inf_mask (list): list containing the amount of infected humans wearing masks at all past timestep
        rec_mask (list): list containing the amount of recovered humans wearing masks at all past timestep
        suc_mask (list): list containing the amount of suceptible humans wearing masks at all past timestep
        steps (list): list containing all time_steps from the past
        number_of_humans (float): amount of humans in the scenario

    """
    # updates the stackplot every timestep
    step_counter = len(suc)
    steps.append(time_step*step_counter)
    suc_s = 0
    inf_s = 0
    rec_s = 0

    suc_mask_s = 0
    inf_mask_s = 0
    rec_mask_s = 0

    suc_vulnerable_s = 0
    inf_vulnerable_s = 0
    rec_vulnerable_s = 0

    # counting the amount of different states
    for h in humans:
        if h.infection_radius == infection_radius:
            if h.status == Status.SUCEPTIBLE:
                suc_s += 1
            if h.status == Status.INFECTED:
                inf_s += 1
            if h.status == Status.RECOVERED:
                rec_s += 1
        elif h.infection_radius < infection_radius:
            if h.status == Status.SUCEPTIBLE:
                suc_mask_s += 1
            if h.status == Status.INFECTED:
                inf_mask_s += 1
            if h.status == Status.RECOVERED:
                rec_mask_s += 1
        elif h.infection_radius > infection_radius:
            if h.status == Status.SUCEPTIBLE:
                suc_vulnerable_s += 1
            if h.status == Status.INFECTED:
                inf_vulnerable_s += 1
            if h.status == Status.RECOVERED:
                rec_vulnerable_s += 1

    suc.append(suc_s)
    inf.append(inf_s)
    rec.append(rec_s)

    suc_mask.append(suc_mask_s)
    inf_mask.append(inf_mask_s)
    rec_mask.append(rec_mask_s)

    suc_vulnerable.append(suc_vulnerable_s)
    inf_vulnerable.append(inf_vulnerable_s)
    rec_vulnerable.append(rec_vulnerable_s)

    test.clear()
    test.set_ylim(0, len(humans))

    test.stackplot(
        steps,
        inf_vulnerable, inf, inf_mask,
        rec_vulnerable, rec, rec_mask,
        suc_vulnerable, suc, suc_mask,
        colors=[
            '#9c0000', '#df0000', '#eb6666',
            '#3b3b3b', '#4a4a4a', '#6e6e6e',
            '#00009c', '#0000df', '#6666eb'
        ])

    label1 = 'infected'
    label2 = 'infected (vulnerable)'
    label3 = 'infected (mask)'
    label4 = 'recovered'
    label5 = 'recovered (vulnerable)'
    label6 = 'recovered (mask)'
    label7 = 'succeptable'
    label8 = 'succeptable(vulnerable)'
    label9 = 'succeptable (mask)'
    p1 = Rectangle((0, 0), 1, 1, fc='#df0000')
    p4 = Rectangle((0, 0), 1, 1, fc='#4a4a4a')
    p7 = Rectangle((0, 0), 1, 1, fc='#0000df')
    p2 = Rectangle((0, 0), 1, 1, fc='#9c0000')
    p3 = Rectangle((0, 0), 1, 1, fc='#eb6666')
    p5 = Rectangle((0, 0), 1, 1, fc='#3b3b3b')
    p6 = Rectangle((0, 0), 1, 1, fc='#6e6e6e')
    p8 = Rectangle((0, 0), 1, 1, fc='#00009c')
    p9 = Rectangle((0, 0), 1, 1, fc='#6666eb')
    legend = test.legend([p1, p2, p3, p4, p5, p6, p7, p8, p9], [label1, label2, label3, label4, label5, label6,
                                                                label7, label8, label9], loc="lower right", bbox_to_anchor=(0.1, -0.15), ncol=3, fontsize='small')


def stack_animation_quarantine(i, humans, quarantined, test, time_step, inf, rec, suc, steps, number_of_humans):
    """
    updates the stackplot every timestep

    Args:
        humans (list): list of all humans in the animated city
        quarantined (list): list of all quarantined humans
        test: plot that gets animated
        time_step (float): timestep in which movement is calculated
        inf (list): list containing the amount of infected humans at all past timestep
        rec (list): list containing the amount of recovered humans at all past timestep
        suc (list): list containing the amount of suceptible humans at all past timestep
        steps (list): list containing all time_steps from the past
        number_of_humans (float): amount of humans in the scenario

    """
    step_counter = len(suc)
    steps.append(time_step*step_counter)
    suc_s = 0
    inf_s = 0
    rec_s = 0

    # counting the amount of different states
    for h in humans:
        if h.status == Status.SUCEPTIBLE:
            suc_s += 1
        if h.status == Status.INFECTED:
            inf_s += 1
        if h.status == Status.RECOVERED:
            rec_s += 1
    suc.append(suc_s)
    inf.append(inf_s)
    qua.append(len(quarantined))
    rec.append(rec_s)
    test.clear()
    test.set_ylim(0, len(humans))
    test.stackplot(steps, inf, qua, rec, suc, colors=[
                   '#df0000', '#ffc637', '#4a4a4a', '#0000df'])

    label1 = 'infected'
    label2 = 'recovered'
    label3 = 'succeptable'
    label4 = 'quarantined'
    p1 = Rectangle((0, 0), 1, 1, fc='#df0000')
    p2 = Rectangle((0, 0), 1, 1, fc='#4a4a4a')
    p3 = Rectangle((0, 0), 1, 1, fc='#0000df')
    p4 = Rectangle((0, 0), 1, 1, fc='#ffc637')
    legend = test.legend([p1, p2, p3, p4], [label1, label2, label3, label4],
                         loc="lower left", bbox_to_anchor=(-0.12, -0.30), ncol=4)


def stack_animation(i, humans, test, time_step, inf, rec, suc, steps, number_of_humans):
    """updates the stackplot every timestep

    Args:
        humans (list): list of all humans in the animated city
        test: plot that gets animated
        time_step (float): timestep in which movement is calculated
        inf (list): list containing the amount of infected humans at all past timestep
        rec (list): list containing the amount of recovered humans at all past timestep
        suc (list): list containing the amount of suceptible humans at all past timestep
        steps (list): list containing all time_steps from the past
        number_of_humans (float): amount of humans in the scenario

    """
    step_counter = len(suc)
    steps.append(time_step*step_counter)
    suc_s = 0
    inf_s = 0
    rec_s = 0

    # counting the amount of different states
    for h in humans:
        if h.status == Status.SUCEPTIBLE:
            suc_s += 1
        if h.status == Status.INFECTED:
            inf_s += 1
        if h.status == Status.RECOVERED:
            rec_s += 1
    suc.append(suc_s)
    inf.append(inf_s)
    rec.append(rec_s)
    test.clear()
    test.set_ylim(0, len(humans))
    test.stackplot(steps, inf, rec, suc, colors=[
                   '#df0000', '#4a4a4a', '#0000df'])

    label1 = 'infected'
    label2 = 'recovered'
    label3 = 'succeptable'
    p1 = Rectangle((0, 0), 1, 1, fc='#df0000')
    p2 = Rectangle((0, 0), 1, 1, fc='#4a4a4a')
    p3 = Rectangle((0, 0), 1, 1, fc='#0000df')
    legend = test.legend([p1, p2, p3], [label1, label2, label3],
                         loc="lower center", bbox_to_anchor=(-0.12, -0.15), ncol=3)


# input functions
def ask_for_input():
    """
    asks for the needed inputs and makes sure they fit the scenario

    Returns:
        prob (float): probability of infection
        infection_radius (float): radius of infection
        number_of_humans (float): number of humans in the scenario (in case of cities for every city)
        temperature (float): influences speed of the humans
    """

    # input for the prob
    while True:
        try:
            prob = float(
                input("Probability of infection (between 0 and 1) (recommended value: 1): "))
            if prob >= 0 and prob <= 1:
                break
            else:
                raise ValueError
        except ValueError:
            print("Please enter a number between 0 and 1. ")

    # input for the infection_radius
    while True:
        try:
            infection_radius = float(input(
                "Infection radius (between 2 and 10) (recommended value: 5, for scenario cities: 10): "))
            if infection_radius >= 2 and infection_radius <= 10:
                break
            else:
                raise ValueError
        except ValueError:
            print("Please enter a number between 2 and 10. ")

    # input for the number_of_humans
    while True:
        try:
            number_of_humans = int(
                input("Number of humans (recommended value: 50, for scenario cities: 15): "))
            if number_of_humans >= 0 and number_of_humans <= 100:
                break
            else:
                raise ValueError
        except ValueError:
            print(
                "Please enter a number a positive number without comma and smaller than 100. ")

    # input for the temperature
    while True:
        try:
            temperature = float(
                input("Temperature (recommended value: 10000): "))
            if temperature >= 0:
                break
            else:
                raise ValueError
        except ValueError:
            print("Please enter a number a positive number. ")

    return prob, infection_radius, number_of_humans, temperature


def ask_for_different_input():
    """
    Asks for more specific input for the simulation that contains vulnerable humans
    and humans that are wearing a face mask. Checks if the user input is correct.

    Returns:
        prob (float): probability of infection for standard humans
        infection_radius (float): infection radius for standard humans
        number_of_humans (float): total number of humans (standard humans + vulnerable humans + humans wearing a face mask)
        temperature (float): influences speed of the humans
        number_vulnerable_humans (int): number of humans that belong to the vulnerable group
        number_humans_with_mask (int): number of humans that are wearing a face mask
    """
    # input for prbability of infection of standard humans
    while True:
        try:
            prob = float(input(
                "Probability of infection for standard humans (between 0 and 1, recommended value: 0.4): "))
            if prob >= 0 and prob <= 1:
                break
            else:
                raise ValueError
        except ValueError:
            print("Please enter a number between 0 and 1. ")

    # input for the infection_radius of standard humans
    while True:
        try:
            infection_radius = float(input(
                "Infection radius for standard humans (between 2 and 7, recommended value: 5): "))
            if infection_radius >= 2 and infection_radius <= 7:
                break
            else:
                raise ValueError
        except ValueError:
            print("Please enter a number between 2 and 7. ")

    # input for total number_of_humans
    while True:
        try:
            number_of_humans = int(
                input("Total number of humans (recommended value: 60): "))
            if number_of_humans >= 0 and number_of_humans <= 100:
                break
            else:
                raise ValueError
        except ValueError:
            print(
                "Please enter a number a positive number without comma and smaller than 100. ")

    # input for the temperature
    while True:
        try:
            temperature = float(
                input("Temperature (recommended value: 10000): "))
            if temperature >= 0:
                break
            else:
                raise ValueError
        except ValueError:
            print("Please enter a number a positive number. ")

    # input for number_vulnerable_humans
    while True:
        try:
            number_vulnerable_humans = int(
                input("Number of vulnerable humans (recommended value: 20): "))
            if number_vulnerable_humans >= 0 and number_vulnerable_humans <= number_of_humans:
                break
            else:
                raise ValueError
        except ValueError:
            print(f"Please enter an integer between 0 and {number_of_humans}.")

    # input for number_humans_with_mask
    while True:
        try:
            number_humans_with_mask = int(
                input("Number of humans that are wearing a face mask (recommended value: 20): "))
            difference = number_of_humans - number_vulnerable_humans
            if number_humans_with_mask >= 0 and number_humans_with_mask <= difference:
                break
            else:
                raise ValueError
        except ValueError:
            print(f"Please enter an interger between 0 and {difference}.")

    return prob, infection_radius, number_of_humans, temperature, number_vulnerable_humans, number_humans_with_mask


def ask_for_even_more_input():
    """
    asks for even more input needed for the simulation

    Returns:
        detection_probability (float): probability an infected human will get quarantined
    """
    while True:
        try:
            detection_probability = float(input(
                "Probability of detecting an infected human (between 0 and 100) (recommended value: 40): "))
            if detection_probability >= 0 and detection_probability <= 100:
                break
            else:
                raise ValueError
        except ValueError:
            print("Please enter a number between 0 and 100. ")
    return detection_probability

