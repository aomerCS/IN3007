from gym import spaces
from gym import Env
import numpy as np
from pathlib import Path
from PIL import Image
from gym.utils import seeding
from spg.view import TopDownView

import arcade

from spg.playground import Playground, Room
from spg.playground.collision_handlers import get_colliding_entities
from spg.utils.definitions import CollisionTypes
from spg.element import ColorWall

# My Custom Entities
from resources.apple import Apple, AppleCollisionType
from resources.reversedForwardBase import ReversedForwardBase
from resources.reverseHeadAgent import ReverseHeadAgent


# Created a Custom Collision Handler to confirm when an Apple and Agent collide
def apple_agent_collision(arbiter, _, data):
    playground: Playground = data["playground"]
    (apple, _), (agent, _) = get_colliding_entities(playground, arbiter)

    assert isinstance(apple, Apple)
    assert isinstance(agent, ReversedForwardBase)

    if apple.agent == agent:
        agent.activate(apple)
    return True


class PerturbationEnv(Env):
    def __init__(self):
        super().__init__()

        self.seed()

        # Initialization of playground and interaction
        playground = Room(size=(256, 256), wall_color=arcade.color.AERO_BLUE)
        playground.add_interaction(
            AppleCollisionType.APPLE, CollisionTypes.PART, apple_agent_collision
        )

        # Initialization of agent (can reverse X or Y controls on creation)
        agent = ReverseHeadAgent(reverse=(False, False))
        playground.add(agent)

        # Initialization of walls
        wall_1 = ColorWall(
            pos_start=(50, 50),
            pos_end=(100, 100),
            width=5,
            color=arcade.color.AERO_BLUE,
        )
        playground.add(wall_1, ((50, 0), 0))
        wall_2 = ColorWall(
            pos_start=(50, 50),
            pos_end=(100, 100),
            width=5,
            color=arcade.color.AERO_BLUE,
        )
        playground.add(wall_2, ((-50, 0), 0))
        wall_3 = ColorWall(
            pos_start=(-50, 50),
            pos_end=(100, 50),
            width=5,
            color=arcade.color.AERO_BLUE,
        )
        playground.add(wall_3, wall_3.wall_coordinates)

        self.playground = playground
        self.agent = self.playground.agents[0]
        self.playground.time_limit = 1000
        self.gui = TopDownView(self.playground)
        self.images = []
        self.no_of_apples = self.num_apples()

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

        reward = reward[self.agent]
        reward -= 0.01

        observation = self._get_obs()

        if msg is None:
            msg = {}

        # Checks if all apples have been eaten
        done = bool(self.no_of_apples == 0) or bool(
            self.playground.timestep >= self.playground.time_limit
        )

        self.gui.update()

        self.no_of_apples = self.num_apples()

        return observation, reward, done, msg

    def render(self, mode="rgb_array"):
        im = Image.fromarray(self.gui.get_np_img())
        self.images.append(im)
        return None

    def reset(self):
        self.playground.reset()
        observation = self._get_obs()
        self.images = []
        self.no_of_apples = self.num_apples()
        return observation

    # Additional methods for functionality

    def num_apples(self):
        apples = 0
        for element in self.playground.elements:
            if isinstance(element, Apple):
                apples += 1
        return apples

    # Saves all images to a file to name.png
    def save_gif(self, name):
        im = self.images[0]
        im.save(
            Path(f"gifs/{name}.gif"),
            format="GIF",
            append_images=self.images[1:],
            save_all=True,
            duration=10,
            loop=1,
        )

    # Code for seed taken from:
    # https://github.com/openai/gym/blob/master/gym/envs/box2d/lunar_lander.py
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

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
