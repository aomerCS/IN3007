# Import of custom gym.Env
from gym_env.envs.pertubation_world import PerturbationEnv

# Import checker to ensure environment is suitable for StableBaselines usage
from stable_baselines3.common.env_checker import check_env

# Checks our policy and returns information about it
from stable_baselines3.common.evaluation import evaluate_policy

# Import reinforcement learning algorithm library
from stable_baselines3 import A2C, DDPG, HER, SAC, TD3, PPO

# Create playground
from resources.create_playground import createPlayground

playground2 = createPlayground(
    (True, True),
    [
        [(-100, 30), (True, True)],
        [(100, 10), (False, True)],
        [(100, 100), (False, False)],
        [(-100, -100), (True, False)],
    ],
)

# Load and initialize environment
env = PerturbationEnv(playground2)

# Training, saving, and loading

# Create folders for storing models
models_dir = "models/PPO"
logdir = "logs"

# #Save model
# model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir)
# for i in range(1, 30):
#     model.learn(total_timesteps=env.playground.time_limit, reset_num_timesteps=False, tb_log_name="PPO")
#     model.save(f"{models_dir}/{env.playground.time_limit*i}")

# Load model
model_path = f"{models_dir}/9000.zip"
model = PPO.load(path=model_path, env=env)

# # Evaluate the agent
# mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)
# print(f"Mean Reward: {mean_reward}, std_reward: {std_reward}")

results = []
for ep in range(1, 10):
    obs = env.reset()
    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)
        env.render()
    results.append(reward)
    env.save_images(f"PPO_V0_{ep}")
print(results)

env.close()
