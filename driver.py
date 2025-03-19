import make_commands
from input_commands import enter_commands
import argparse
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # search space and plot options
    parser.add_argument("--centre", type=int, nargs=2, default=(0, 0), help="x z coordinates of the centre of the reward landscape plot; defaults to 0 0")
    parser.add_argument("--radius", type=int, default=10, help="radius of the incircle of the reward landscape plot; defaults to 10")
    parser.add_argument("--height", type=int, default=60, help="height to scale the reward landscape plot to; defaults to 60")
    # hyperparameters for simulated annealing
    parser.add_argument("--iters", type=int, default=100, help="number of simulated annealing timesteps; defaults to 100")
    parser.add_argument("--xy_init", type=int, nargs=2, default=(0, 0), help="initial x and y; defaults to 0 0")
    parser.add_argument("--C", type=float, default=1, help="constant C for the logarithmic \"cooling\" schedule lambda=C(1+t); defaults to 0.01")
    parser.add_argument("--neighbour_size", type=int, default=1, help="incircle radius of square neighbour set. neighbour set is {(x±neighbour_size, y±neighbour_size)}\{(x, y)}; defaults to 1")
    # Minecraft-related options
    parser.add_argument("--minecraft", type=bool, default=False, help="visualise in Minecraft?; defaults to False")
    parser.add_argument("--min_typing_speed", type=float, default=0.001, help="minimum time (in seconds) between successive keystrokes during command input; defaults to 1e-3")
    parser.add_argument("--delay", type=float, default=0.2, help="minimum delay (in seconds) between input of successive commands; defaults to 0.2")
    parser.add_argument("--countdown", type=int, default=10, help="countdown (in seconds) before command entry begins; defaults to 10")
    parser.add_argument("--landscape_block", type=str, default="minecraft:light_gray_concrete", help="block to construct loss landscape with; defaults to minecraft:light_gray_concrete")
    parser.add_argument("--optimiser_block", type=str, default="minecraft:torch", help="block to highlight optimiser path with; defaults to minecraft:torch")

    args = parser.parse_args()

    centre = tuple(args.centre)
    radius = args.radius
    height = args.height
    iters = args.iters
    xy_init = tuple(args.xy_init)
    C = args.C
    neighbour_size = args.neighbour_size
    minecraft = args.minecraft
    min_typing_speed = args.min_typing_speed
    delay = args.delay
    counter_max = args.countdown
    landscape_block = args.landscape_block
    optimiser_block = args.optimiser_block

    if minecraft:
        # to create Minecraft commands to plot the reward landscape:
        make_commands.reward_surface(x_centre=centre[0], y_centre=centre[1], radius=radius, height=height, block=landscape_block)
        # to enter the commands into the Minecraft console, one by one:
        # THIS CAN TAKE SEVERAL HOURS and requires Minecraft to be the active window without interruption:
        enter_commands("reward_surface_commands.txt", min_typing_speed=min_typing_speed, delay=delay, counter_max=counter_max)
        print("Landscape plot complete!")

    # to run simulated annealing and create Minecraft commands to plot the path:
    make_commands.optimiser(iters=iters, x_init=xy_init[0], y_init=xy_init[1], x_centre=centre[0], y_centre=centre[1], C=C, neighbour_size=neighbour_size, radius=radius, height=height, block=optimiser_block)
    
    if minecraft:
        # to enter those commands into the Minecraft console, one by one:
        enter_commands("optimiser_commands.txt", min_typing_speed=min_typing_speed, delay=delay, counter_max=counter_max)
        print("End")