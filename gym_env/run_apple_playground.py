# Simple environment showcasing the apple agent collision

from spg.view import HeadAgentGUI
from gym_env.creating_apple_playground import createPlayground

pg = createPlayground()
gui = HeadAgentGUI(pg, pg.agents[0])
gui.run()

# Code that if all apples are eaten, a super apple with 100 reward will spawn in the center
