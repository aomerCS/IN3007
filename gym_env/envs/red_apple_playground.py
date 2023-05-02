from gym_env.envs.perturbation_world import PerturbationEnv
from resources.apple import Apple
from pathlib import Path
from gym_env.envs.utils import low, high


class RedAppleEnv(PerturbationEnv):
    def __init__(self):
        super().__init__()

        # Create Apples
        red_apples = []
        for i in range(4):
            apple = Apple(
                self.agent,
                filename=Path("../../resources/red_apple.png"),
                reverse=(False, False),
            )
            red_apples.append(apple)

        # Add Apples to Playground
        for apple in red_apples:
            self.playground.add(
                apple,
                (
                    (
                        self.np_random.randint(-high, high),
                        self.np_random.choice(
                            [
                                self.np_random.randint(-high, -low),
                                self.np_random.randint(low, high),
                            ]
                        ),
                    ),
                    0,
                ),
            )
