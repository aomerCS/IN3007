from gym import spaces
from gym import Env
import numpy as np
from matplotlib import pyplot as plt

from spg.view import GUI, TopDownView
from gym_env.creating_apple_playground import createPlayground
from gym_env.envView import GymGUI


class PerturbationEnv(Env):
    """Custom Environment that follows gym interface"""

    metadata = {"render.modes": ["human", "rgb_array"]}

    def __init__(self):
        super().__init__()
        self.playground = createPlayground()
        self.playground.time_limit = 1000
        self.agent = self.playground.agents[0]
        self.gui = TopDownView(self.playground)
        #self.gui = GUI(self.playground, keyboard_agent=self.agent, random_agents=False)

        self.episodes = 0
        self.reward = 0

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

        commands = {}
        command_dict = {}

        for controller, act in zip(self.agent.controllers, action):
            commands[controller.name] = act

        command_dict[self.agent] = commands

        _observation, msg, reward, _done = self.playground.step(commands=command_dict)

        observation = self._get_obs()

        self.reward += reward[self.agent]

        if msg is None:
            msg = {}

        # Checks if all apples have been eaten, or we have gone past the timelimit
        done = bool(self.reward == 40.0) or bool(self.playground.timestep >= self.playground.time_limit)

        # Determines how the GUI will render (if rendering is occurring)
        # if isinstance(self.gui, GUI):
        #     self.gui.on_draw()
        #     self.gui._agent_commands = command_dict
        # if isinstance(self.gui, TopDownView):
        #     self.gui.update()

        # self.gui.on_draw()
        # self.gui._agent_commands = command_dict

        self.gui.update()

        return observation, self.reward, done, msg

    def render(self, mode="rgb_array"):
        if mode == "human":
            # Displays an arcade window
            #self.gui = GUI(self.playground, keyboard_agent=self.agent, draw_sensors=True, random_agents=False)
            #self.gui = GUI(self.playground, keyboard_agent=None, draw_sensors =True, random_agents=False)
            self.playground.window.run()
        else:
            # Plots numpy array of the playground
            self.gui.draw()
            plt.imsave("test.png", self.gui.get_np_img())
        return self.gui.get_np_img()

    def reset(self):
        # if seed is not None:
        #     super().reset(seed=seed)
        # observation = self.playground.reset()
        # observation = self.fix_obs(observation=observation[0][self.agent])
        self.playground.reset()
        observation = self._get_obs()
        self.episodes += 1
        return observation

    def close(self):
        # Closes the pygame window in case the program is abruptly closed
        self.playground.window.close()

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
