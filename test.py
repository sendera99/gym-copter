#!/usr/bin/env python3
'''
Run simple test from http://gym.openai.com/docs/

Copyright (C) 2019 Simon D. Levy

MIT License
'''

import gym
import gym_copter

env = gym.make('CartPole-v0')

for i_episode in range(20):

    observation = env.reset()

    for t in range(100):

        env.render()

        print(observation)

        action = env.action_space.sample()

        observation, reward, done, info = env.step(action)

        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break

env.close()