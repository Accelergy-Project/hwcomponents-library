from hwcomponents_library.base import LibraryEstimatorClassBase
from hwcomponents.scaling import *
from hwcomponents import actionDynamicEnergy


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

    @actionDynamicEnergy
    def read(self) -> float:
        """
        Returns the energy of one read operation in Joules. Energy is zero.

        Returns
        -------
        float
            Energy of one read operation in Joules
        """
        return 0.0

    @actionDynamicEnergy
    def write(self) -> float:
        """
        Returns the energy of one write operation in Joules. Energy is zero.

        Returns
        -------
        float
            Energy of one write operation in Joules
        """
        return 0.0


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

    @actionDynamicEnergy
    def read(self) -> float:
        """
        Returns the energy of one compute operation in Joules. Energy is zero.

        Returns
        -------
        float
            Energy of one compute operation in Joules
        """
        return 0.0

    @actionDynamicEnergy
    def compute(self) -> float:
        """
        Returns the energy of one compute operation in Joules. Energy is zero.

        Returns
        -------
        float
            Energy of one compute operation in Joules
        """
        return 0.0


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

    @actionDynamicEnergy
    def read(self) -> float:
        """
        Returns the energy of one read operation in Joules. Energy is zero.

        Returns
        -------
        float
            Energy of one read operation in Joules
        """
        return 0.0

    @actionDynamicEnergy
    def write(self) -> float:
        """
        Returns the energy of one write operation in Joules. Energy is zero.

        Returns
        -------
        float
            Energy of one write operation in Joules
        """
        return 0.0


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

    @actionDynamicEnergy
    def read(self) -> float:
        """
        Returns the energy of one read operation in Joules. Energy is zero.

        Returns
        -------
        float
            Energy of one read operation in Joules
        """
        return 0.0

    @actionDynamicEnergy
    def write(self) -> float:
        """
        Returns the energy of one write operation in Joules. Energy is zero.

        Returns
        -------
        float
            Energy of one write operation in Joules
        """
        return 0.0
