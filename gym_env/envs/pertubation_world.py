from gym import spaces
from gym import Env
import numpy as np

from spg.view import GUI
from spg.agent.controller import ContinuousController
from gym_env.creating_apple_playground import createPlayground


class perturbationEnv(Env):
    """Custom Environment that follows gym interface"""

    metadata = {"render.modes": ["human", "rgb_array"]}

    def __init__(self):
        super().__init__()
        self.playground = createPlayground()
        self.playground.time_limit = 1000
        self.agent = self.playground.agents[0]
        self.gui = GUI(self.playground, self.agent)
        #self.gui = TopDownView(self.playground)
        self.episodes = 0

        # Set the action space
        self._set_action_space()

        # Create observation space
        self._get_obs()

    def step(self, action):

        commands = {}
        command_dict = {}

        for actuator, act in zip(self.agent.controllers, action):
            commands[actuator] = act

        command_dict[self.agent] = commands

        observation, msg, reward, done = self.playground.step()
        #observation, msg, reward, done = self.playground.step(commands=command_dict)
        observation = observation[self.agent]
        reward = reward[self.agent]

        # Needed for initialization
        if observation is None:
            observation = np.zeros(shape=self.observation_space.shape)
        if msg is None:
            msg = {}

        return observation, reward, done, msg

    def render(self, mode="human"):
        #gui.run()
        #view.get_np_img()
        return self.gui.get_np_img()

    def reset(self):
        # if seed is not None:
        #     super().reset(seed=seed)
        self.playground.reset()
        return np.zeros(shape=self.observation_space.shape)

    def _set_action_space(self):

        lows = []
        highs = []

        for controller in zip(self.agent.controllers):
            lows.append(controller[0].min)
            highs.append(controller[0].max)
            # else:
            #     lows.append(controller[0].command_value[0])
            #     highs.append(controller[0].command_value[-1])

        self.action_space = spaces.Box(
            low=np.array(lows).astype(np.float32),
            high=np.array(highs).astype(np.float32),
            dtype=np.float32,
        )

        # CenteredContinuousController actions are value between 1 and -1
        # First value is for linear control, second is for angular control, third is for head
        # self.action_space = spaces.Box(
        #     low=-1,
        #     high=1,
        #     shape=(len(self.agent.controllers),),
        #     dtype=np.float32,
        # )

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

    def close(self):
        self.playground.window.close()
