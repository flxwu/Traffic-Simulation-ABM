import random
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from mesa.visualization.TextVisualization import (
    TextData, TextGrid, TextVisualization
)

from carModel import CarModel

def car_draw(agent):
    '''
    Portrayal Method for canvas
    '''
    r = lambda: random.randint(0,255)
    color = '#%02X%02X%02X' % (r(),r(),r())
    return {"Shape": "rect", "w": 0.5,"h": 40, "Filled": "true", "Layer": 0, "Color": color, "stroke_color": "#00FF00" }

canvas_element = CanvasGrid(car_draw, 100, 100, 500, 500)

model_params = {
    "height": 100,
    "width": 100,
    "dawdle_prob": UserSettableParameter("slider", "Dawdle Probability", 0.1, 0, 1, 0.05),
    "car_amount": UserSettableParameter("slider", "Number of Cars", 10, 1, 100 , 1),
}

server = ModularServer(CarModel,
                       [canvas_element],
                       "Nagel-Schreckenberg", model_params)