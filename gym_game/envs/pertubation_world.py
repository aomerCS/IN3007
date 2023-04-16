import gymnasium as gym
from gymnasium import spaces
import numpy as np
from apple_playground import playground, agent, apple1, apple2, apple3, apple4, gui


class PerturbationEnv(gym.Env):
    """Custom Environment that follows gym interface"""

    metadata = {"render.modes": ["human", "rgb_array"]}

    def __init__(self):
        # assume actions are float between 1 and -1
        # linear ratio, angular velocity
        self.action_space = spaces.Box(
            low=np.array([-1, -1]),
            high=np.array([1, 1]),
            dtype=np.float64)
        self.observation_space = spaces.Box(
            low=np.zeroes((256,256,3)),
            high=np.full((256,256,3),255),
            shape=(256,256,3)) # (view.height, view.width ,playground.size)
        # spaces.Dict{agent,apple1,apple2,apple3,apple4}
        # create a new view similar to the gui

    def step(self, action):
        observation = playground._compute_observations()
        reward = agent.reward
        done = playground.done

        return observation, reward, done

    def render(self):
        #gui.run()
        #gui.get_np_img()
        return gui.get_np_img()

    def reset(self):
        playground.reset()

        return gui.get_np_img()
