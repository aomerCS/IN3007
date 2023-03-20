from spg.utils.definitions import CollisionTypes
from spg.element import PhysicalElement, RewardElement


class Apple(PhysicalElement, RewardElement):
    def __init__(self, agent):

        super().__init__(
            mass=10,
            filename=":spg:platformer/items/diamond_blue.png",
            radius=10,
        )

        self.agent = agent

    def _set_pm_collision_type(self):
        for pm_shape in self._pm_shapes:
            pm_shape.collision_type = CollisionTypes.GEM

    @property
    def _base_reward(self) -> float:
        return 10

    def activate(self, entity: RewardElement):

        assert self._playground

        agent = self._playground.get_closest_agent(self)
        agent.reward += entity.reward

        self._playground.remove(entity)

"import add custom coolisions"