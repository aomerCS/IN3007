# Simple environment showcasing the apple agent collision
from resources.create_playground import createPlayground
from spg.view import HeadAgentGUI

# Simplest playground, no perturbation
playground = createPlayground(
    (False, False),
    [
        [(-100, 30), (False, False)],
        [(100, 10), (False, False)],
        [(100, 100), (False, False)],
        [(-100, -100), (False, False)],
    ],
)

gui = HeadAgentGUI(playground, playground.agents[0], random_agents=False)
gui.run()
