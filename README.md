# IN3007
## Installation Guide
- Clone the GitHub repository onto local device:
  - https://github.com/aomerCS/IN3007
- Install modules from requirements.txt in the root folder

# Repository Information
- ## resources/
  - This folder contains resources needed for our custom gym environment
  - ### apple.py
    - Custom class that can create an apple within a playground with the ability to manipulate the controls of the colliding body
  - ###create_playground.py
    - Methods to create playgrounds that can be loaded to different python files
  - ### license.txt
    - Contains license information regarding apple pngs
  - ### pixel_apple.png
    - Sprite base for creating apples to be used in playground 
  - ### red_apple.png/blue_apple.png/green_apple.png/black_apple.png
    - Modified sprites based on pixel_apple.png for testing
  - ### reversedForwardBase.py
    - Custom class that allows the reversing of controls from a forwardBase
    - e.g. if a command of 1 is expected, if the criteria is met, reverseForwardBase returns -1 instead 
    - This allows us to deceive a player due to their controls being reversed compared to what is expected
  - ### reversedHeadAgent
    - Custom class that creates an Agent with their first part as the ReversedForwardBase instead of a ForwardBase 
    - This agent is now capable of being manipulated using the ReversedForwardBase, mainly by having their control reversed
- ## gym_env/
  - This folder contains everything related to the machine learning aspects of the project
  - ###init.py
    -  Contains the registration information for our custom gym environment
  - ### envs/
    - This contains the file that creates the custom gym environment
    - #### init.py
      - Needed to create environment
    - #### perturbation_world.py
      - Contains the creation of our custom gym environment, most of the logic is written here
    - #### red_apple_playground.py/black_apple_playground.py/blue_apple_playground.py/green_apple_playground.py/random_apple_playground.py
      - Inherits from perturbation_world, creates a specific playground for training
  - ### results/
    - This contains the files to run our models, as well as any images of the results (screenshots of the environment, graphs of the models performance etc.)
    - #### run_playground.py
      - Test file that allows someone to view a spg playground in real-time
    - ##### red_playground.ipynb/blue_playground.ipynb/green_playground.ipynb/black_playground.ipynb/random_playground.ipynb
      - Jupyter notebook that shows the result of the experiments done using the specific custom environment
      - Display outputs of code blocks as well as showing gifs of models actions
    - ##### models/
      - Stores any models that we create
    - ##### logs/
      - Contains the logs of the models we create
    - ##### gifs/
      - Contains the gifs showing each step of our custom environment

# How to run
- Running any of the jupyter notebooks within IN3007/gym_env/results will show all the results of the experiments (when downloaded, the jupyter notebook should contain the results from already executing the code)

# Tensorboard
- To view the data, first open a terminal and starting from the IN3007 directory, move to gym_envs/results, then run the tensorboard command to open tensorboard locally
- (Commands assume your starting directory is .... -> IN3007 and using Windows / for paths, change to \ in your terminal if running Linux/Mac)
  - cd gym_env/results
  - tensorboard --logdir=logs

# Potential Errors
- Due to the amount of GPU/CPU power that is required to run reinforcement learning policies, the process of running these may take a large amount of time
- The nature of reinforcement learning means that when these are run on your own machine, the models developed won't be identical to the ones in the notebook, however they will be similar enough to confirm that the results are real
- The project was developed on a Windows machine, some errors may occur with directory path problems if using Linux/Mac
  - The pathlib library was used when paths were involved - so it should work without any issues, however the project has not been thoroughly tested with those machines therefore it cannot be guaranteed
  
# MODEL SYSTEM INFO
- OS: Windows-10-10.0.19044-SP0 10.0.19044
- Python: 3.11.2
- Stable-Baselines3: 1.8.0
- PyTorch: 2.0.0+cpu
- GPU Enabled: False
- Numpy: 1.23.5
- Gym: 0.21.0