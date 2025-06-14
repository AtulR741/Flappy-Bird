# Flappy-Bird
I have designed an RL model for the classic flappy bird game which I have made using pygame, a library in python. This model makes use of the position of pipe along with the current velocity of the bird, without using any convolutional layer.

Following files can be identified in the repository:
1. game.py - main game file
2. play.py - run this file if you want to play the game
3. model.py - the main model
4. agent.py - the RL agent, open this file to train/test your model

The following things are included in the state passed to the agent to train/test:
1. relative position of the gap between the next pair of pipes
2. velocity of the bird along the y-axis

The following reward system was used:
1. A reward of +0.5 if the bird aligns along the y-axis with the gap between the next pair of pipes.
2. A reward of -1 if the bird crashes with any pipe
3. A reward of -2 if the bird crashes with the top/bottom of the screen
4. A reward of 0 otherwise
![image](https://github.com/user-attachments/assets/2aa7bf6c-5b4d-48a2-95b4-e74ca2ce959b)
