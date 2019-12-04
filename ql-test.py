#!/usr/bin/env python3
'''
Trains a copter for maximum altitude using Q-Learing algorithm

Copyright (C) Simon D. Levy 2019

MIT License
'''

from ql import QLAgentContinuous
import gym_copter

import gym
import argparse
import os
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Run A3C algorithm on CopterGym.')

parser.add_argument('--train', dest='train', action='store_true', help='Train our model.')
parser.add_argument('--alpha', default=0.001, help='Learning rate for the shared optimizer.')
parser.add_argument('--neps', default=1000, type=int, help='Global maximum number of episodes to run.')
parser.add_argument('--gamma', default=0.99, help='Discount factor of rewards.')
parser.add_argument('--epsilon', default=0.99, help='Exploration rate.')

args = parser.parse_args()

env = gym.make('Copter-v0')

agent = QLAgentContinuous(env)

'''

if args.train:

    moving_average_rewards = agent.train(args.neps, args.alpha, args.gamma, args.epsilon)

    print(len(moving_average_rewards))

    plt.plot(moving_average_rewards)
    plt.ylabel('Moving average ep reward')
    plt.xlabel('Step')
    plt.title(args.game)
    plt.savefig(os.path.join(args.save_dir, '{} Moving Average.png'.format(args.game)))
    plt.show()

else:

    agent.play()
'''