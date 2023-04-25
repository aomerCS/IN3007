from gym import spaces
from gym import Env
import numpy as np
from matplotlib import pyplot as plt
from spg.view import TopDownView
from pathlib import Path


class PerturbationEnv(Env):
    """Custom Environment that follows gym interface"""

    def __init__(self, playground):
        super().__init__()
        self.playground = playground
        self.agent = self.playground.agents[0]
        self.playground.time_limit = 1000
        self.gui = TopDownView(self.playground)
        self.episodes = 0
        self.reward = 0
        self.images = []

        # Code for creating action and observation space taken from:
        # https://github.com/gaorkl/spg-experiments/blob/master/spg_experiments/envs/spg/base.py

        # Create action space
        lows = []
        highs = []

        for controller in zip(self.agent.controllers):
            lows.append(controller[0].min)
            highs.append(controller[0].max)

        self.action_space = spaces.Box(
            low=np.array(lows).astype(np.float32),
            high=np.array(highs).astype(np.float32),
            dtype=np.float32,
        )

        # Create observation space
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
            dtype=np.float32,
        )

    def step(self, action):
        # Code for obtaining the controller names was taken from:
        # https://github.com/gaorkl/spg-experiments/blob/master/spg_experiments/envs/spg/base.py

        commands = {}
        command_dict = {}

        for controller, act in zip(self.agent.controllers, action):
            commands[controller.name] = act

        command_dict[self.agent] = commands

        _observation, msg, reward, _done = self.playground.step(commands=command_dict)

        observation = self._get_obs()

        self.reward += reward[self.agent] * 1000
        self.reward -= self.playground.timestep / 100

        if msg is None:
            msg = {}

        # Checks if all apples have been eaten
        done = bool(self.reward == 40.0)

        self.gui.update()

        return observation, self.reward, done, msg

    def render(self, mode="rgb_array"):
        self.images.append(self.gui.get_np_img())
        return None

    def reset(self):
        self.playground.reset()
        observation = self._get_obs()
        self.reward = 0
        self.episodes += 1
        self.images = []
        return observation

    # Additional methods for functionality
    # Code for get and process observation taken from:
    # https://github.com/gaorkl/spg-experiments/blob/master/spg_experiments/envs/spg/base.py

    # Calculate values for sensors on agent and return numpy array
    def _get_obs(self):
        sensor_values = {}
        for sensor in self.agent.sensors:
            sensor_values[sensor.name] = sensor._values
        return self.process_obs(sensor_values)

    # Creates numpy array from values in _get_obs()
    def process_obs(self, obs):
        obs_vec = []
        for _, v in obs.items():
            obs_vec.append(v.ravel())

        return np.concatenate(obs_vec)

    # Saves all images to a file to name.png
    def save_images(self, name):
        plt.imsave(Path(f"pngs/{name}.png"), np.concatenate(self.images))
