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
from hwcomponents import action


# Original CSV contents:
# tech_node,global_cycle_period,width|datawidth,energy,area,action
# 40nm,1e-9,32,0.21,2.78E+02,add|read
# 40nm,1e-9,32,0.0024,2.78E+02,leak
# 40nm,1e-9,32,0,2.78E+02,update|write
class AladdinAdder(LibraryEstimatorClassBase):
    """
    An adder from the Aladdin paper. Adds two values.

    Parameters
    ----------
    tech_node : str
        The technology node in meters.
    width : int, optional
        The width of the adder in bits. This is the number of bits of the input values.

    Attributes
    ----------
    tech_node : str
        The technology node in meters.
    width : int
        The width of the adder in bits. This is the number of bits of the input values.
    """

    component_name = ["Adder", "AladdinAdder", "IntAdder"]
    priority = 0.1

    def __init__(self, tech_node: float, width: int = 32):
        super().__init__(leak_power=2.40e-6, area=278.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            40e-9,
            tech_node_area,
            tech_node_energy,
            noscale,
            tech_node_leak,
        )
        self.width: int = self.scale(
            "width", width, 32, linear, linear, noscale, linear
        )

    @action
    def add(self) -> tuple[float, float]:
        """
        Returns the energy and latency for one addition operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.21e-12, 0.0

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency for one addition operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.21e-12, 0.0


# Original CSV contents:
# tech_node,global_cycle_period,width|datawidth,dynamic energy(pJ),area(um^2),action
# 40nm,1e-9,1,0.009,5.98E+00,read
# 40nm,1e-9,1,0,5.98E+00,write
# 40nm,1e-9,1,0,5.98E+00,leak|update
class AladdinRegister(LibraryEstimatorClassBase):
    """
    A register from the Aladdin paper. Stores a value.

    Parameters
    ----------
    tech_node : str
        The technology node in meters.
    width : int, optional
        The width of the register in bits.
    """

    component_name = ["Register", "AladdinRegister"]
    priority = 0.1

    def __init__(
        self,
        tech_node: float,
        width: int = 1,
        dynamic_energy: int = 1,
        area: int = 5.98e00,
    ):
        super().__init__(leak_power=0.0, area=5.98e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            40e-9,
            tech_node_area,
            tech_node_energy,
            noscale,
            tech_node_leak,
        )
        self.width: int = self.scale("width", width, 1, linear, linear, noscale, linear)
        self.dynamic_energy: int = self.scale(
            "dynamic_energy", dynamic_energy, 1, linear, linear, noscale, linear
        )

    @action(bits_per_action="width")
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency for one read operation.

        Parameters
        ----------
        bits_per_action : int
            The number of bits that are read.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.009e-12, 0.0

    @action(bits_per_action="width")
    def write(self) -> tuple[float, float]:
        """
        Returns the energy and latency for one write operation.

        Parameters
        ----------
        bits_per_action : int
            The number of bits that are written.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.009e-12, 0.0


# Original CSV contents:
# tech_node,global_cycle_period,width|datawidth,energy(pJ),area(um^2),action
# 40nm,1e-9,32,0.02947,71,compare|read
# 40nm,1e-9,32,2.51E-05,71,leak
# 40nm,1e-9,32,0,71,update|write
class AladdinComparator(LibraryEstimatorClassBase):
    """
    A comparator from the Aladdin paper. Tells whether one value is greater than
    another.

    Parameters
    ----------
    tech_node : str
        The technology node in meters.
    width : int, optional
        The width of the comparator in bits.
    """

    component_name = ["Comparator", "AladdinComparator"]
    priority = 0.1

    def __init__(self, tech_node: float, width: int = 32):
        super().__init__(leak_power=2.51e-8, area=71.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            40e-9,
            tech_node_area,
            tech_node_energy,
            noscale,
            tech_node_leak,
        )
        self.width: int = self.scale(
            "width", width, 32, linear, linear, noscale, linear
        )

    @action
    def compare(self) -> tuple[float, float]:
        """
        Returns the energy and latency for one comparison operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.02947e-12, 0.0

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency for one comparison operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.02947e-12, 0.0


# Original CSV contents:
# tech_node,global_cycle_period,width|datawidth,width_a|datawidth_a,width_b|datawidth_b,energy(pJ),area(um^2),action
# 40nm,1e-9,32,32,32,12.68,6350,multiply|read
# 40nm,1e-9,32,32,32,0.08,6350,leak
# 40nm,1e-9,32,32,32,0,6350,update|write
class AladdinMultiplier(LibraryEstimatorClassBase):
    """
    A integer multiplier from the Aladdin paper. Multiplies two values.

    Parameters
    ----------
    tech_node : str
        The technology node in meters.
    width : int, optional
        The width of the multiplier in bits. Can not be set if width_a and width_b are
        set.
    width_a : int, optional
        The width of the first input value in bits.
    width_b : int, optional
        The width of the second input value in bits.
    """

    component_name = ["Multiplier", "AladdinMultiplier", "IntMultiplier"]
    priority = 0.1

    def __init__(
        self,
        tech_node: float,
        width: int = 32,
        width_a: int = 32,
        width_b: int = 32,
        energy: int = 12.68,
        area: int = 6350,
    ):
        super().__init__(leak_power=8.00e-5, area=6350.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            40e-9,
            tech_node_area,
            tech_node_energy,
            noscale,
            tech_node_leak,
        )
        if width_a != 32 and width != 32:
            raise ValueError(
                "width and width_a cannot both be set. Either set width of both inputs "
                "or width_a and width_b separately."
            )
        if width != 32 and width_b != 32:
            raise ValueError(
                "width and width_b cannot both be set. Either set width of both inputs "
                "or width_a and width_b separately."
            )
        self.width: int = self.scale(
            "width", width, 32, quadratic, noscale, quadratic, quadratic
        )
        self.width_a: int = self.scale(
            "width_a", width_a, 32, linear, linear, noscale, linear
        )
        self.width_b: int = self.scale(
            "width_b", width_b, 32, linear, linear, noscale, linear
        )

    @action
    def multiply(self) -> tuple[float, float]:
        """
        Returns the energy and latency for one multiplication operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 12.68e-12, 0.0

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency for one read operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 12.68e-12, 0.0


# Original CSV contents:
# tech_node,global_cycle_period,width|datawidth,energy(pJ),area(um^2),action
# 40nm,1e-9,32,0.25074,495.5,count|read
# 40nm,1e-9,32,0.0003213,495.5,leak
# 40nm,1e-9,32,0,495.5,update|write
class AladdinCounter(LibraryEstimatorClassBase):
    """
    A counter from the Aladdin paper. Increments a stored value.

    Parameters
    ----------
    tech_node : str
        The technology node in meters.
    width : int, optional
        The width of the counter in bits.
    """

    component_name = ["Counter", "AladdinCounter"]
    priority = 0.1

    def __init__(self, tech_node: float, width: int = 32):
        super().__init__(leak_power=3.21e-7, area=495.5e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            40e-9,
            tech_node_area,
            tech_node_energy,
            noscale,
            tech_node_leak,
        )
        self.width: int = self.scale(
            "width", width, 32, linear, linear, noscale, linear
        )

    @action
    def count(self) -> tuple[float, float]:
        """
        Returns the energy and latency for one increment operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.25074e-12, 0.0

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency for one increment operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.25074e-12, 0.0


class AladdinIntMAC(LibraryEstimatorClassBase):
    """
    A integer multiply-accumulate unit from the Aladdin paper. Multiplies two values
    and adds the result to a stored value.

    Parameters
    ----------
    tech_node : str
        The technology node in meters.
    adder_width : int, optional
        The width of the adder in bits.
    multiplier_width : int, optional
        The width of the multiplier in bits.
    """

    component_name = ["IntMAC", "AladdinIntMAC"]
    priority = 0.1

    def __init__(
        self, tech_node: float, adder_width: int = 16, multiplier_width: int = 8
    ):
        self.adder = AladdinAdder(tech_node, adder_width)
        self.multiplier = AladdinMultiplier(tech_node, multiplier_width)
        super().__init__(
            area=self.adder.area + self.multiplier.area,
            leak_power=self.adder.leak_power + self.multiplier.leak_power,
        )

    @action
    def mac(self) -> tuple[float, float]:
        """
        Returns the energy and latency for one multiply-accumulate operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        ae, al = self.adder.add()
        me, ml = self.multiplier.multiply()
        return ae + me, max(al, ml)

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency for one multiply-accumulate operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return self.mac()

    @action
    def compute(self) -> tuple[float, float]:
        """
        Returns the energy and latency for one multiply-accumulate operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return self.mac()
