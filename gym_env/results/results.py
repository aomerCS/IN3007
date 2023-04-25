# Import of custom gym.Env
import random

from gym_env.envs.perturbation_world import PerturbationEnv

# Import checker to ensure environment is suitable for StableBaselines usage
from stable_baselines3.common.env_checker import check_env

# Checks our policy and returns information about it
from stable_baselines3.common.evaluation import evaluate_policy

# Import reinforcement learning algorithm library
from stable_baselines3 import A2C, DDPG, SAC, TD3, PPO

# Needed for creating new directories
import os
from pathlib import Path

# Create playground
from resources.create_playground import createPlayground

# randInt = (random.getrandbits(1))
# randBool = bool(randInt)

# Simplest playground, no perturbation
playground1 = createPlayground(
    (False, False),
    [
        [(-100, 30), (False, False)],
        [(100, 10), (False, False)],
        [(100, 100), (False, False)],
        [(-100, -100), (False, False)],
    ],
)

# Load and initialize environment
env = PerturbationEnv(playground1)
# check_env(env)

# Training a model, and saving the model
# PPO Version 1 will be our base case

# Create folders for storing models
model_name = "PPO_V5"
models_dir = Path(f"models/{model_name}")
logdir = Path("logs")
img_dir = Path(f"pngs/{model_name}")

os.makedirs(models_dir, exist_ok=True)
os.makedirs(img_dir, exist_ok=True)
os.makedirs(logdir, exist_ok=True)

# We split the training per 1000 timesteps (our playgrounds timelimit) so that we can choose the best point of time to load the model from
total = 100000
model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    gamma=0.4,
    n_epochs=4,
    clip_range=0.2,
    normalize_advantage=True,
    ent_coef=0.9,
    vf_coef=0.5,
    tensorboard_log=logdir,
)
model.learn(
    total_timesteps=total,
    reset_num_timesteps=False,
    tb_log_name=model_name,
)
model.save(Path(f"{models_dir}/{total}"))

# for i in range(1, 10):
#     model.learn(
#         total_timesteps=999999,
#         reset_num_timesteps=False,
#         tb_log_name=model_name,
#     )
#     model.save(Path(f"{models_dir}/{env.playground.time_limit*i}"))
#     print(str(Path(f"{models_dir}/{env.playground.time_limit*i}")) + " saved")
# del model

# Load the trained model that looks the best on Tensorboard graph
model_path = Path(f"{models_dir}/{total}.zip")
model = PPO.load(path=model_path, env=env, print_system_info=True)

# Testing the model

results = []
for episode in range(1, 10):
    obs = env.reset()
    done = False
    while not done:
        if env.playground.timestep >= env.playground.time_limit:
            done = True
        else:
            action, _states = model.predict(obs)
            obs, reward, done, info = env.step(action)
            env.render()
        print(
            f"Test {episode}, current timestep: {env.playground.timestep} Reward: {reward}, Done: {done}"
        )
    results.append([env.playground.timestep, reward, done])
    env.save_images(f"{model_name}/ep_{episode}")
print(f"[Timestep, Reward, Done]")
print(results)

env.close()
