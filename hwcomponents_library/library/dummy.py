from hwcomponents_library.base import LibraryEstimatorClassBase
from hwcomponents.scaling import *
from hwcomponents import action


# Original CSV contents:
# global_cycle_period,energy,area,n_instances,action
# 1e-9,0,0,1,read|update|leak|write|*
class DummyStorage(LibraryEstimatorClassBase):
    """
    A dummy storage component. Has zero area, zero energy, and zero leakage power.

    Parameters
    ----------
    tech_node: float, optional
        Technology node in meters. This is not used.
    """

    def __init__(self, tech_node: float | None = None):
        super().__init__(leak_power=0.0, area=0.0)
        self.tech_node: float = tech_node

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency of one read operation. Energy is zero.

        Returns
        -------
        (energy, latency): (0.0, 0.0)
        """
        return 0.0, 0.0

    @action
    def write(self) -> tuple[float, float]:
        """
        Returns the energy and latency of one write operation. Energy is zero.

        Returns
        -------
        (energy, latency): (0.0, 0.0)
        """
        return 0.0, 0.0


# Original CSV contents:
# global_cycle_period,energy,area,n_instances,action
# 1e-9,0,0,1,read|update|leak|write|*
class DummyCompute(LibraryEstimatorClassBase):
    """
    A dummy compute component. Has zero area, zero energy, and zero leakage power.

    Parameters
    ----------
    tech_node: float, optional
        Technology node in meters. This is not used.
    """

    def __init__(self, tech_node: float | None = None):
        super().__init__(leak_power=0.0, area=0.0)
        self.tech_node: float = tech_node

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency of one compute operation. Energy is zero.

        Returns
        -------
        (energy, latency): (0.0, 0.0)
        """
        return 0.0, 0.0

    @action
    def compute(self) -> tuple[float, float]:
        """
        Returns the energy and latency of one compute operation. Energy is zero.

        Returns
        -------
        (energy, latency): (0.0, 0.0)
        """
        return 0.0, 0.0


class DummyMemory(LibraryEstimatorClassBase):
    """
    A dummy memory component. Has zero area, zero energy, and zero leakage power.

    Parameters
    ----------
    tech_node: float
        Technology node in meters. This is not used.
    """

    def __init__(self, tech_node: float | None = None):
        super().__init__(leak_power=0.0, area=0.0)
        self.tech_node: float = tech_node

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency of one read operation. Energy is zero.

        Returns
        -------
        (energy, latency): (0.0, 0.0)
        """
        return 0.0, 0.0

    @action
    def write(self) -> tuple[float, float]:
        """
        Returns the energy and latency of one write operation. Energy is zero.

        Returns
        -------
        (energy, latency): (0.0, 0.0)
        """
        return 0.0, 0.0


class DummyNetwork(LibraryEstimatorClassBase):
    """
    A dummy network component. Has zero area, zero energy, and zero leakage power.

    Parameters
    ----------
    tech_node: float
        Technology node in meters. This is not used.
    """

    def __init__(self, tech_node: float | None = None):
        super().__init__(leak_power=0.0, area=0.0)
        self.tech_node: float = tech_node

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency of one read operation. Energy is zero.

        Returns
        -------
        (energy, latency): (0.0, 0.0)
        """
        return 0.0, 0.0

    @action
    def write(self) -> tuple[float, float]:
        """
        Returns the energy and latency of one write operation. Energy is zero.

        Returns
        -------
        (energy, latency): (0.0, 0.0)
        """
        return 0.0, 0.0
