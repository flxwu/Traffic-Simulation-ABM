from random import random

from mesa import Model, Agent
from mesa.datacollection import DataCollector
from mesa.space import SingleGrid
from mesa.time import RandomActivation

class CarModel(Model):

    def __init__(self, height, width, dawdle_prob, car_amount):
        '''
        '''

        super().__init__()
        self.height = height
        self.width = width
        self.dawdle_prob = dawdle_prob
        self.car_amount = car_amount

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(height, width, torus=True)

        self.place_agents()

        self.running = True

    def place_agents(self):
        '''
        Set up agents. We use a grid iterator that returns
        the coordinates of a cell as well as
        its contents. (coord_iter)

        '''
        i = 0
        for x, y, *_ in self.grid.coord_iter():
            if i > self.car_amount:
                break
            agent = CarAgent((x, y), self, 0, 5)
            self.grid.position_agent(agent, (x, y))
            self.schedule.add(agent)
            i+=1

    def step(self):
        '''
        Run one step of the model.
        '''
        agents = self.schedule.agents
        for i,k in zip(agents[0::2], agents[1::2]):
            gap = k.pos[0] - i.pos[0]
            if gap < i.speed:
                i.speed = gap
        self.schedule.step()

class CarAgent(Agent):
    '''
    Car agent
    '''

    def __init__(self, pos, model: CarModel, speed, maxSpeed):
        '''
         Create a new Car agent.

         Args:
            pos: x, y : Agent initial location.
            model: The surrounding world model.
            speed: The car's speed
        '''
        super().__init__(pos, model)
        # set in super() already, but helps the IDE with the type hints.
        self.model = model
        self.pos = pos
        self.speed = speed
        self.maxSpeed = maxSpeed

    def step(self):
        if(self.speed < self.maxSpeed):
            self.speed+=1
        self.move()

    def move(self):
        '''move this agent to an empty cell in `model.grid`. '''
        self.model.grid.move_agent(self,
                                   (self.pos[0]+self.speed, self.pos[1])
                                   )