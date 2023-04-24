# IN3007
## Installation Guide
- Clone the GitHub repository onto local device:
  - https://github.com/aomerCS/IN3007
- Install modules from requirements.txt in the root folder

# Repository Information
- ## Resources
  - This folder contains resources needed for our custom gym environment
  - ### apple.py
    - Custom class that can create an apple within a playground with the ability to manipulate the controls of the colliding body
  - ###create_playground.py
    - Methods to create playgrounds that can be loaded to different python files
  - ### license.txt
    - Contains license information regarding red_apple.png
  - ### red_apple.png
    - Sprite for the Apple class within apple.py
  - ### reversedForwardBase.py
    - Custom class that allows the reversing of controls from a forwardBase
    - e.g. if a command of 1 is expected, if the criteria is met, reverseForwardBase returns -1 instead 
    - This allows us to deceive a player due to their controls being reversed compared to what is expected
  - ### reversedHeadAgent
    - Custom class that creates an Agent with their first part as the ReversedForwardBase instead of a ForwardBase 
    - This agent is now capable of being manipulated using the ReversedForwardBase, mainly by having their control reversed
- ## gym_game
  - This folder contains everything related to the machine learning aspects of the project
  - ###init.py
    -  Contains the registration information for our custom gym environment
  - ### envs
    - This contains the file that creates the custom gym environment
    - #### init.py
      - Needed to create environment
    - #### perturbation_world.py
      - Contains the creation of our custom gym environment, most of the logic is written here
  - ### results
    - This contains the files to run our models, as well as any images of the results (screenshots of the environment, graphs of the models performance etc.)
    - #### result.ipynb
      - Jupyter notebook that shows the result of the experiments done using the custom environment
    - #### run_playground.py
      - Test file that allows someone to view a spg playground in real-time
    - #### models
      - Stores any models that we create
    - #### logs
      - Contains the logs of the models we create
    - #### pngs
      - Contains the images of each step of our custom environment
      - Many steps will occur during testing/training, so the image file will be very long - it is recommended to look at the start and end to determine the progress the model took, however the image will show the entire history of the model if needed

#How to run
- Running IN3007/gym_env/results/result.ipynb will show all the results of the experiments (when downloaded, the jupyter notebook should contain the results from already executing the code)
- In the event that IN3007/gym_env/results/result.ipynb does not run, the code within the jupyter notebook can be copied into a .py file (it is recommended to keep in the same directory under the name results.py) and run

# Tensorboard
- To view the data, first open a terminal and starting from the IN3007 directory, move to gym_envs/results, then run the tensorboard command to open tensorboard locally
- (Commands assume your starting directory is .... -> IN3007)
- cd gym_env/results
- tensorboard --logdir=logs

# Potential Errors
- Due to the amount of GPU/CPU power that is required to run reinforcement learning policies, the process of running these may take a large amount of time
- The nature of reinforcement learning means that when these are run on your own machine, the models developed won't be identical to the ones in the notebook, however they will be similar enough to confirm that the results are real
- The project was developed on a Windows machine, some errors may occur with directory path problems if using Linux/Mac - so it is recommended to run the project using Windows or change the paths when errors occurs (e.g. changing / to \ etc.)