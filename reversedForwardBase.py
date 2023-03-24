from __future__ import annotations

import numpy as np
import pymunk
from spg.element import RewardElement

from spg.utils.definitions import ANGULAR_VELOCITY, LINEAR_FORCE
from spg.agent.controller import CenteredContinuousController
from spg.agent.part import AnchoredPart, PhysicalPart


class ReversedForwardBase(PhysicalPart):
    def __init__(
            self,
            linear_ratio: float = 1,
            angular_ratio: float = 1,
            reverse_value: bool = False,
            **kwargs,
    ):
        super().__init__(
            mass=30,
            filename=":spg:puzzle/element/element_blue_square.png",
            sprite_front_is_up=True,
            shape_approximation="decomposition",
            **kwargs,
        )

        self.reverse = reverse_value
        self.forward_controller = CenteredContinuousController("forward")
        self.add(self.forward_controller)

        self.angular_vel_controller = CenteredContinuousController("angular")
        self.add(self.angular_vel_controller)

        if self.reverse:
            self.linear_ratio = -LINEAR_FORCE * linear_ratio
            self.angular_ratio = -ANGULAR_VELOCITY * angular_ratio
        else:
            self.linear_ratio = LINEAR_FORCE * linear_ratio
            self.angular_ratio = ANGULAR_VELOCITY * angular_ratio

    def _apply_commands(self, **kwargs):

        command_value = self.forward_controller.command_value

        self._pm_body.apply_force_at_local_point(
            pymunk.Vec2d(command_value, 0) * self.linear_ratio, (0, 0)
        )

        command_value = self.angular_vel_controller.command_value
        self._pm_body.angular_velocity = command_value * self.angular_ratio

    def activate(self, entity: RewardElement):

        self.reverse = not self.reverse

        if self.reverse:
            self.linear_ratio = -LINEAR_FORCE * self.linear_ratio
            self.angular_ratio = -ANGULAR_VELOCITY * self.angular_ratio
        else:
            self.linear_ratio = LINEAR_FORCE * self.linear_ratio
            self.angular_ratio = ANGULAR_VELOCITY * self.angular_ratio

        self._playground.remove(entity)
