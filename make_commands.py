import reward
import numpy as np
import random

def get_min_max_reward(x_centre, y_centre, radius):
    max_reward = 0
    min_reward = np.inf
    for x in range(x_centre-radius, x_centre+radius):
        for y in range (y_centre-radius, y_centre+radius):
            max_reward = max(max_reward, reward.f(x, y))
            min_reward = min(min_reward, reward.f(x, y))
    return min_reward, max_reward

'''
To create Minecraft commands to plot the reward surface on the search space, and store them in reward_landscape_commands.txt
radius is the radius of the incircle of the square search space
height is the height to scale the plot to
1 unit = 1 Minecraft block for all params
'''
def reward_surface(x_centre=0, y_centre=0, radius=10, height=60, block="minecraft:light_gray_concrete"):
    output_file = open("reward_surface_commands.txt", "w")
    min_reward, max_reward = get_min_max_reward(x_centre, y_centre, radius)
    for x in range(x_centre-radius, x_centre+radius): # for all points within the plot boundaries
        for y in range (y_centre-radius, y_centre+radius):
            # scale the reward value to the chosen maximum height and create Minecraft command to plot it:
            output_file.write(f"setblock {int(x)} {int(((reward.f(x, y)-min_reward)*height)/(max_reward-min_reward))-60} {int(y)} {block}\n") # O(n)
        print(f"creating reward surface commands, {((x+1-(x_centre-radius))*100)//(2*radius)}% completed", end="\r")
    print()
    output_file.close()

'''
The simulated annealing implementation.
This function also create Minecraft commands to plot the optimiser steps and stores them in reward_landscape_commands.txt
1 unit = 1 Minecraft block for all params
'''
def optimiser(iters=100, x_init=0, y_init=0, x_centre=0, y_centre=0, C=1, neighbour_size=1, radius=10, height=60, block="minecraft:torch"):
    random.seed(42) # for reproducibility
    output_file = open("optimiser_commands.txt", "w")
    x = x_init # (x,y) is the "current state" of the underlying Markov chain
    y = y_init
    min_reward, max_reward = get_min_max_reward(x_centre, y_centre, radius)
    for t in range(iters):
        lambda_t = C*np.log(1+t) # lambda_n in Sheldon Ross, which makes transitions less likely over time
        # make a Minecraft command to plot the current iteration, computing reward and scaling to fit it on the plot:
        output_file.write(f"setblock {int(x)} {int(((reward.f(x, y)-min_reward)*height)/(max_reward-min_reward))-59} {int(y)} {block}\n")
        print(f"Reward = {reward.f(x, y)} at ({x}, {y}) in iteration {t+1}/{iters}")
        neighbours = set() # all possible (x,y) values in the neighbour set of current (x,y)
        for x_neigh in range(x-neighbour_size, x+neighbour_size+1):
            for y_neigh in range(y-neighbour_size, y+neighbour_size+1):
                if x_centre - radius <= x_neigh <= x_centre + radius and y_centre - radius <= y_neigh <= y_centre + radius: # if the neighbour is in the plot
                    if(not(x_neigh==x and y_neigh==y)): # exclude current point from its neighbour set
                        neighbours.add((x_neigh, y_neigh))
        neighbour = random.choice(list(neighbours)) # choose a random neighbour
        u = random.uniform(0, 1)
        if u < min(1, pow(np.e, lambda_t*reward.f(neighbour[0], neighbour[1]))/pow(np.e, lambda_t*reward.f(x, y))): # neighbour sets are equal size (the unlikely case of a point on the edge of the search space is not considered)
            x = neighbour[0]
            y = neighbour[1]
        
    print()
    output_file.close()