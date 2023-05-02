from gym_env.envs.perturbation_world import PerturbationEnv
from resources.apple import Apple
from pathlib import Path
from gym_env.envs.utils import low, high


class BlackAppleEnv(PerturbationEnv):
    def __init__(self):
        super().__init__()

        # Create Apples
        black_apples = []
        for i in range(4):
            apple = Apple(
                self.agent,
                filename=Path("../../resources/black_apple.png"),
                reverse=(
                    self.np_random.choice([True, False]),
                    self.np_random.choice([True, False]),
                ),
            )
            black_apples.append(apple)

        # Add Apples to Playground
        for apple in black_apples:
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
