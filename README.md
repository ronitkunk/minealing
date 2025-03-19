# DoubleVanilla

## Introduction
Run simulated annealing on a bivariate reward function, and optionally visualise in the video game Minecraft.

![banner](data/banner.png "Simulated Annealing")

## Instructions
* Navigate to this directory
* Install the python packages `numpy` and `pynput`. You can get them from PyPI using:
```sh
pip install -r requirements.txt
```
* Create a reward function to be maximised in `reward.py`, or keep the default (see the Theory section below).
* To see a list of possible optional arguments and values, use:
```sh
python driver.py --help
```
* Run `driver.py`, specifying suitable optional arguments. By default, visualisation in Minecraft is turned off.
```sh
python driver.py [ARGS]
```
* To reproduce the conditions of the supplementary YouTube video, keep the default reward function in `reward.py` and run:
```sh
python driver.py --centre 0 0 --radius 50 --xy_init -50 -50 --iters 1000 --C 1 --neighbour_size 5 --height 40
```
* To visualise in Minecraft, open a Minecraft: Java Edition world and open the console (press 'T'), leaving it empty. Be prepared to switch back to this window shortly. When running `driver.py`, set the command line argument `minecraft` to True.

## Theory
* The reward function is defined in `reward.py`, the default being:
```math
f(x,y) = cos(\frac{x}{3}) +cos(\frac{y}{3})-(\frac{x}{15})^2-(\frac{y}{15})^2
```
* The neighbour set for a state (x, y), where n is the value of `--neighbour_size` set using command-line arguments, is given by:
```math
\{(i, j) : x-n \leq i \leq x+n, y-n \leq j \leq y+n\} \backslash \{(x,y)\}
```
* The "temperature schedule", where C is the value of `--C` set using command-line arguments, is:
```math
\lambda (t) = C \cdot ln(1+t)
```
* Transition probabilities are set using Hastings-Metropolis as described in Ch 12.5 of Reference 1.

## Pointers if visualisation in Minecraft is enabled
* All chunks spanned by the printable region must be loaded.
* Arrange for Minecraft to remain the active window throughout printing, otherwise, commands may be entered into other fields on your computer.
    * If your screen locks, gibberish may be entered into the password field, requiring a hard restart — be sure to prevent sleeping.
    * macOS users can use `$ caffeinate -d`
* Since the `setblock` command tends to shift the player with each use, it is recommended that you build a stable viewing platform for the player.

## References
* "Simulation" (5th edition) by Sheldon M. Ross