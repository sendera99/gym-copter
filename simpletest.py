#!/usr/bin/env python3
'''
Simple test of gym-copter

Copyright (C) Simon D. Levy 2019

MIT License
'''

import gym
from time import sleep

env = gym.make('gym_copter:copter-v0')

env.reset()

for _ in range(1000):
    env.render()
    env.step([.6]*4)
    sleep(.001)
env.close()
