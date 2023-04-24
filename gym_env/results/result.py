import os
import numpy as np
from matplotlib import pyplot as plt

# Custom class imports
from resources.create_playground import createPlayground
from gym_env.envs.pertubation_world import PerturbationEnv

# Create folders for storing models
models_dir = "../models/PPO"
logdir = "logs"

os.makedirs(models_dir, exist_ok=True)
os.makedirs(logdir, exist_ok=True)

# Create playground
playground2 = createPlayground((True, True), [[(-100, 30), (True, True)], [(100, 10), (False, True)], [(100, 100), (False, False)], [(-100, -100), (True, False)]])

# Load and initialize environment
env = PerturbationEnv(playground=playground2)
env.reset()

# Examples of action and observation
# print("sample action:", env.action_space.sample())
#
# print("observation space shape:", env.observation_space.shape)
# print("sample observation:", env.observation_space.sample())

# Testing the environment
# Code taken from: https://stable-baselines3.readthedocs.io/en/master/guide/custom_env.html
# check_env(env)

images = []
for step in range(200):
    img = env.render()
    images.append(img)
    obs, reward, done, msg = env.step(env.action_space.sample())
    print(f"Observation: {obs}, Reward: {reward}, Done: {done}, Message: {msg}")
print(f"Completed in {env.playground.timestep} timesteps!")
plt.imsave("example.png", np.concatenate(images))

# Training the model
# model = PPO("MlpPolicy", env, verbose=1)
# model.learn(total_timesteps=10_000)

# obs = env.reset()
# for i in range(1000):
#     action, _states = model.predict(obs)
#     obs, reward, done, info = env.step(action)
#     env.render("rgb_array")

# vec_env = model.get_env()
# obs = vec_env.reset()
# for i in range(1000):
#     action, _states = model.predict(obs)
#     obs, reward, done, info = vec_env.step(action)
#     vec_env.render("rgb_array")
#     # VecEnv resets automatically
#     # if done:
#     #     obs = env.reset()

# Save model
# model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir)
# TIMESTEPS = 10000
# for i in range(1, 10):
#     model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO")
#     model.save(f"{models_dir}/{TIMESTEPS*i}")

# Load model
# model_path = f"{models_dir}/90000.zip"
# model = PPO.load(model_path, env=env)
#
# episodes = 10
#
# for ep in range(episodes):
#     obs = env.reset()
#     done = False
#     while not done:
#         env.render()
#         action, _states = model.predict(obs)
#         obs, reward, done, info = env.step(action)


env.close()
