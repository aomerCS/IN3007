from gym_env.envs.pertubation_world import perturbationEnv

from stable_baselines3 import PPO

env = perturbationEnv()
env.reset()

# Examples of action and observation
print("sample action:", env.action_space.sample())

print("observation space shape:", env.observation_space.shape)
print("sample observation:", env.observation_space.sample())

# for step in range(200):
#     env.render()
#     env.step(env.action_space.sample())

# model = PPO("MlpPolicy", env, verbose=1)
# model.learn(total_timesteps=10_000)
#
# vec_env = model.get_env()
# obs = vec_env.reset()
# for i in range(1000):
#     action, _states = model.predict(obs, deterministic=True)
#     obs, reward, done, info = vec_env.step(action)
#     vec_env.render()
#     # VecEnv resets automatically
#     # if done:
#     #   obs = env.reset()

env.close()
