from hwcomponents import EnergyAreaEstimator, actionDynamicEnergy
from hwcomponents.scaling import *


class LibraryEstimatorClassBase(EnergyAreaEstimator):
    @actionDynamicEnergy
    def write(self) -> float:
        return 0

    @actionDynamicEnergy
    def read(self) -> float:
        return 0
