from gym_env.envs.perturbation_world import PerturbationEnv
from resources.apple import Apple
from pathlib import Path
from gym_env.envs.utils import low, high


class BlueAppleEnv(PerturbationEnv):
    def __init__(self):
        super().__init__()

        # Create Apples
        blue_apples = []
        for i in range(4):
            apple = Apple(
                self.agent,
                filename=Path("../../resources/blue_apple.png"),
                reverse=(True, False),
            )
            blue_apples.append(apple)

        # Add Apples to Playground
        for apple in blue_apples:
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
