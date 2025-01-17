from omni.isaac.core.utils.nucleus import get_assets_root_path
from omni.isaac.core.utils.types import ArticulationAction
from omni.isaac.wheeled_robots.robots import WheeledRobot
from omni.isaac.examples.base_sample import BaseSample

import numpy as np


class HelloMobileRobot(BaseSample):
    def __init__(self) -> None:
        super().__init__()

        assets_root_path = get_assets_root_path()
        self.JETBOT_PATH = assets_root_path + "/Isaac/Robots/Jetbot/jetbot.usd"

        return

    def setup_scene(self):
        world = self.get_world()
        world.scene.add_default_ground_plane()

        self._jetbot = world.scene.add(
            WheeledRobot(
                prim_path="/World/fancy_jetbot",
                name="fancy_jetbot",
                wheel_dof_names=["left_wheel_joint", "right_wheel_joint"],
                create_robot=True,
                usd_path=self.JETBOT_PATH,
                position=np.array([0.0, 0.0, 0.0]),
                orientation=np.array([1.0, 0.0, 0.0, 0.0]),
            )
        )
        return

    async def setup_post_load(self):
        self._world = self.get_world()
        self._jetbot = self._world.scene.get_object("fancy_jetbot")

        self._world.add_physics_callback("sending_actions", callback_fn=self.send_robot_actions)
        return

    def send_robot_actions(self, step_size):
        self._jetbot.apply_wheel_actions(
            ArticulationAction(
                joint_positions=None,
                joint_efforts=None,
                joint_velocities=5 * np.random.rand(2,)
            )
        )
        return