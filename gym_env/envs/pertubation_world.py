from gym import spaces
from gym import Env
import numpy as np

from spg.view import GUI, TopDownView
from gym_env.creating_apple_playground import createPlayground


class PerturbationEnv(Env):
    """Custom Environment that follows gym interface"""

    metadata = {"render.modes": ["human", "rgb_array"]}

    def __init__(self):
        super().__init__()
        self.playground = createPlayground()
        self.playground.time_limit = 1000
        self.agent = self.playground.agents[0]
        self.gui = None
        #self.gui = GUI(self.playground)
        self.episodes = 0

        self._get_act_space()
        self._get_obs()

    def step(self, action):

        commands = {}
        command_dict = {}

        for controller, act in zip(self.agent.controllers, action):
            commands[controller.name] = act

        command_dict[self.agent] = commands

        observation, msg, reward, done = self.playground.step(commands=command_dict)
        observation = self.fix_obs(observation=observation[self.agent])
        reward = reward[self.agent]

        if msg is None:
            msg = {}

        self.update_render()
        #self.gui.on_draw()

        done = bool(reward == 10.0)

        return observation, reward, done, msg

    def render(self, mode="rgb_array"):
        if mode == "rgb_array":
            self.gui = TopDownView(self.playground)
            self.gui.draw()
        if mode == "human":
            self.gui = GUI(self.playground)
            self.playground.window.run()
        #self.gui.draw()
        return self.gui.get_np_img()

    def reset(self):
        # if seed is not None:
        #     super().reset(seed=seed)
        observation = self.playground.reset()
        observation = self.fix_obs(observation=observation[0][self.agent])
        self.episodes += 1
        return observation

    def close(self):
        # Closes the pygame window in case the program is abruptly closed
        self.playground.window.close()

    # Additional methods for functionality
    # Code for action and observation space inspired from:
    # https://github.com/gaorkl/spg-experiments/blob/master/spg_experiments/envs/spg/base.py

    def _get_act_space(self):
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

    def _get_obs(self):
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

    # Sorts through the tuple, and creates a numpy array with zeros as the values if the observation is None/empty
    def fix_obs(self, observation):
        # Needed for initialization
        if observation is None:
            return np.zeros(shape=self.observation_space.shape)
        else:
            return observation

    def update_render(self):
        if isinstance(self.gui, GUI):
            self.gui.on_draw()
        if isinstance(self.gui, TopDownView):
            self.gui.update()
        return None
