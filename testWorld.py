import arcade

from spg.agent import HeadAgent
from spg.playground import Playground, Room
from spg.playground.collision_handlers import get_colliding_entities
from spg.utils.definitions import CollisionTypes
from spg.view import HeadAgentGUI

from apple import Apple


def apple_agent_collision(arbiter, _, data):

    playground: Playground = data["playground"]
    (apple, _), (agent, _) = get_colliding_entities(playground, arbiter)

    assert isinstance(apple, Apple)
    assert isinstance(agent, HeadAgent)

    if apple.agent == agent:
        apple.activate(agent)
        #agent.apply_commands({"forward": 0.2})
        #self._agent_commands["forward"] = 0.2
        #agent.activate(apple)

    return True


playground = Room(size=(500, 200), wall_color=arcade.color.AMARANTH_PURPLE)
playground.add_interaction(
    CollisionTypes.GEM, CollisionTypes.GEM, apple_agent_collision
)

agent = HeadAgent()

playground.add(agent)

apple = Apple(agent)
apple.graspable = True
playground.add(apple, ((-200, 60), 0))


gui = HeadAgentGUI(playground, agent)
gui.run()
