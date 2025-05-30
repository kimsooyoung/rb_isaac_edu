# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""
This script demonstrates how to create a simple environment with a cartpole. It combines the concepts of
scene, action, observation and event managers to create an environment.

.. code-block:: bash

    ./isaaclab.sh -p scripts/tutorials/03_envs/create_cartpole_base_env.py --num_envs 32
    or
    isaaclab -p my_create_cartpole_base_env_pid.py --num_envs 1

"""

"""Launch Isaac Sim Simulator first."""


import argparse

from isaaclab.app import AppLauncher

# add argparse arguments
parser = argparse.ArgumentParser(description="Tutorial on creating a cartpole base environment.")
parser.add_argument("--num_envs", type=int, default=16, help="Number of environments to spawn.")

# append AppLauncher cli args
AppLauncher.add_app_launcher_args(parser)
# parse the arguments
args_cli = parser.parse_args()

# launch omniverse app
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

"""Rest everything follows."""

import torch
import numpy as np

from isaaclab.envs import ManagerBasedEnv

# Environment configuration can be found from below code.
from robots.pendulum_manager_based_env import CartpoleEnvCfg
from model_based_control import PIDController


class Parameters():

    def __init__(self):
        self.goal = [np.pi, 0.0]

        # Control parameters
        self.Kp = 20.0
        self.Kd = 1.0
        self.Ki = 3.0

        # Torque limits
        # 5 X / 10 OK / 7.5 O / 6.0 X
        self.torque_limit = 10.0

        # pure control 30 ok / 25 x
        # self.min_torque, self.max_torque = -30, 30

def controller(obs, pid_controller, torque_limit, counter):
    theta, omega = obs[0]
    
    # Convert torch tensors to numpy arrays using detach() to avoid circular imports
    theta_np = theta.detach().cpu().numpy()
    omega_np = omega.detach().cpu().numpy()

    _, _, torque = pid_controller.get_control_output(counter, theta_np, omega_np)

    torque = np.clip(torque, -torque_limit, torque_limit)

    # Wrap in 2D NumPy array to get shape [1, 1]
    torque = torch.tensor([[torque]], dtype=torch.float32, device=theta.device)

    return torque

def main():
    """Main function."""
    # parse the arguments
    env_cfg = CartpoleEnvCfg()
    env_cfg.scene.num_envs = args_cli.num_envs
    env_cfg.sim.device = args_cli.device
    # setup base environment
    env = ManagerBasedEnv(cfg=env_cfg)

    params = Parameters()

    pid_controller = PIDController(
        Kp=params.Kp,
        Ki=params.Ki,
        Kd=params.Kd,
        use_feed_forward=True
    )
    pid_controller.set_goal(params.goal)

    # simulate physics
    count = 0
    obs = None
    while simulation_app.is_running():
        with torch.inference_mode():
            # reset
            if count % 100 == 0:
                count = 0
                env.reset()
                print("-" * 80)
                print("[INFO]: Resetting environment...")
            # sample random actions
            if obs is not None:
                joint_efforts = controller(obs["policy"], pid_controller, params.torque_limit, count)
                print(f"count: {count} / joint_efforts: {joint_efforts} {joint_efforts.size()} {type(joint_efforts)}")

                # step the environment
                obs, extra = env.step(joint_efforts)
            else:
                random_efforts = torch.randn_like(env.action_manager.action)
                print(f"random_efforts: {random_efforts} {random_efforts.size()} {type(random_efforts)}")

                # step the environment
                obs, extra = env.step(random_efforts)
                        
            # print current orientation of pole
            print("[Env 0]: Pole joint: ", obs["policy"][0][0].item())
            print("[Env 0]: Pole vel: ", obs["policy"][0][1].item())
            # update counter
            count += 1

    # close the environment
    env.close()


if __name__ == "__main__":
    # run the main function
    main()
    # close sim app
    simulation_app.close()