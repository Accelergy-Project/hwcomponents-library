from hwcomponents import EnergyAreaModel, actionDynamicEnergy
from hwcomponents.scaling import *


class LibraryEstimatorClassBase(EnergyAreaModel):
    @actionDynamicEnergy
    def write(self) -> float:
        return 0

    @actionDynamicEnergy
    def read(self) -> float:
        return 0
