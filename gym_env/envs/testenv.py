import gymnasium as gym
from gym_env.envs.pertubation_world import PerturbationEnv

from stable_baselines3 import PPO

env = PerturbationEnv()
#env = gym.make("gym_env:gym_env/perturbationEnv-v0")

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10_000)

vec_env = model.get_env()
obs = vec_env.reset()
for i in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = vec_env.step(action)
    vec_env.render()
    # VecEnv resets automatically
    # if done:
    #   obs = env.reset()

env.close()
