# Custom class that creates an Agent with their first part as the ReversedForwardBase instead of a ForwardBase
# This agent is now capable of being manipulated using the ReversedForwardBase, mainly by having their control reversed

# Assume any code that does not have a line stating it was changed or comment explaining it,
# was taken from the file in the spg library spg/agent/agents, specifically the HeadAgent class

from resources.reversedForwardBase import ReversedForwardBase

import math

from spg.agent import Agent
from spg.agent.communicator import Communicator
from spg.agent.part import Head
from spg.agent.sensor import DistanceSensor, RGBSensor


class ReverseHeadAgent(Agent):
    def __init__(self, reverse_x: bool = False, reverse_y: bool = False, **kwargs):
        super().__init__(**kwargs)

        # We want this agent to be capable of reversing, so we give it the new class as its base
        base = ReversedForwardBase(
            linear_ratio=10, reverse_x=reverse_x, reverse_y=reverse_y
        )
        self.add(base)

        self.head = Head(rotation_range=math.pi)
        base.add(self.head)

        # SENSORS
        self.distance = DistanceSensor(
            fov=360,
            resolution=36,
            max_range=100,
            invisible_elements=self._parts,
            normalize=True,
        )
        self.base.add(self.distance)

        # RGBSensor normally returns values from 0-255 following the colour gambit
        # We need change the normalize parameter to true so our observation space can use the values
        self.rgb = RGBSensor(
            fov=180,
            resolution=64,
            max_range=400,
            invisible_elements=self._parts,
            invisible_when_grasped=True,
            normalize=True,
        )
        self.head.add(self.rgb)

        # COMMS
        self.comm = Communicator()
        self.base.add(self.comm)

        # Grapser has been removed due to not having the opportunity
        # to implement to environment
