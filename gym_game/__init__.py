from gymnasium.envs.registration import register

register(
    id='gym_game/perturbationEnv-v0',
    entry_point='gym_game.envs:perturbationEnv',
    reward_threshold=40,
    nondeterministic=False,
    max_episode_steps=None,
    order_enforce=True,
    autoreset=False
)
