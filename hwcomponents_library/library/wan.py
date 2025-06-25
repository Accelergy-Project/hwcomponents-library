"""
@article{wan2022compute,
  title={A compute-in-memory chip based on resistive random-access memory},
  author={Wan, Weier and Kubendran, Rajkumar and Schaefer, Clemens and Eryilmaz, Sukru Burc and Zhang, Wenqiang and Wu, Dabin and Deiss, Stephen and Raina, Priyanka and Qian, He and Gao, Bin and others},
  journal={Nature},
  volume={608},
  number={7923},
  pages={504--512},
  year={2022},
  publisher={Nature Publishing Group UK London}
}
"""

from hwcomponents_library.base import LibraryEstimatorClassBase
from hwcomponents.scaling import *
from hwcomponents import actionDynamicEnergy


# Original CSV contents:
# tech_node,n_repeats,global_cycle_seconds,resolution, voltage,energy,area,  action
# 130nm,     1,      1e-6,                8,          1.8,    0.1,   170,  read
# 130nm,     1,      1e-6,                8,          1.8,    0.1,   170,  write|update
# 130nm,     1,      1e-6,                8,          1.8,    0.1,   170,  leak
class WanShiftAdd(LibraryEstimatorClassBase):
    component_name = "wan_shift_add"
    percent_accuracy_0_to_100 = 90

    def __init__(
        self,
        tech_node: str,
        n_repeats: int = 1,
        resolution: int = 8,
        voltage: float = 1.8,
    ):
        super().__init__(leak_power=1.00e-7, area=170.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            130e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.n_repeats: int = self.scale(
            "n_repeats", n_repeats, 1, linear, linear, linear
        )
        self.resolution: int = self.scale(
            "resolution", resolution, 8, pow_base(2), pow_base(2), pow_base(2)
        )
        self.voltage: float = self.scale("voltage", voltage, 1.8, noscale, quadratic, 1)

    @actionDynamicEnergy
    def read(self) -> float:
        return 0.1e-12

    @actionDynamicEnergy
    def write(self) -> float:
        return 0.1e-12


# Original CSV contents:
# tech_node,n_repeats,global_cycle_seconds,voltage,energy,area,  action
# 130nm,     1,      1e-6,                1.8,    0.3,  400,   read
# 130nm,     1,      1e-6,                1.8,    0,     400,   leak
# 130nm,     1,      1e-6,                1.8,    0,     400,   write|update
class WanVariablePrecisionAdc(LibraryEstimatorClassBase):
    component_name = "wan_variable_precision_adc"
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str, n_repeats: int = 1, voltage: float = 1.8):
        super().__init__(leak_power=0.0, area=400.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            130e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.n_repeats: int = self.scale(
            "n_repeats", n_repeats, 1, linear, linear, linear
        )
        self.voltage: float = self.scale("voltage", voltage, 1.8, noscale, quadratic, 1)

    @actionDynamicEnergy
    def read(self) -> float:
        return 0.3e-12


# Original CSV contents:
# tech_node,global_cycle_seconds,voltage,energy,area,  action
# 130nm,     1e-6,                1.8,    1.2,   350,  read
# 130nm,     1e-6,                1.8,    0,     350,  leak
# 130nm,     1e-6,                1.8,    0,     350,  write|update
class WanAnalogSample(LibraryEstimatorClassBase):
    component_name = "wan_analog_sample"
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str, voltage: float = 1.8):
        super().__init__(leak_power=0.0, area=350.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            130e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.voltage: float = self.scale("voltage", voltage, 1.8, noscale, quadratic, 1)

    @actionDynamicEnergy
    def read(self) -> float:
        return 1.2e-12


# Original CSV contents:
# tech_node,n_repeats,global_cycle_seconds,voltage,energy,area, action
# 130nm,     1,      1e-6,                 1.8,   0.25,  350,  read
# 130nm,     1,      1e-6,                1.8,    0,     350,  leak
# 130nm,     1,      1e-6,                1.8,    0,     350,  write|update
class WanAnalogIntegrator(LibraryEstimatorClassBase):
    component_name = "wan_analog_integrator"
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str, n_repeats: int = 1, voltage: float = 1.8):
        super().__init__(leak_power=0.0, area=350.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            130e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.n_repeats: int = self.scale(
            "n_repeats", n_repeats, 1, linear, linear, linear
        )
        self.voltage: float = self.scale("voltage", voltage, 1.8, noscale, quadratic, 1)

    @actionDynamicEnergy
    def read(self) -> float:
        return 0.25e-12
