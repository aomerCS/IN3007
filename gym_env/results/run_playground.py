# Playground that shows different apples and the types of collisions
import arcade
from pathlib import Path
import random

from spg.playground import Room
from spg.utils.definitions import CollisionTypes
from spg.element import ColorWall
from spg.view.gui import HeadAgentGUI

# My Custom Entities
from resources.apple import Apple, AppleCollisionType
from resources.reverseHeadAgent import ReverseHeadAgent
from gym_env.envs.perturbation_world import apple_agent_collision

# Initialization of Playground and resources
playground = Room(size=(256, 256), wall_color=arcade.color.AERO_BLUE)
playground.add_interaction(
    AppleCollisionType.APPLE, CollisionTypes.PART, apple_agent_collision
)

# Initialization of agent (can reverse X or Y controls on creation)
agent = ReverseHeadAgent(reverse=(False, False))
playground.add(agent)

# Initialization of walls
wall_1 = ColorWall(
    pos_start=(50, 50), pos_end=(100, 100), width=5, color=arcade.color.AERO_BLUE
)
playground.add(wall_1, ((50, 0), 0))
wall_2 = ColorWall(
    pos_start=(50, 50), pos_end=(100, 100), width=5, color=arcade.color.AERO_BLUE
)
playground.add(wall_2, ((-50, 0), 0))
wall_3 = ColorWall(
    pos_start=(-50, 50), pos_end=(100, 50), width=5, color=arcade.color.AERO_BLUE
)
playground.add(wall_3, wall_3.wall_coordinates)

# redapples have no effect on the agent
red_apple = Apple(
    agent, filename=Path("../../resources/red_apple.png"), reverse=(False, False)
)
playground.add(red_apple, ((-100, -30), 0))
# blueapples invert the x axis
blue_apple = Apple(
    agent, filename=Path("../../resources/blue_apple.png"), reverse=(True, False)
)
playground.add(blue_apple, ((100, 10), 0))
# greenapples invert the y axis
green_apple = Apple(
    agent, filename=Path("../../resources/green_apple.png"), reverse=(False, True)
)
playground.add(green_apple, ((100, 100), 0))
# blackapples randomly invert
blackapple = Apple(
    agent,
    filename=Path("../../resources/black_apple.png"),
    reverse=(random.choice([True, False]), random.choice([True, False])),
)
playground.add(blackapple, ((-100, -100), 0))


# Set up an arcade view and run
gui = HeadAgentGUI(playground, playground.agents[0])
gui.run()
