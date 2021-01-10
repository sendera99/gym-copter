'''
Copyright (C) 2019 Simon D. Levy

MIT License
'''

from gym.envs.registration import register

register(
    id='Lander-v0',
    entry_point='gym_copter.envs:Lander2D',
    max_episode_steps=2000
)

register(
    id='Lander3D-v0',
    entry_point='gym_copter.envs:Lander3D',
    max_episode_steps=2000
)

register(
    id='Lander3DHardcore-v0',
    entry_point='gym_copter.envs:Lander3DHardcoreFixed',
    max_episode_steps=2000
)

register(
    id='Lander3DHardcore-v1',
    entry_point='gym_copter.envs:Lander3DHardcore',
    max_episode_steps=2000
)
