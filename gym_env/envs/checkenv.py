from gym_env.envs.pertubation_world import perturbationEnv
from stable_baselines3.common.env_checker import check_env
env = perturbationEnv()
env.reset()
check_env(env)
