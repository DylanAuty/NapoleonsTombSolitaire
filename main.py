# Napoleons Tomb simulator
# Simulates a version of the Napoleon's Tomb solitaire game to work out the chances of winning.
import logging
import argparse
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

from NapoleonsTomb import NapoleonsTomb


def main(args):
    wins = 0
    losses = 0   # Define both to allow early stopping
    fractions = np.array([])    # Stores rolling success rate at each trial
    trials_idx = []             # Trial idx for use with line.set_xdata

    if args.plot is not None:
        if args.plot == "live":
            plt.ion()
        fig = plt.figure()
        plt.xlabel("Iterations")
        plt.ylabel("Win rate (%)")
        plt.xlim(0, args.num_trials)
        plt.ylim(0, 100)
        if args.plot == "live":
            line, = plt.plot(trials_idx, fractions)

    # Main loop
    for i in tqdm(range(args.num_trials)):
        game = NapoleonsTomb()
        result = game.simulate_game()
        # print(result)
        if result:
            wins += 1
        else:
            losses += 1
        win_percentage = 100 * wins / (i + 1)
        fractions = np.append(fractions, win_percentage)
        trials_idx.append(i)
        if args.plot == "live":
            line.set_xdata(trials_idx)
            line.set_ydata(fractions)
            fig.canvas.draw()
            fig.canvas.flush_events()
    
    if args.plot == "final":
        plt.plot(fractions)
        plt.show()

    print(f"Wins: {wins}, Losses: {losses}, percent: {win_percentage}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="NapoleonsTomb",
        description="Simulate the Napoleon's Tomb solitaire game",
    )
    parser.add_argument('-n', '--num_trials', type=int, default=1000, help="How many trials to simulate for.")
    parser.add_argument('-p', '--plot', type=str, choices=["live", "final"], help="Whether to plot success rate, and if so whether to do so live or at the end.")

    args = parser.parse_args()
    main(args)
