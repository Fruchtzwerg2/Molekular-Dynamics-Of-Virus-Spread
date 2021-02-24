# Molekular-Dynamics-Of-Virus-Spread
Uni project to simulate a pandemic using ideal gas laws

# The idea

The idea behind the structure of code was to create a notebook containing only the neccesary code fragments to run the simulation and to hide all other code in seperate files. The structure is as follows: human.py consists of the class human, init.py contains the code to generate a list of humans for a simulation, simulation.py allows to calculate the interaction between the humans moving around, scenarios_main.py sets all the different scenarios up. 

# Usage

## Installation

This project requires Python 3.8 or later.

After cloning the repository to your machine install the requirements using _pip_:

```bash
pip install -r requirements.txt
```

After that you can interact with the application using the provided Juypter Notebook.
Keep in mind that _Jupyter_ is also required to be installed separately.

## Working from the console

You can also import the application from the console by starting the interactive python prompt and running the following code for importing:

```python
import src.scenarios as s
```

After that you can choose to run the available scenarios like:

```python
s.scenario_quarantine(show=True)
```

The option *show = True* is essential here as it tells the application to open the _matplotlib_ window instead of rendering it in the notebook.

## Working from the Juypter Notebook

The notebook is designed to be as user friendly as possible. Therefore it conntains only a minimmum of code. Before starting one of the scenarios the first code fell needs to be carried out in order to load all the required files. Then the chosen scenario can be started by running the matching cell. In each scenario the user will be asked to enter some constants to influence the simulation.

Several different simulations can de done after another, only restarting a simmulation that was performed by the computer is not possible. To do that the kernel needs a restart.

Contrary to working from the console you must not the *show = True* here as the default behaviour of the application is to render to the Jupyter Notebook anyways.

# Scenarios
The program is able to simulate different scenarios. Each one focuses on a different aspect of the virus spread.
Each sceanrio contains at least an area of simulation showing the moving humans and a stackplot plotting the amount of humans in each healthstate.

## Basic

This scenario contains the required minimum, so it only simmulates humans moving around and changing direction due to the potential. While moving humans getting too close to an infected human will be infected themselves. It basically reasembles the spread of a virus when nobody is aware of it and none actions against the spread are performed.
Before running the simulation the user is required to choose a probbability of infection as well as the number of humans in the simulation and a temperature which influcences the speed of the humans

## Random Walk

This scenario is very similar to the basic simulation, it only differs in one detail: here the humans change direction and speed due to chance in contrast to the potential in the basic scenario.

## Cities

This scenario simulates the spread of the virus in different places which are connected only by humans travelling. The simulaation consists of three different cities, only one will have an infected human in the beginning. After a certain time period a human from each city is chosen randomly and transported to another city. The paramters thaat need to be chosen are identical to the ones from the scenarios above, only in this case the number of humans refers to only one city.

Watching the simulation several times gives a great idea on how a virus can spread over the whole world or just stay locally. In some cases the virus will affect all cities and in other cases the virus will stay in only one citie an die out pretty quickly.

## Face mask and vulnerable group

This scenario aims to imitate real life. Two completely different groups are introduced: The first one consists of humans that are wearing a face mask, which is just protecting the person wearing it. Therefore they have a smaller chance of getting infected as their infection radius and infection probability is roughly halved (about 45% smaller in comparison to the standard group). They are assigend the lighter colors in the stack plot. 
The second group should represent more vulnerable humans (elderly people, people with a weak immune system, ...). Their risk of getting infected and their infection radius is nearly doubled (about 190% higher compared to standard humans). In the stack plot they are represented by the darker shades. 

A gaussian distribution is used to make the infection radius and the infection probability completely different for every person. 

While running the simulation, one can see that sometimes a human does not get infect by another one despite them sticking together (as he/she is wearing a face mask). Whereas other times a person gets infected even though social-distancing (as he/she belongs to the vulnerable group). 

## Quarantine

Upon start of the simulation the user can (alongside the default parameters) choose a probability for a infected person to be detected and sent into quarantine.
Based on this probability, every timestep all humans are "tested" and if found to be infected, are sent to quarantine where they stay until they recover.
The result of this is that often times the curve of infected people is lowered dramatically and a lot more people stay susceptible / healthy until the end.
This proves that widespread and especially early testing is an effective measure for fighting a pandemic.
