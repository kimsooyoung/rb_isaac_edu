# Copyright 2024 Road Balance Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf, UsdLux
from omni.isaac.examples.base_sample import BaseSample
from omni.isaac.core.objects import DynamicCuboid

import numpy as np
import omni.usd


class HelloLight(BaseSample):
    def __init__(self) -> None:
        super().__init__()
        return

    def setup_scene(self):
        world = self.get_world()
        world.scene.add_default_ground_plane()

        # Turn off the default light
        stage = omni.usd.get_context().get_stage()
        prim = stage.GetPrimAtPath("/World/defaultGroundPlane/SphereLight")
        attribute = prim.GetAttribute("intensity")
        attribute.Set(0)

        fancy_cube = world.scene.add(
            DynamicCuboid(
                prim_path="/World/random_cube", # The prim path of the cube in the USD stage
                name="fancy_cube", # The unique name used to retrieve the object from the scene later on
                position=np.array([0, 0, 1.0]), # Using the current stage units which is in meters by default.
                scale=np.array([0.5015, 0.5015, 0.5015]), # most arguments accept mainly numpy arrays.
                color=np.array([0, 0, 1.0]), # RGB channels, going from 0-1
            ))

        # Create a Sphere light
        sphereLight = UsdLux.SphereLight.Define(stage, Sdf.Path("/World/MySphereLight"))
        sphereLight.CreateRadiusAttr(0.5)
        sphereLight.CreateIntensityAttr(50000.0)
        sphereLight.AddTranslateOp().Set(Gf.Vec3f(5.0, 5.0, 5.0))

        # Create a disk light
        diskLight = UsdLux.DiskLight.Define(stage, Sdf.Path("/World/MyDiskLight"))
        diskLight.CreateRadiusAttr(1.0)
        diskLight.CreateIntensityAttr(50000.0)
        diskLight.AddTranslateOp().Set(Gf.Vec3f(5.0, -5.0, 5.0))

        # Create a distant light
        distantLight = UsdLux.DistantLight.Define(stage, Sdf.Path("/World/MyDistantLight"))
        distantLight.CreateIntensityAttr(1000)
        distantLight.AddRotateXYZOp().Set((0, 45, 90))
        distantLight.AddTranslateOp().Set(Gf.Vec3f(-5.0, 5.0, 5.0))

        # Create a cylinder light
        cylinderLight = UsdLux.CylinderLight.Define(stage, Sdf.Path("/World/MyCylinderLight"))
        cylinderLight.CreateLengthAttr(2.0)
        cylinderLight.CreateRadiusAttr(0.05)
        cylinderLight.CreateIntensityAttr(50000.0)
        cylinderLight.AddTranslateOp().Set(Gf.Vec3f(-5.0, -5.0, 5.0))
        return

    async def setup_post_load(self):
        self._world = self.get_world()
        self._cube = self._world.scene.get_object("fancy_cube")
        return
