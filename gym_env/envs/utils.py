# Checks our policy and returns information about it
from stable_baselines3.common.evaluation import evaluate_policy

# Import reinforcement learning algorithm library
from stable_baselines3 import A2C, DDPG, SAC, TD3, PPO

# Needed for creating new directories
import os
from pathlib import Path

# Preset variables

# Involved in randomly placing apples in the environment
low = 50
high = 100

# Used for all learning
total_timesteps = 50000

# Pathing for model, log and gif directories used throughout project
modelsdir = Path("models")
logsdir = Path("logs")
gifsdir = Path("gifs")

# Setting the names for directories involving these playgrounds
red_apple_playground = "red_apple_playground"
blue_apple_playground = "blue_apple_playground"
green_apple_playground = "green_apple_playground"
black_apple_playground = "black_apple_playground"
all_apple_playground = "all_apple_playground"

# Setting the names for directories involving these models
A2C_V1 = "A2C_V1"
DDPG_V1 = "DDPG_V1"
SAC_V1 = "SAC_V1"
TD3_V1 = "TD3_V1"
PPO_V1 = "PPO_V1"


# Methods


# Agent takes random actions until environment is considered done or time limit is reached
# Environment and the actions of an agent are stored in a gif
def random_actions(env, env_name):
    obs = env.reset()
    done = False
    while not done:
        obs, reward, done, msg = env.step(env.action_space.sample())
        env.render()

        # with observation
        # print(
        #     f"TimeStep: {env.playground.timestep}, Observation: {obs}, Reward: {reward}, Done: {done}, Message: {msg}, Apples: {env.no_of_apples}"
        # )

        # without observation
        print(
            f"TimeStep: {env.playground.timestep}, Reward: {reward}, Done: {done}, Message: {msg}, Apples: {env.no_of_apples}"
        )
    env.save_gif(f"{env_name}_random")


# Creates the directories involved with model/playground
def create_directories(model_name, env_name):
    model_dir = Path(f"{modelsdir}/{model_name}")
    gif_dir = Path(f"{gifsdir}/{model_name}/{env_name}")
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(gif_dir, exist_ok=True)

    return model_name, model_dir


# Runs the training and saves model
def train_learning(model, model_name, model_dir, env_name):
    model.learn(
        total_timesteps=total_timesteps,
        reset_num_timesteps=False,
        tb_log_name=f"{model_name}_{env_name}",
    )
    model.save(Path(f"{model_dir}/{env_name}"))


def train_PPO(env, env_name):
    # Create folders for storing models
    model_name, model_dir = create_directories(PPO_V1, env_name)

    # Train the model
    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logsdir)
    train_learning(model, model_name, model_dir, env_name)

    return model_name, model_dir


def train_A2C(env, env_name):
    # Create folders for storing models
    model_name, model_dir = create_directories(A2C_V1, env_name)

    # Train the model
    model = A2C("MlpPolicy", env, verbose=1, tensorboard_log=logsdir)
    train_learning(model, model_name, model_dir, env_name)

    return model_name, model_dir


def train_DDPG(env, env_name):
    # Create folders for storing models
    model_name, model_dir = create_directories(DDPG_V1, env_name)

    # Train the model
    model = DDPG("MlpPolicy", env, verbose=1, tensorboard_log=logsdir)
    train_learning(model, model_name, model_dir, env_name)

    return model_name, model_dir


def train_SAC(env, env_name):
    # Create folders for storing models
    model_name, model_dir = create_directories(SAC_V1, env_name)

    # Train the model
    model = SAC("MlpPolicy", env, verbose=1, tensorboard_log=logsdir)
    train_learning(model, model_name, model_dir, env_name)

    return model_name, model_dir


def train_TD3(env, env_name):
    # Create folders for storing models
    model_name, model_dir = create_directories(TD3_V1, env_name)

    # Train the model
    model = TD3("MlpPolicy", env, verbose=1, tensorboard_log=logsdir)
    train_learning(model, model_name, model_dir, env_name)

    return model_name, model_dir


# Tests a model in a given environment 10 times
# Stores results in a gif
def testing_model(env, model, model_name, env_name):
    results = []
    for episode in range(1, 10):
        obs = env.reset()
        done = False
        while not done:
            action, _states = model.predict(obs)
            obs, reward, done, msg = env.step(action)
            env.render()
            print(
                f"Episode {episode}, TimeStep: {env.playground.timestep}, Reward: {reward}, Done: {done}, Message: {msg}, Apples: {env.no_of_apples}"
            )
        results.append([episode, env.playground.timestep])
        env.save_gif(f"{model_name}/{env_name}/ep_{episode}")
    print(f"[Episode, Timestep]")
    print(results)

    # Evaluate the agent
    mean_reward, std_reward = evaluate_policy(
        model, model.get_env(), n_eval_episodes=10
    )
    print(f"Mean Reward: {mean_reward}, std_reward: {std_reward}")
