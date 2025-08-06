"""
@ARTICLE{9131838,
  author={Giterman, Robert and Shalom, Amir and Burg, Andreas and Fish, Alexander and Teman, Adam},
  journal={IEEE Solid-State Circuits Letters},
  title={A 1-Mbit Fully Logic-Compatible 3T Gain-Cell Embedded DRAM in 16-nm FinFET},
  year={2020},
  volume={3},
  number={},
  pages={110-113},
  keywords={Random access memory;FinFETs;Temperature measurement;Leakage currents;Power demand;Voltage measurement;Embedded DRAM;gain cell (GC);low voltage;retention time;SRAM},
  doi={10.1109/LSSC.2020.3006496}}
"""

from hwcomponents_library.base import LibraryEstimatorClassBase
from hwcomponents.scaling import *
from hwcomponents import actionDynamicEnergy


# Original CSV contents:
# tech_node,global_cycle_period,width|datawidth,depth,energy,area,action
# 16nm,1e-9,1024,1024,2641.92,131570,read
# 16nm,1e-9,1024,1024,2519.04,131570,write|update
# 16nm,1e-9,1024,1024,0.381,131570,leak
# # Read: 2.58 uW / MHz
# # Write: 2.46 uW / MHz
# # Leak + Refresh: (105uw leak) + (276uW refresh) = 381uW
# # @ARTICLE{9131838,
# #   author={Giterman, Robert and Shalom, Amir and Burg, Andreas and Fish, Alexander and Teman, Adam},
# #   journal={IEEE Solid-State Circuits Letters},
# #   title={A 1-Mbit Fully Logic-Compatible 3T Gain-Cell Embedded DRAM in 16-nm FinFET},
# #   year={2020},
# #   volume={3},
# #   number={},
# #   pages={110-113},
# #   keywords={Random access memory;FinFETs;Temperature measurement;Leakage currents;Power demand;Voltage measurement;Embedded DRAM;gain cell (GC);low voltage;retention time;SRAM},
# #   doi={10.1109/LSSC.2020.3006496}}
class RaaamEDRAM(LibraryEstimatorClassBase):
    component_name = "raaam_edram"
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str, width: int = 1024, depth: int = 1024):
        super().__init__(leak_power=3.81e-4, area=131570.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            16e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.width: int = self.scale("width", width, 1024, linear, linear, linear)
        self.depth: int = self.scale(
            "depth", depth, 1024, linear, cacti_depth_energy, cacti_depth_energy
        )

    @actionDynamicEnergy(bits_per_action="width")
    def read(self) -> float:
        return 2641.92e-12

    @actionDynamicEnergy(bits_per_action="width")
    def write(self) -> float:
        return 2519.04e-12
