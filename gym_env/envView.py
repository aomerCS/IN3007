from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional, Tuple

import arcade

from spg.view import TopDownView

if TYPE_CHECKING:
    from spg.agent import Agent
    from spg.agent.controller import Command, Controller
    from spg.playground import Playground


class GymGUI(TopDownView):
    def __init__(
            self,
            playground: Playground,
            keyboard_agent: Optional[Agent] = None,
            size: Optional[Tuple[int, int]] = None,
            center: Tuple[float, float] = (0, 0),
            zoom: float = 1,
            display_uid: bool = False,
            draw_transparent: bool = True,
            draw_interactive: bool = True,
            draw_zone: bool = True,
            draw_sensors: bool = False,
            print_rewards: bool = True,
            print_messages: bool = True,
            random_agents: bool = True,
    ) -> None:
        super().__init__(
            playground,
            size,
            center,
            zoom,
            display_uid,
            draw_transparent,
            draw_interactive,
            draw_zone,
        )

        self._playground.window.set_size(*self._size)
        self._playground.window.set_visible(True)

        self._keyboard_agent = keyboard_agent
        self._random_agents = random_agents

        self._agent_commands: Dict[Controller, Command] = {}
        self._message = None

        self.print_rewards = print_rewards
        self.print_messages = print_messages

        self._playground.window.on_draw = self.on_draw
        self._playground.window.on_update = self.on_update
        self._playground.window.on_key_press = self.on_key_press
        self._playground.window.on_key_release = self.on_key_release

        self._draw_sensors = draw_sensors

    def run(self):
        self._playground.window.run()

    def on_draw(self):

        self._playground.window.clear()
        self._fbo.use()
        self.update()

    def on_update(self, _):

        commands = self._get_commands()

        self._playground.step(commands=commands, messages=self._message)

        if self.print_rewards:

            for agent in self._playground.agents:
                if agent.reward != 0:
                    print(agent.reward)

        if self.print_messages:

            for agent in self._playground.agents:
                for comm in agent.communicators:
                    for _, msg in comm.received_messages:
                        print(f"Agent {agent.name} received message {msg}")

        self._message = {}

    def _get_commands(self, commands: Dict[Controller, Command] = {} ):

        command_dict[self._keyboard_agent] = commands

        return command_dict

    def update(self, force=False):

        self.update_sprites(force)

        self._playground.window.use()

        self._playground.window.clear(self._background)

        if self._draw_sensors:

            for agent in self._playground.agents:
                for sensor in agent.sensors:
                    sensor.draw()

        # Change projection to match the contents

        self._transparent_sprites.draw(pixelated=True)
        self._interactive_sprites.draw(pixelated=True)
        self._zone_sprites.draw(pixelated=True)
        self._visible_sprites.draw(pixelated=True)
        self._traversable_sprites.draw(pixelated=True)
