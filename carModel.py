from random import random

from mesa import Model, Agent
from mesa.space import SingleGrid
from mesa.time import BaseScheduler


class CarModel(Model):
    '''
    Model class for the Nagel-Schreckenberg Car model.
    '''

    def __init__(self, height, width, dawdle_prob, car_amount):
        '''
        '''

        super().__init__()
        self.height = height
        self.width = width
        self.dawdle_prob = dawdle_prob
        self.car_amount = car_amount

        self.schedule = BaseScheduler(self)
        self.grid = SingleGrid(height, width, torus=True)

        self.place_agents()

        self.running = True

    def place_agents(self):
        for i in range(self.car_amount):
            while True:
                try:
                    r = random()
                    agent = CarAgent((int(r*100), 5), self, 10)
                    self.grid.position_agent(agent, int(r*100), 5)
                    self.schedule.add(agent)
                    break
                except Exception:
                    continue

    def step(self):
        self.schedule.step()


class CarAgent(Agent):
    '''
    Car agent
    '''

    def __init__(self, pos, model: CarModel, max_speed):
        '''
         Create a new Car agent.

         Args:
            pos: x, y : Agent initial location.
            model: The surrounding world model.
            max_speed: Car's speed threshold
        '''
        super().__init__(pos, model)
        # set in super() already, but helps the IDE with the type hints.
        self.model = model
        self.pos = pos
        self.max_speed = max_speed
        self.speed = 1

    def step(self):
        '''
        A single step
        - evaluate all parameters to adjust speed and whether to move or not
        '''
        if self.speed < self.max_speed:
            self.speed += 1

        tmpX = self.pos[0] + 1
        while True:
            if not self.model.grid.is_cell_empty(self.model.grid.torus_adj((tmpX, self.pos[1]))):
                break
            tmpX += 1
        if tmpX - self.pos[0] < self.speed:
            self.speed = tmpX - self.pos[0]

        if random() < self.model.dawdle_prob:
            self.speed -= 1
        self.move()

    def move(self):
        '''
        Actual move method
        - only move if the cell the agent's going to be moved to is empty
        '''
        if self.model.grid.is_cell_empty(self.model.grid.torus_adj((self.pos[0]+self.speed, self.pos[1]))):
            self.model.grid.move_agent(self,
                                       self.model.grid.torus_adj(
                                           (self.pos[0]+self.speed, self.pos[1]))
                                       )
