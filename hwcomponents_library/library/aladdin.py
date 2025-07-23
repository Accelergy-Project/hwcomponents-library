"""
@INPROCEEDINGS{6853196,
  author={Shao, Yakun Sophia and Reagen, Brandon and Wei, Gu-Yeon and Brooks, David},
  booktitle={2014 ACM/IEEE 41st International Symposium on Computer Architecture (ISCA)},
  title={Aladdin: A pre-RTL, power-performance accelerator simulator enabling large design space exploration of customized architectures},
  year={2014},
  volume={},
  number={},
  pages={97-108},
  doi={10.1109/ISCA.2014.6853196}}
"""

from hwcomponents_library.base import LibraryEstimatorClassBase
from hwcomponents.scaling import *
from hwcomponents import actionDynamicEnergy


# Original CSV contents:
# tech_node,global_cycle_seconds,width|datawidth,energy,area,action
# 40nm,1e-9,32,0.21,2.78E+02,add|read
# 40nm,1e-9,32,0.0024,2.78E+02,leak
# 40nm,1e-9,32,0,2.78E+02,update|write
class AladdinAdder(LibraryEstimatorClassBase):
    component_name = ["adder", "intadder", "aladdin_adder"]
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str, width: int = 32):
        super().__init__(leak_power=2.40e-6, area=278.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            40e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.width: int = self.scale("width", width, 32, linear, linear, linear)

    @actionDynamicEnergy
    def add(self) -> float:
        return 0.21e-12

    @actionDynamicEnergy
    def read(self) -> float:
        return 0.21e-12


# Original CSV contents:
# tech_node,global_cycle_seconds,width|datawidth,dynamic energy(pJ),area(um^2),action
# 40nm,1e-9,1,0.009,5.98E+00,read
# 40nm,1e-9,1,0,5.98E+00,write
# 40nm,1e-9,1,0,5.98E+00,leak|update
class AladdinRegister(LibraryEstimatorClassBase):
    component_name = ["register", "aladdin_register"]
    percent_accuracy_0_to_100 = 90

    def __init__(
        self,
        tech_node: str,
        width: int = 1,
        dynamic_energy: int = 1,
        area: int = 5.98e00,
    ):
        super().__init__(leak_power=0.0, area=5.98e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            40e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.width: int = self.scale("width", width, 1, linear, linear, linear)
        self.dynamic_energy: int = self.scale(
            "dynamic_energy", dynamic_energy, 1, linear, linear, linear
        )

    @actionDynamicEnergy
    def read(self) -> float:
        return 0.009e-12


# Original CSV contents:
# tech_node,global_cycle_seconds,width|datawidth,energy(pJ),area(um^2),action
# 40nm,1e-9,32,0.02947,71,compare|read
# 40nm,1e-9,32,2.51E-05,71,leak
# 40nm,1e-9,32,0,71,update|write
class AladdinComparator(LibraryEstimatorClassBase):
    component_name = ["comparator", "aladdin_comparator"]
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str, width: int = 32):
        super().__init__(leak_power=2.51e-8, area=71.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            40e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.width: int = self.scale("width", width, 32, linear, linear, linear)

    @actionDynamicEnergy
    def compare(self) -> float:
        return 0.02947e-12

    @actionDynamicEnergy
    def read(self) -> float:
        return 0.02947e-12


# Original CSV contents:
# tech_node,global_cycle_seconds,width|datawidth,width_a|datawidth_a,width_b|datawidth_b,energy(pJ),area(um^2),action
# 40nm,1e-9,32,32,32,12.68,6350,multiply|read
# 40nm,1e-9,32,32,32,0.08,6350,leak
# 40nm,1e-9,32,32,32,0,6350,update|write
class AladdinMultiplier(LibraryEstimatorClassBase):
    component_name = ["intmultiplier", "multiplier", "aladdin_multiplier"]
    percent_accuracy_0_to_100 = 90

    def __init__(
        self,
        tech_node: str,
        width: int = 32,
        width_a: int = 32,
        width_b: int = 32,
        energy: int = 12.68,
        area: int = 6350,
    ):
        super().__init__(leak_power=8.00e-5, area=6350.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            40e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.width: int = self.scale("width", width, 32, linear, linear, linear)
        self.width_a: int = self.scale("width_a", width_a, 32, linear, linear, linear)
        self.width_b: int = self.scale("width_b", width_b, 32, linear, linear, linear)

    @actionDynamicEnergy
    def multiply(self) -> float:
        return 12.68e-12

    @actionDynamicEnergy
    def read(self) -> float:
        return 12.68e-12


# Original CSV contents:
# tech_node,global_cycle_seconds,width|datawidth,energy(pJ),area(um^2),action
# 40nm,1e-9,32,0.25074,495.5,count|read
# 40nm,1e-9,32,0.0003213,495.5,leak
# 40nm,1e-9,32,0,495.5,update|write
class AladdinCounter(LibraryEstimatorClassBase):
    component_name = ["counter", "aladdin_counter"]
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str, width: int = 32):
        super().__init__(leak_power=3.21e-7, area=495.5e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            40e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.width: int = self.scale("width", width, 32, linear, linear, linear)

    @actionDynamicEnergy
    def count(self) -> float:
        return 0.25074e-12

    @actionDynamicEnergy
    def read(self) -> float:
        return 0.25074e-12
