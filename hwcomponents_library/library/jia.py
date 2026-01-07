"""
@ARTICLE{9082159,
  author={Jia, Hongyang and Valavi, Hossein and Tang, Yinqi and Zhang, Jintao and Verma, Naveen},
  journal={IEEE Journal of Solid-State Circuits},
  title={A Programmable Heterogeneous Microprocessor Based on Bit-Scalable In-Memory Computing},
  year={2020},
  volume={55},
  number={9},
  pages={2609-2621},
  doi={10.1109/JSSC.2020.2987714}}
"""

from hwcomponents_library.base import LibraryEstimatorClassBase
from hwcomponents.scaling import *
from hwcomponents import action


# Original CSV contents:
# tech_node,global_cycle_period,resolution,voltage,energy,area,action
# 65nm,      540e-9,              8,         1.2,   2.25,   5000,read
# 65nm,      540e-9,              8,         1.2,   1.2,    5000,leak
# 65nm,      540e-9,              8,         1.2,   0,      5000,write|update
class JiaShiftAdd(LibraryEstimatorClassBase):
    """
    The shift-and-add unit from Jia et al. JSSC 2020. This unit will sum and accumulate
    values in a register, while also shifting the register contents to accept various
    power-of-two scaling factors for the summed values.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    resolution: int
        Resolution of the shift-and-add unit in bits. This is the number of bits of each
        input value that is added to the register.
    voltage: float
        Voltage of the shift-and-add unit in volts.
    """

    def __init__(self, tech_node: float, resolution: int = 8, voltage: float = 1.2):
        super().__init__(leak_power=2.22e-6, area=5000.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            65e-9,
            tech_node_area,
            tech_node_energy,
            noscale,
            tech_node_leak,
        )
        self.resolution: int = self.scale(
            "resolution", resolution, 8, pow_base(2), pow_base(2), noscale, pow_base(2)
        )
        self.voltage: float = self.scale(
            "voltage", voltage, 1.2, noscale, quadratic, noscale, quadratic, 1
        )

    @action
    def shift_and_add(self) -> tuple[float, float]:
        """
        Returns the energy and latency consumed by a shift+add operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """

        return 2.25e-12, 0.0

    @action
    def write(self) -> tuple[float, float]:
        """
        Returns the energy and latency consumed by a shift+add operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return self.shift_and_add()

    @action
    def read(self) -> tuple[float, float]:
        """
        Zero energy and latency to read.

        Returns
        -------
        (energy, latency): (0.0, 0.0)
        """
        return 0.0, 0.0


# Original CSV contents:
# tech_node,global_cycle_period,rows,resolution,voltage,energy,area,action
# 65nm,      540e-9,              1,   8,         1.2,   0.5,   174, read
# 65nm,      540e-9,              1,   8,         1.2,   0.2,   174, leak
# 65nm,      540e-9,              1,   8,         1.2,   0,     174, write|update
class JiaZeroGate(LibraryEstimatorClassBase):
    """
    The zero gating unit from Jia et al. JSSC 2020. This unit gates analog voltages for
    zero-valued inputs going into the rows of the crossbar array.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    rows: int
        Number of rows in the crossbar array, equal to the number of checks done by the
        zero gate.
    resolution: int
        Resolution of each input in bits.
    voltage: float
        Voltage of the zero gating unit in volts.
    """

    def __init__(
        self, tech_node: float, rows: int = 1, resolution: int = 8, voltage: float = 1.2
    ):
        super().__init__(leak_power=3.70e-7, area=174.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            65e-9,
            tech_node_area,
            tech_node_energy,
            noscale,
            tech_node_leak,
        )
        self.rows: int = self.scale("rows", rows, 1, linear, linear, noscale, linear)
        self.resolution: int = self.scale(
            "resolution", resolution, 8, linear, linear, noscale, linear
        )
        self.voltage: float = self.scale(
            "voltage", voltage, 1.2, noscale, noscale, noscale, quadratic, 1
        )

    @action(bits_per_action="resolution")
    def zero_gate(self) -> tuple[float, float]:
        """
        Returns the energy and latency consumed to zero gate & read an input.

        Parameters
        ----------
        bits_per_action: int
            The number of bits to check for zero.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.5e-12, 0.0

    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency consumed to zero gate & read an input.

        Parameters
        ----------
        bits_per_action: int
            The number of bits to check for zero.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return self.zero_gate()


# Original CSV contents:
# tech_node,global_cycle_period,voltage,energy,area,  action
# 65nm,      540e-9,              1.2,   12,     10535,read
# 65nm,      540e-9,              1.2,   2.4,    10535,leak
# 65nm,      540e-9,              1.2,   0,      10535,write|update
class JiaDatapath(LibraryEstimatorClassBase):
    """
    The datapath in Jia et al. JSSC 2020. This datapath will perform quantization and
    activation functions on accumulated ouputs.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    voltage: float
        Voltage of the datapath in volts.

    """

    def __init__(self, tech_node: float, voltage: float = 1.2):
        super().__init__(leak_power=4.44e-6, area=10535.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            65e-9,
            tech_node_area,
            tech_node_energy,
            noscale,
            tech_node_leak,
        )
        self.voltage: float = self.scale(
            "voltage", voltage, 1.2, noscale, quadratic, noscale, quadratic, 1
        )

    @action
    def process(self) -> tuple[float, float]:
        """
        Returns the energy and latency consumed by the datapath to quantize and apply
        activation functions on a single input.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 2.4e-12, 0.0

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency consumed by the datapath to quantize and apply
        activation functions on a single input.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return self.process()
