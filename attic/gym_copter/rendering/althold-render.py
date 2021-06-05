#!/usr/bin/env python3
'''
Run simple altitude-hold PID controller to test dynamics

Copyright (C) 2019 Simon D. Levy

MIT License
'''

import gym
import numpy as np
import matplotlib.pyplot as plt
from time import time

DURATION        = 30 # seconds
ALTITUDE_TARGET = 10 # meters

# PID params
ALT_P = 1.0
VEL_P = 1.0
VEL_I = 0
VEL_D = 0

# Time constant
DT = 0.001

class AltitudePidController(object):

    def __init__(self, target, posP, velP, velI, velD, windupMax=10):

        # In a real PID controller, this would be a set-point
        self.target = target

        # Constants
        self.posP = posP
        self.velP = velP
        self.velI = velI
        self.velD = velD
        self.windupMax = windupMax

        # Values modified in-flight
        self.posTarget      = 0
        self.lastError      = 0
        self.integralError  = 0

    def u(self, alt, vel, dt):

        # Compute dzdt setpoint and error
        velTarget = (self.target - alt) * self.posP
        velError = velTarget - vel

        # Update error integral and error derivative
        self.integralError +=  velError * dt
        self.integralError = AltitudePidController._constrainAbs(self.integralError + velError * dt, self.windupMax)
        deltaError = (velError - self.lastError) / dt if abs(self.lastError) > 0 else 0
        self.lastError = velError

        # Compute control u
        return self.velP * velError + self.velD * deltaError + self.velI * self.integralError

    def _constrainAbs(x, lim):

        return -lim if x < -lim else (+lim if x > +lim else x)

if __name__ == '__main__':

    # Create and initialize copter environment
    env = gym.make('gym_copter:Copter-v1')
    env.reset()

    # initial conditions
    z = 0
    u = np.zeros(4)
    prev = time()
    start = prev

    # Create PID controller
    pid  = AltitudePidController(ALTITUDE_TARGET, ALT_P, VEL_P, VEL_I, VEL_D)

    # Start timing
    prev = time()

    # Initialize array for plotting
    plotdata = []

    # Loop until user hits the stop button
    while True:

        # Draw the current environment
        if env.render() is None: break

        # Update timer
        curr = time()
        dt = curr - prev
        elapsed = curr - start
        prev = curr

        if elapsed > DURATION: break

        # Update the environment with the current motor commands
        state, _, _, _ = env.step(u*np.ones(4))

        # Extract altitude from state (negate to accommodate NED)
        z = -state[4]

        # Extract velocity from state (negate to accommodate NED)
        dzdt = -state[5]

        # Get correction from PID controller
        u = pid.u(z, dzdt, dt)

        # Constrain correction to [0,1] to represent motor value
        u = max(0, min(1, u))

        # Accumulate array for plotting
        plotdata.append([elapsed, z, u])

    # Plot results
    plotdata = np.array(plotdata)
    plt.subplot(2,1,1)
    plt.plot(plotdata[:,0], plotdata[:,1])
    plt.ylabel('Altitude (m)')
    plt.subplot(2,1,2)
    plt.plot(plotdata[:,0], plotdata[:,2])
    plt.ylabel('Motors')
    plt.xlabel('Time (s)')
    plt.show()

    # Cleanup
    del env
