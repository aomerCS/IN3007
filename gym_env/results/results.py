# Import of custom gym.Env
from gym_env.envs.perturbation_world import PerturbationEnv

# Import checker to ensure environment is suitable for StableBaselines usage
from stable_baselines3.common.env_checker import check_env

# Checks our policy and returns information about it
from stable_baselines3.common.evaluation import evaluate_policy

# Import reinforcement learning algorithm library
from stable_baselines3 import A2C, DDPG, HER, SAC, TD3, PPO

# Needed for creating new directories
import os
from pathlib import Path

# Create playground
from resources.create_playground import createPlayground

# Simplest playground, no perturbation
playground1 = createPlayground(
    (True, True),
    [
        [(-100, 30), (True, True)],
        [(100, 10), (False, True)],
        [(100, 100), (False, False)],
        [(-100, -100), (True, False)],
    ],
)

# Load and initialize environment
env = PerturbationEnv(playground1)
check_env(env)

# Training, saving, and loading

# Create folders for storing models
models_dir = Path("models/PPO_V1")
logdir = Path("logs")

os.makedirs(models_dir, exist_ok=True)
os.makedirs(logdir, exist_ok=True)

# #Save model
# model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir)
# for i in range(1, 100):
#     model.learn(total_timesteps=env.playground.time_limit, reset_num_timesteps=False, tb_log_name="PPO_V1")
#     model.save(Path(f"{models_dir}/{env.playground.time_limit*i}"))
# del model

# Load model
model_path = Path(f"{models_dir}/9000.zip")
model = PPO.load(path=model_path, env=env, print_system_info=True)

# results = []
# for episode in range(1, 10):
#     obs = env.reset()
#     done = False
#     while not done:
#         if env.playground.timestep >= env.playground.time_limit:
#             done = True
#             break
#         else:
#             action, _states = model.predict(obs)
#             obs, reward, done, info = env.step(action)
#             env.render()
#         print(f"Test {episode}, current timestep: {env.playground.timestep} Reward: {reward}, Done: {done}")
#     results.append([env.playground.timestep, reward, done])
#     env.save_images(f"PPO_V0_{episode}")
# print(f"[Timestep, Reward, Done]")
# print(results)

env.close()
