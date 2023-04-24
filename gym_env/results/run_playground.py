# Simple environment showcasing the apple agent collision
from gym_env.results.result import playground2
from spg.view import HeadAgentGUI

# #gui = HeadAgentGUI(playground=playground1, keyboard_agent=playground1.agents[0], random_agents=False)
gui = HeadAgentGUI(playground2, playground2.agents[0])
gui.run()

# Code that if all apples are eaten, a super apple with 100 reward will spawn in the center
