from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid
from SimpleContinuousModule import SimpleCanvas

from mesa.visualization.TextVisualization import (
    TextData, TextGrid, TextVisualization
)

from carModel import CarModel

def car_draw(agent):
    return {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0, "Color" : ["#FF0000", "#FF9999"], "stroke_color": "#00FF00"}

# canvas_element = SimpleCanvas(car_draw, 500, 850)
canvas_element = CanvasGrid(car_draw, 500, 500)

model_params = {
    "height": 500,
    "width": 500,
    "dawdle_prob": UserSettableParameter("slider", "Dawdle Probability", 10, 0, 100, 5),
    "car_amount": UserSettableParameter("slider", "Number of Cars", 10, 1, 100 , 5),	
}

server = ModularServer(CarModel,
                       [canvas_element],
                       "Nagel-Schreckenberg", model_params)
