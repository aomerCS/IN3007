from gym_env.envs.perturbation_world import PerturbationEnv
from resources.apple import Apple
from pathlib import Path
from gym_env.envs.utils import low, high


class AllAppleEnv(PerturbationEnv):
    def __init__(self):
        super().__init__()

        # Create each type of Apple
        red_apple = Apple(
            self.agent,
            filename=Path("../../resources/red_apple.png"),
            reverse=(False, False),
        )
        blue_apple = Apple(
            self.agent,
            filename=Path("../../resources/blue_apple.png"),
            reverse=(True, False),
        )
        green_apple = Apple(
            self.agent,
            filename=Path("../../resources/green_apple.png"),
            reverse=(False, True),
        )
        black_apple = Apple(
            self.agent,
            filename=Path("../../resources/black_apple.png"),
            reverse=(
                self.np_random.choice([True, False]),
                self.np_random.choice([True, False]),
            ),
        )

        # Stores all Apples into Array
        apples = [red_apple, blue_apple, green_apple, black_apple]

        while len(apples) != 0:
            # Selects a random Apple from the Array and adds Apple to Playground
            apple = self.np_random.choice(apples)
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
            apples.remove(apple)
