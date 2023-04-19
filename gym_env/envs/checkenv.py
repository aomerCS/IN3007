from gym_env.envs.pertubation_world import PerturbationEnv
from stable_baselines3.common.env_checker import check_env
env = PerturbationEnv()
check_env(env)
