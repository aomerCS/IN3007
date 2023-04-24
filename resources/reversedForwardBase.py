# Assume any code that does not have a line stating it was changed or comment explaining it,
# was taken from the file in the spg library spg/part/parts

from __future__ import annotations

import pymunk
from spg.element import RewardElement

from spg.utils.definitions import ANGULAR_VELOCITY, LINEAR_FORCE
from spg.agent.controller import CenteredContinuousController
from spg.agent.part import PhysicalPart


class ReversedForwardBase(PhysicalPart):
    def __init__(
            self,
            linear_ratio: float = 1,
            angular_ratio: float = 1,
            # reverse_x and reverse_y will determine if the controller commands of the agent is reversed
            reverse_x: bool = False,
            reverse_y: bool = False,
            **kwargs,
    ):
        super().__init__(
            mass=30,
            filename=":spg:puzzle/element/element_blue_square.png",
            sprite_front_is_up=True,
            shape_approximation="decomposition",
            **kwargs,
        )

        self.forward_controller = CenteredContinuousController("forward")
        self.add(self.forward_controller)

        self.angular_vel_controller = CenteredContinuousController("angular")
        self.add(self.angular_vel_controller)

        self.linear_ratio = LINEAR_FORCE * linear_ratio
        self.angular_ratio = ANGULAR_VELOCITY * angular_ratio

        # Reverses the direction of the base
        if reverse_y:
            self.linear_ratio = -self.linear_ratio
        if reverse_x:
            self.angular_ratio = -self.angular_ratio

    def _apply_commands(self, **kwargs):
        command_value = self.forward_controller.command_value

        self._pm_body.apply_force_at_local_point(
            pymunk.Vec2d(command_value, 0) * self.linear_ratio, (0, 0)
        )

        command_value = self.angular_vel_controller.command_value
        self._pm_body.angular_velocity = command_value * self.angular_ratio

    # New function that makes changes after an apple collision
    def activate(self, entity: RewardElement):
        # Reverses the direction of the base
        if entity.reverse_y:
            self.linear_ratio = -self.linear_ratio
        if entity.reverse_x:
            self.angular_ratio = -self.angular_ratio
        # Gives the colliding entity a reward
        agent = self._playground.get_closest_agent(self)
        agent.reward += entity.reward

        # Deletes the entity that the base collided with from the playground
        self._playground.remove(entity)
