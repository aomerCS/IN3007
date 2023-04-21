# Assume any code that does not have a line stating it was changed, was taken from the file in the spg library spg/agent/agents

from entities.reversedForwardBase import ReversedForwardBase

import math

from spg.agent import Agent
from spg.agent.communicator import Communicator
from spg.agent.interactor import GraspHold
from spg.agent.part import Head
from spg.agent.sensor import DistanceSensor, RGBSensor


class ReverseHeadAgent(Agent):
    def __init__(self, reverse_x: bool = False, reverse_y: bool = False, **kwargs):
        super().__init__(**kwargs)

        # This is the only line changed from the HeadAgent class
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

        self.rgb = RGBSensor(
            fov=180,
            resolution=64,
            max_range=400,
            invisible_elements=self._parts,
            invisible_when_grasped=True,
        )
        self.head.add(self.rgb)

        # COMMS
        self.comm = Communicator()
        self.base.add(self.comm)

        # Grapser has been removed due to it not being needed for this project
