import gymnasium as gym
from gym import spaces
from gym import Env
import numpy as np
from spg.view import GUI
from gym_env.envs.apple_playground import createPlayground


class perturbationEnv(Env):
    """Custom Environment that follows gym interface"""

    metadata = {"render.modes": ["human", "rgb_array"]}

    def __init__(self):
        super().__init__()
        self.playground = createPlayground()
        self.playground.time_limit = 1000
        self.agent = self.playground.agents[0]
        #self.gui = GUI(self.playground, self.agent)
        self.episodes = 0

        #self.agent.cls(controller.External())

        # CenteredContinuousController actions are value between 1 and -1
        # First value is for linear control, second is for angular control, third is for head
        self.action_space = spaces.Box(
            low=-1,
            high=1,
            shape=(len(self.agent.controllers),),
            dtype=np.float32,
        )

        # Create observation space
        self._get_obs()

    def step(self, action):

        actions_to_game_engine = {}
        actions_dict = {}

        for actuator, act in zip(self.agent.controllers, action):
            actions_dict[actuator] = act

        actions_to_game_engine[self.agent] = actions_dict

        observation, msg, reward, done = self.playground.step()
        #observation, msg, reward, done = self.playground.step(commands=actions_to_game_engine)
        observation = observation[self.agent]
        reward = reward[self.agent]

        # Needed for initialization
        if observation is None:
            observation = np.zeros(shape=self.observation_space.shape)
        if msg is None:
            msg = {}

        return observation, reward, done, msg

    # def render(self, mode):
    #     #gui.run()
    #     #view.get_np_img()
    #     return self.gui.get_np_img()

    def reset(self):
        # if seed is not None:
        #     super().reset(seed=seed)
        self.playground.reset()
        return np.zeros(shape=self.observation_space.shape)

    def _get_obs(self):
        # Code for observation space taken from: https://github.com/gaorkl/spg-experiments/blob/master/spg_experiments/envs/spg/base.py
        elems = 0
        for sensor in self.agent.sensors:
            if isinstance(sensor.shape, int):
                elems += sensor.shape
            else:
                elems += np.prod(sensor.shape)

        self.observation_space = spaces.Box(
            low=0,
            high=1,
            shape=(elems,),
            dtype=np.float64,
        )

        # self.observation_space = spaces.Box(
        #     low=np.zeros((self.playground.size[0], self.playground.size[1], 3)),
        #     high=np.full((self.playground.size[0], self.playground.size[1], 3), 255),
        #     shape=(self.playground.size[0], self.playground.size[1], 3))

        # np.zeros (playground.size,3)
        # (view.height, view.width ,playground.size)
        # spaces.Dict{agent,apple1,apple2,apple3,apple4}
        # create a new view similar to the gui

    #def close(self):
        #self.gui.playground.window.close()
