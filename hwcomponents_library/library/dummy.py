from hwcomponents_library.base import LibraryEstimatorClassBase
from hwcomponents.scaling import *
from hwcomponents import actionDynamicEnergy


# Original CSV contents:
# global_cycle_period,energy,area,n_instances,action
# 1e-9,0,0,1,read|update|leak|write|*
class DummyStorage(LibraryEstimatorClassBase):
    component_name = "dummy_storage"
    priority = 0.9

    def __init__(self, tech_node: str):
        super().__init__(leak_power=0.0, area=0.0)
        self.tech_node: str = tech_node

    @actionDynamicEnergy
    def read(self) -> float:
        return 0.0

    @actionDynamicEnergy
    def write(self) -> float:
        return 0.0


# Original CSV contents:
# global_cycle_period,energy,area,n_instances,action
# 1e-9,0,0,1,read|update|leak|write|*
class DummyCompute(LibraryEstimatorClassBase):
    component_name = "dummy_compute"
    priority = 0.9

    def __init__(self, tech_node: str):
        super().__init__(leak_power=0.0, area=0.0)
        self.tech_node: str = tech_node

    @actionDynamicEnergy
    def read(self) -> float:
        return 0.0

    @actionDynamicEnergy
    def write(self) -> float:
        return 0.0
    
    @actionDynamicEnergy
    def compute(self) -> float:
        return 0.0


class DummyMemory(LibraryEstimatorClassBase):
    component_name = "dummy_memory"
    priority = 0.9

    def __init__(self, tech_node: str):
        super().__init__(leak_power=0.0, area=0.0)
        self.tech_node: str = tech_node

    @actionDynamicEnergy
    def read(self) -> float:
        return 0.0

    @actionDynamicEnergy
    def write(self) -> float:
        return 0.0

class DummyNetwork(LibraryEstimatorClassBase):
    component_name = "dummy_network"
    priority = 0.9

    def __init__(self, tech_node: str):
        super().__init__(leak_power=0.0, area=0.0)
        self.tech_node: str = tech_node

    @actionDynamicEnergy
    def read(self) -> float:
        return 0.0

    @actionDynamicEnergy
    def write(self) -> float:
        return 0.0
