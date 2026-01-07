from hwcomponents import ComponentModel, action
from hwcomponents.scaling import *


class LibraryEstimatorClassBase(ComponentModel):
    priority: float = 0.8

    @action
    def write(self) -> tuple[float, float]:
        """Default write returns zero energy and latency."""
        return 0.0, 0.0

    @action
    def read(self) -> tuple[float, float]:
        """Default read returns zero energy and latency."""
        return 0.0, 0.0
