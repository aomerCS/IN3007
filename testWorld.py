import arcade

from spg.agent import HeadAgent
from spg.playground import Playground, Room
from spg.playground.collision_handlers import get_colliding_entities
from spg.utils.definitions import CollisionTypes
from spg.view import HeadAgentGUI

from apple import Apple, AppleCollisionType
from spg.agent.part import ForwardBase


# Created a Custom Collision Handler to confirm when an Apple and Agent collide
def apple_agent_collision(arbiter, _, data):

    playground: Playground = data["playground"]
    (apple, _), (agent, _) = get_colliding_entities(playground, arbiter)

    assert isinstance(apple, Apple)
    assert isinstance(agent, ForwardBase)

    if apple.agent == agent:
        print("collision")

    return True


# Initialization of Playground and Entities
playground = Room(size=(500, 200), wall_color=arcade.color.AMARANTH_PURPLE)
playground.add_interaction(
    AppleCollisionType.APPLE, CollisionTypes.PART, apple_agent_collision
)

agent = HeadAgent()

playground.add(agent)

apple = Apple(agent)
apple.graspable = False
playground.add(apple, ((-200, 60), 0))

gui = HeadAgentGUI(playground, agent)
gui.run()
