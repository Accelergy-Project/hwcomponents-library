from hwcomponents import ComponentModel, action, ActionCost
from hwcomponents.scaling import *


class LibraryEstimatorClassBase(ComponentModel):
    priority: float = 0.8

    @action
    def write(self) -> ActionCost:
        """Default write returns zero energy and latency."""
        return ActionCost(energy=0.0, throughput=float("inf"), latency=0.0)

    @action
    def read(self) -> ActionCost:
        """Default read returns zero energy and latency."""
        return ActionCost(energy=0.0, throughput=float("inf"), latency=0.0)
