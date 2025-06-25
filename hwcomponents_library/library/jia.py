"""
@ARTICLE{9082159,
  author={Jia, Hongyang and Valavi, Hossein and Tang, Yinqi and Zhang, Jintao and Verma, Naveen},
  journal={IEEE Journal of Solid-State Circuits},
  title={A Programmable Heterogeneous Microprocessor Based on Bit-Scalable In-Memory Computing},
  year={2020},
  volume={55},
  number={9},
  pages={2609-2621},
  doi={10.1109/JSSC.2020.2987714}}
"""

from hwcomponents_library.base import LibraryEstimatorClassBase
from hwcomponents.scaling import *
from hwcomponents import actionDynamicEnergy


# Original CSV contents:
# tech_node,global_cycle_seconds,resolution,voltage,energy,area,action
# 65nm,      540e-9,              8,         1.2,   2.25,   5000,read
# 65nm,      540e-9,              8,         1.2,   1.2,    5000,leak
# 65nm,      540e-9,              8,         1.2,   0,      5000,write|update
class JiaShiftAdd(LibraryEstimatorClassBase):
    component_name = "jia_shift_add"
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str, resolution: int = 8, voltage: float = 1.2):
        super().__init__(leak_power=2.22e-6, area=5000.0e-12)
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
        self.voltage: float = self.scale("voltage", voltage, 1.2, noscale, quadratic, 1)

    @actionDynamicEnergy
    def read(self) -> float:
        return 2.25e-12


# Original CSV contents:
# tech_node,global_cycle_seconds,rows,resolution,voltage,energy,area,action
# 65nm,      540e-9,              1,   8,         1.2,   0.5,   174, read
# 65nm,      540e-9,              1,   8,         1.2,   0.2,   174, leak
# 65nm,      540e-9,              1,   8,         1.2,   0,     174, write|update
class JiaZeroGate(LibraryEstimatorClassBase):
    component_name = "jia_zero_gate"
    percent_accuracy_0_to_100 = 90

    def __init__(
        self, tech_node: str, rows: int = 1, resolution: int = 8, voltage: float = 1.2
    ):
        super().__init__(leak_power=3.70e-7, area=174.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            65e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.rows: int = self.scale("rows", rows, 1, linear, noscale, noscale)
        self.resolution: int = self.scale(
            "resolution", resolution, 8, pow_base(2), pow_base(2), pow_base(2)
        )
        self.voltage: float = self.scale("voltage", voltage, 1.2, noscale, quadratic, 1)

    @actionDynamicEnergy
    def read(self) -> float:
        return 0.5e-12


# Original CSV contents:
# tech_node,global_cycle_seconds,voltage,energy,area,  action
# 65nm,      540e-9,              1.2,   12,     10535,read
# 65nm,      540e-9,              1.2,   2.4,    10535,leak
# 65nm,      540e-9,              1.2,   0,      10535,write|update
class JiaDatapath(LibraryEstimatorClassBase):
    component_name = "jia_datapath"
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str, voltage: float = 1.2):
        super().__init__(leak_power=4.44e-6, area=10535.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            65e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.voltage: float = self.scale("voltage", voltage, 1.2, noscale, quadratic, 1)

    @actionDynamicEnergy
    def read(self) -> float:
        return 12.0e-12
