'''
Copyright (C) 2019 Simon D. Levy

MIT License
'''

from gym.envs.registration import register

# 2D lander
register(
    id='Lander2D-v0',
    entry_point='gym_copter.envs:Lander2D',
    max_episode_steps=400
)

# 3D lander
register(
    id='Lander3D-v0',
    entry_point='gym_copter.envs:Lander3D',
    max_episode_steps=400
)
