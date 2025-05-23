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

from omni.isaac.examples.base_sample import BaseSampleExtension
import os

from .etri_defect_car_panel_example import DefectEnv
# from .etri_defect_car_panel_env import DefectEnv

"""
This file serves as a basic template for the standard boilerplate operations
that make a UI-based extension appear on the toolbar.

This implementation is meant to cover most use-cases without modification.
Various callba/home/kimsooyoung/Documents/IssacSimTutorials/rb_issac_tutorial/RoadBalanceEdu/ETRIUR52F85Insertion
/home/kimsooyoung/Documents/IssacSimTutorials/rb_issac_tutorial/RoadBalanceEdu/ETRIUR52F85Insertioncks are hooked up to a seperate class UIBuilder in .ui_builder.py
Most users will be able to make their desired UI extension by interacting solely with
UIBuilder.

This class sets up standard useful callback functions in UIBuilder:
    on_menu_callback: Called when extension is opened
    on_timeline_event: Called when timeline is stopped, paused, or played
    on_physics_step: Called on every physics step
    on_stage_event: Called when stage is opened or closed
    cleanup: Called when resources such as physics subscriptions should be cleaned up
    build_ui: User function that creates the UI they want.
"""

class Extension(BaseSampleExtension):
    def on_startup(self, ext_id: str):
        super().on_startup(ext_id)
        super().start_extension(
            menu_name="RoadBalanceEdu",
            submenu_name="",
            name="HelloDefectCarPanel",
            title="HelloDefectCarPanel",
            doc_link="https://docs.omniverse.nvidia.com/isaacsim/latest/core_api_tutorials/tutorial_core_hello_world.html",
            overview="This Example introduces the user on how to do cool stuff with Isaac Sim through scripting in asynchronous mode.",
            file_path=os.path.abspath(__file__),
            sample=DefectEnv(),
        )
        return
