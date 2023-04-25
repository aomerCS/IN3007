# Methods to create playgrounds that can be loaded to different python files
import random

import arcade

from spg.playground import Playground, Room
from spg.playground.collision_handlers import get_colliding_entities
from spg.utils.definitions import CollisionTypes
from spg.element import ColorWall

# My Custom Entities
from resources.apple import Apple, AppleCollisionType
from resources.reversedForwardBase import ReversedForwardBase
from resources.reverseHeadAgent import ReverseHeadAgent


# Created a Custom Collision Handler to confirm when an Apple and Agent collide
def apple_agent_collision(arbiter, _, data):
    playground: Playground = data["playground"]
    (apple, _), (agent, _) = get_colliding_entities(playground, arbiter)

    assert isinstance(apple, Apple)
    assert isinstance(agent, ReversedForwardBase)

    if apple.agent == agent:
        agent.activate(apple)
    return True


# Creates our base playground with an agent and the walls we want to use for all tests
# The parameters allow us to decide if our agent will have normal controls, or if they will be modified
# We can also add any number of apples using a list - inside this list will contain n number of lists for n apples
# Each apple must have two tuples inside
# The first tuple will indicate its position within the playground (pos_x, pos_y)
# The second determines the effects it will have upon colliding with an agent (reverse_x, reverse_y)
def createPlayground(agent_reverse: tuple = (), apples: list[list[tuple]] = [[(), ()]]):
    # Initialization of Playground and resources
    playground = Room(size=(256, 256), wall_color=arcade.color.AO)
    playground.add_interaction(
        AppleCollisionType.APPLE, CollisionTypes.PART, apple_agent_collision
    )

    # Initialization of agent (can reverse X or Y controls on creation)
    agent = ReverseHeadAgent(reverse_x=agent_reverse[0], reverse_y=agent_reverse[-1])
    playground.add(agent)

    for info in apples:
        apple = Apple(agent, reverse_x=info[1][0], reverse_y=info[1][-1])
        playground.add(apple, (info[0], 0))

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
