import gymnasium as gym
from gymnasium import spaces
import numpy as np
from spg.view import GUI
from gym_env.envs.apple_playground import createPlayground


class PerturbationEnv(gym.Env):
    """Custom Environment that follows gym interface"""

    metadata = {"render.modes": ["human", "rgb_array"]}

    def __init__(self):
        self.playground = createPlayground()
        self.agent = self.playground.agents[0]

        self.gui = GUI(self.playground, self.agent)
        #self.agent.cls(controller.External())

        # CenteredContinuousController actions are value between 1 and -1
        # First value is for linear control, second is for angular control
        self.action_space = spaces.Box(
            low=np.array([-1, -1]),
            high=np.array([1, 1]),
            dtype=np.float64)

        # Code for observation space taken from: https://github.com/gaorkl/spg-experiments/blob/master/spg_experiments/envs/spg/base.py
        # d = {}
        # for sensor in self.agent.sensors:
        #     if isinstance(sensor.shape, int):
        #         shape = (sensor.shape, 1)
        #     else:
        #         shape = sensor.shape
        #
        #     d[sensor.name] = spaces.Box(
        #         low=0,
        #         high=1,
        #         shape=shape,
        #         dtype=np.float64,
        #     )
        #
        # self.observation_space = spaces.Dict(d)

        self.observation_space = spaces.Box(
            low=np.zeros((256,256,3)),
            high=np.full((256,256,3),255),
            shape=(256,256,3))

        #np.zeros (playground.size,3)
        # (view.height, view.width ,playground.size)
        # spaces.Dict{agent,apple1,apple2,apple3,apple4}
        # create a new view similar to the gui


    def step(self, action):
        self.agent.base.setForwardController(action[0])
        self.agent.base.setForwardController(action[1])
        observation, msg, reward, terminated = self.playground.step()

        return observation, reward, terminated, msg

    def render(self):
        #gui.run()
        #view.get_np_img()
        return self.gui.get_np_img()

    def reset(self):
        observation = self.playground.reset()

        return observation

    def close(self):
        self.gui.playground.window.close()
