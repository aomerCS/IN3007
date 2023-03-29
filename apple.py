from spg.utils.definitions import CollisionTypes, add_custom_collision
from spg.element import PhysicalElement, RewardElement

# Create a Custom Collision Type
AppleCollisionType = add_custom_collision(CollisionTypes, "APPLE")


# Create Apple Class
class Apple(PhysicalElement, RewardElement):
    def __init__(self, agent):

        super().__init__(
            mass=10,
            #filename=":spg:platformer/items/diamond_blue.png",
            filename="red_apple.png",
            radius=10,
        )

        self.agent = agent.base

    # Every Apple created will use the new custom collision type
    def _set_pm_collision_type(self):
        for pm_shape in self._pm_shapes:
            pm_shape.collision_type = AppleCollisionType.APPLE

    # Sets the reward for agent to receive upon interacting with Apple
    @property
    def _base_reward(self) -> float:
        return 10.0

