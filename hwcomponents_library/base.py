from hwcomponents import EnergyAreaModel, actionDynamicEnergy
from hwcomponents.scaling import *


class LibraryEstimatorClassBase(EnergyAreaModel):
    priority: float = 0.8

    @actionDynamicEnergy
    def write(self) -> float:
        return 0

    @actionDynamicEnergy
    def read(self) -> float:
        return 0
