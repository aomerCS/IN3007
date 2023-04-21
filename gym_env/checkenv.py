# Code taken from: https://stable-baselines3.readthedocs.io/en/master/guide/custom_env.html

from gym_env.envs.pertubation_world import perturbationEnv
from stable_baselines3.common.env_checker import check_env
env = perturbationEnv()
check_env(env)
