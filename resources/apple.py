# Custom class that can create an apple within a playground
# with the ability to manipulate the controls of the colliding body

from spg.utils.definitions import CollisionTypes, add_custom_collision
from spg.element import PhysicalElement, RewardElement
from pathlib import Path

# Create a Custom Collision Type
AppleCollisionType = add_custom_collision(CollisionTypes, "APPLE")


# Create Apple Class
class Apple(PhysicalElement, RewardElement):
    def __init__(
        self,
        agent,
        # Determines image for apple
        filename: Path = Path("../../resources/red_apple.png"),
        # First tuple value is for x, second tuple is for y
        reverse: (bool, bool) = (
            False,
            False,
        ),
    ):
        super().__init__(
            mass=10,
            filename=filename,
            radius=20,
        )

        self.agent = agent.base
        self.reverse = reverse

    # Every Apple created will use the new custom collision type
    def _set_pm_collision_type(self):
        for pm_shape in self._pm_shapes:
            pm_shape.collision_type = AppleCollisionType.APPLE

    # Sets the reward for agent to receive upon interacting with Apple
    @property
    def _base_reward(self) -> float:
        return 10.0
