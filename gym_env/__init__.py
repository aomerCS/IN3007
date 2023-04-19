from gymnasium.envs.registration import register

register(
    id='gym_env/perturbationEnv-v0',
    entry_point='gym_env.envs:perturbationEnv',
    reward_threshold=40,
    nondeterministic=False,
    max_episode_steps=None,
    order_enforce=True,
    autoreset=False
)
