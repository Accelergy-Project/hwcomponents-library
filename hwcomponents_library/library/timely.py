"""
@INPROCEEDINGS{9138916,
  author={Li, Weitao and Xu, Pengfei and Zhao, Yang and Li, Haitong and Xie, Yuan and Lin, Yingyan},
  booktitle={2020 ACM/IEEE 47th Annual International Symposium on Computer Architecture (ISCA)},
  title={Timely: Pushing Data Movements And Interfaces In Pim Accelerators Towards Local And In Time Domain},
  year={2020},
  volume={},
  number={},
  pages={832-845},
  doi={10.1109/ISCA45697.2020.00073}}
"""

from hwcomponents_library.base import LibraryEstimatorClassBase
from hwcomponents.scaling import *
from hwcomponents import actionDynamicEnergy
from .isaac import IsaacChip2ChipLink


# Original CSV contents:
# tech_node,global_cycle_seconds,energy,area,action
# 65nm,1e-9,0.0368,40,read|add
# 65nm,1e-9,0,40,write|update|leak
# # TIMELY says these don't contribute to area
# # Numbers from paper table II
class TimelyIadder(LibraryEstimatorClassBase):
    component_name = "timely_iadder"
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str):
        super().__init__(leak_power=0.0, area=40.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            65e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )

    @actionDynamicEnergy
    def read(self) -> float:
        return 0.0368e-12

    @actionDynamicEnergy
    def add(self) -> float:
        return 0.0368e-12


# Original CSV contents:
# tech_node,global_cycle_seconds,n_instances,energy,area,action
# 65nm,1e-9,1,0.0023,5,drive|read|convert
# 65nm,1e-9,1,0,5,leak|update|write
# # Numbers from paper table II
class TimelyPsubBuf(LibraryEstimatorClassBase):
    component_name = "timely_psubBuf"
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str):
        super().__init__(leak_power=0.0, area=5.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            65e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )

    @actionDynamicEnergy
    def drive(self) -> float:
        return 0.0023e-12

    @actionDynamicEnergy
    def read(self) -> float:
        return 0.0023e-12

    @actionDynamicEnergy
    def convert(self) -> float:
        return 0.0023e-12


# Original CSV contents:
# tech_node,global_cycle_seconds,resolution,energy,area,action
# 65nm,1e-9,8,0.0375,240,convert|read
# 65nm,1e-9,8,0,240,write|leak|update
# # Numbers from paper table II
class TimelyDTC(LibraryEstimatorClassBase):
    component_name = "timely_dtc"
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str, resolution: int = 8):
        super().__init__(leak_power=0.0, area=240.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            65e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.resolution: int = self.scale(
            "resolution", resolution, 8, pow_base(2), pow_base(2), pow_base(2)
        )

    @actionDynamicEnergy
    def convert(self) -> float:
        return 0.0375e-12

    @actionDynamicEnergy
    def read(self) -> float:
        return 0.0375e-12


# Original CSV contents:
# tech_node,global_cycle_seconds,resolution,energy,area,action
# 65nm,1e-9,8,0.145,310,convert|read
# 65nm,1e-9,8,0,310,leak|write|update
class TimelyTdc(LibraryEstimatorClassBase):
    component_name = "timely_tdc"
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str, resolution: int = 8):
        super().__init__(leak_power=0.0, area=310.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            65e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.resolution: int = self.scale(
            "resolution", resolution, 8, pow_base(2), pow_base(2), pow_base(2)
        )

    @actionDynamicEnergy
    def convert(self) -> float:
        return 0.145e-12

    @actionDynamicEnergy
    def read(self) -> float:
        return 0.145e-12


# Original CSV contents:
# tech_node,global_cycle_seconds,rows,energy,area,action
# 65nm,1e-9,1,0.00062,5,read|drive|buffer
# 65nm,1e-9,1,0,5,leak|write|update
# # Numbers from paper table II
class TimelyXsubBuf(LibraryEstimatorClassBase):
    component_name = "timely_xsubBuf"
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str, rows: int = 1):
        super().__init__(leak_power=0.0, area=5.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            65e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.rows: int = self.scale("rows", rows, 1, linear, noscale, noscale)

    @actionDynamicEnergy
    def read(self) -> float:
        return 0.00062e-12

    @actionDynamicEnergy
    def drive(self) -> float:
        return 0.00062e-12

    @actionDynamicEnergy
    def buffer(self) -> float:
        return 0.00062e-12


# Original CSV contents:
# tech_node,global_cycle_seconds,energy,area,action
# 65nm,1e-9,0.0417,40,compare|read
# 65nm,1e-9,0,40,write|update|leak
# # Numbers from paper table II
class TimelyChargingComparator(LibraryEstimatorClassBase):
    component_name = "timely_charging_comparator"
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str):
        super().__init__(leak_power=0.0, area=40.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            65e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )

    @actionDynamicEnergy
    def compare(self) -> float:
        return 0.0417e-12

    @actionDynamicEnergy
    def read(self) -> float:
        return 0.0417e-12


# Original CSV contents:
# tech_node,global_cycle_seconds,width|datawidth,depth,energy,area,action
# 65nm,1e-9,128,128,203.776,40,read
# 65nm,1e-9,128,128,496.624,40,write|update
# 65nm,1e-9,128,128,0,40,leak
class TimelyInputOutputBuffer(LibraryEstimatorClassBase):
    component_name = "timely_input_output_buffer"
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str, width: int = 128, depth: int = 128):
        super().__init__(leak_power=0.0, area=40.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            65e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.width: int = self.scale("width", width, 128, linear, linear, linear)
        self.depth: int = self.scale(
            "depth", depth, 128, linear, cacti_depth_energy, cacti_depth_energy
        )

    @actionDynamicEnergy
    def read(self) -> float:
        return 203.776e-12

    @actionDynamicEnergy
    def write(self) -> float:
        return 496.624e-12


class TimelyChip2ChipLink(IsaacChip2ChipLink):
    pass
