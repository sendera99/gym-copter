#!/usr/bin/env python3
'''
2D Copter-Lander, based on
  https://github.com/openai/gym/blob/master/gym/envs/box2d/lunar_lander.py

This version controls each motor separately

Copyright (C) 2019 Simon D. Levy

MIT License
'''

import numpy as np
import time

from gym_copter.dynamics.djiphantom import DJIPhantomDynamics
from gym_copter.envs.lander import Lander


class Lander2D(Lander):

    PENALTY_FACTOR = 12  # penalizes distance from center of floor
    OBSERVATION_SIZE = 6
    ACTION_SIZE = 2

    def __init__(self):

        Lander.__init__(self)

    def reset(self):

        Lander.reset(self)

        self._destroy()

        # Create cusom dynamics model
        self.dynamics = DJIPhantomDynamics(self.FRAMES_PER_SECOND)

        # Initialize custom dynamics with random perturbation
        state = np.zeros(12)
        d = self.dynamics
        state[d.STATE_Y] = 0
        state[d.STATE_Z] = -self.INITIAL_ALTITUDE
        self.dynamics.setState(state)
        self.dynamics.perturb(np.array([0,                # X
                                        self._perturb(),  # Y
                                        self._perturb(),  # Z
                                        0,                # phi
                                        0,                # theta
                                        0]))              # psi

        return self.step(np.array([0, 0]))[0]

    def step(self, action):

        # Abbreviation
        d = self.dynamics
        status = d.getStatus()

        # Stop motors after safe landing
        if status == d.STATUS_LANDED:
            d.setMotors(np.zeros(4))
            self.spinning = False

        # In air, set motors from action
        else:
            m = np.clip(action, 0, 1)    # keep motors in interval [0,1]
            d.setMotors([m[0], m[1], m[1], m[0]])
            self.spinning = sum(m) > 0
            d.update()

        # Get new state from dynamics
        _, _, posy, vely, posz, velz, phi, velphi = d.getState()[:8]

        # Set lander pose for viewer
        self.pose = posy, posz, phi

        # Convert state to usable form
        state = np.array([posy, vely, posz, velz, phi, velphi])

        # Penalize distance from center and velocity
        shaping = -self.PENALTY_FACTOR * np.sqrt(np.sum(state[0:4]**2))

        reward = ((shaping - self.prev_shaping)
                  if (self.prev_shaping is not None)
                  else 0)

        self.prev_shaping = shaping

        # Assume we're not done yet
        done = False

        # Lose bigly if we go outside window
        if abs(posy) >= self.BOUNDS:
            done = True
            reward -= self.OUT_OF_BOUNDS_PENALTY

        else:

            # It's all over once we're on the ground
            if status == d.STATUS_LANDED:

                done = True
                self.spinning = False

                # Win bigly we land safely between the flags
                if abs(posy) < self.LANDING_RADIUS:

                    reward += self.INSIDE_RADIUS_BONUS

            elif status == d.STATUS_CRASHED:

                # Crashed!
                done = True
                self.spinning = False

        return np.array(state, dtype=np.float32), reward, done, {}

    def render(self, mode='human'):

        from gym_copter.rendering.twod import TwoDLanderRenderer

        # Create viewer if not done yet
        if self.viewer is None:
            self.viewer = TwoDLanderRenderer(self.LANDING_RADIUS)

        return self.viewer.render(mode, self.pose, self.spinning)

    def close(self):
        if self.viewer is not None:
            self.viewer.close()
            self.viewer = None

    def _perturb(self):

        return np.random.uniform(-self.INITIAL_RANDOM_FORCE,
                                 + self.INITIAL_RANDOM_FORCE)

    def _destroy(self):
        if self.viewer is not None:
            self.viewer.close()

    def heuristic(self, s):
        """
        The heuristic for
        1. Testing
        2. Demonstration rollout.

        Args:
            s (list): The state. Attributes:
                      s[0] is the horizontal coordinate
                      s[1] is the horizontal speed
                      s[2] is the vertical coordinate
                      s[3] is the vertical speed
                      s[4] is the angle
                      s[5] is the angular speed
        returns:
             a: The heuristic to be fed into the step function defined above to
                determine the next step and reward.
        """

        # Angle target
        A = 0.1  # 0.05
        B = 0.1  # 0.06

        # Angle PID
        C = 0.1  # 0.025
        D = 0.05
        E = 0.4

        # Vertical PID
        F = 1.15
        G = 1.33

        posy, vely, posz, velz, phi, velphi = s

        phi_targ = posy*A + vely*B         # angle should point towards center
        phi_todo = (phi-phi_targ)*C + phi*D - velphi*E

        hover_todo = posz*F + velz*G

        return hover_todo-phi_todo, hover_todo+phi_todo


def demo_heuristic_lander(env, seed=None, render=False):

    from time import sleep

    env.seed(seed)
    np.random.seed(seed)
    total_reward = 0
    steps = 0
    state = env.reset()
    while True:
        action = env.heuristic(state)
        state, reward, done, _ = env.step(action)
        total_reward += reward

        if render:
            frame = env.render('rgb_array')
            time.sleep(1./env.FRAMES_PER_SECOND)
            if frame is None:
                break

        if (steps % 20 == 0) or done:
            print("step {} total_reward {:+0.2f}".format(steps, total_reward))

        steps += 1
        if done:
            break

    sleep(1)
    env.close()
    return total_reward


def main():

    demo_heuristic_lander(Lander2D(), seed=None, render=True)


if __name__ == '__main__':
    main()
