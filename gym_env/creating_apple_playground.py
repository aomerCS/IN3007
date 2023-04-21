# Methods to create playgrounds that can be loaded to different python files

import arcade

from spg.playground import Playground, Room
from spg.playground.collision_handlers import get_colliding_entities
from spg.utils.definitions import CollisionTypes
from spg.element import ColorWall

# My Custom Entities
from entities.apple import Apple, AppleCollisionType
from entities.reversedForwardBase import ReversedForwardBase
from entities.reverseHeadAgent import ReverseHeadAgent


# Created a Custom Collision Handler to confirm when an Apple and Agent collide
def apple_agent_collision(arbiter, _, data):
    playground: Playground = data["playground"]
    (apple, _), (agent, _) = get_colliding_entities(playground, arbiter)

    assert isinstance(apple, Apple)
    assert isinstance(agent, ReversedForwardBase)

    if apple.agent == agent:
        agent.activate(apple)
    return True


def createPlayground():
    # Initialization of Playground and entities
    playground = Room(size=(256, 256), wall_color=arcade.color.AMARANTH_PURPLE)
    playground.add_interaction(
        AppleCollisionType.APPLE, CollisionTypes.PART, apple_agent_collision
    )

    # Initialization of agent (can reverse X or Y controls on creation)
    agent = ReverseHeadAgent(reverse_x=True, reverse_y=False)
    playground.add(agent)

    # Initialization of apple (reversing of X or Y controls for agent will occur to agent on collision)
    apple1 = Apple(agent, reverse_x=False, reverse_y=True)
    playground.add(apple1, ((-100, 30), 0))

    apple2 = Apple(agent, reverse_x=True, reverse_y=False)
    playground.add(apple2, ((100, 10), 0))

    apple3 = Apple(agent, reverse_x=True, reverse_y=True)
    playground.add(apple3, ((100, 100), 0))

    apple4 = Apple(agent, reverse_x=True, reverse_y=True)
    playground.add(apple4, ((-100, -100), 0))

    # Initialization of walls
    wall = ColorWall(
        pos_start=(50, 50), pos_end=(100, 100), width=5, color=arcade.color.AERO_BLUE
    )
    playground.add(wall, ((50, 0), 0))
    wall2 = ColorWall(
        pos_start=(50, 50), pos_end=(100, 100), width=5, color=arcade.color.AERO_BLUE
    )
    playground.add(wall2, ((-50, 0), 0))
    wall3 = ColorWall(
        pos_start=(-50, 50), pos_end=(100, 50), width=5, color=arcade.color.AERO_BLUE
    )
    playground.add(wall3, wall3.wall_coordinates)

    # Our playground is now preset for usage
    return playground
