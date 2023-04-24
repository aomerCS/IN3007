# Custom class that can create an apple within a playground
# with the ability to manipulate the controls of the colliding body

from spg.utils.definitions import CollisionTypes, add_custom_collision
from spg.element import PhysicalElement, RewardElement

# Create a Custom Collision Type
AppleCollisionType = add_custom_collision(CollisionTypes, "APPLE")


# Create Apple Class
class Apple(PhysicalElement, RewardElement):
    def __init__(self, agent, reverse_x: bool = False, reverse_y: bool = False):
        super().__init__(
            mass=10,
            filename="../../resources/red_apple.png",
            radius=10,
        )

        self.agent = agent.base
        self.reverse_x = reverse_x
        self.reverse_y = reverse_y

    # Every Apple created will use the new custom collision type
    def _set_pm_collision_type(self):
        for pm_shape in self._pm_shapes:
            pm_shape.collision_type = AppleCollisionType.APPLE

    # Sets the reward for agent to receive upon interacting with Apple
    @property
    def _base_reward(self) -> float:
        return 10.0
