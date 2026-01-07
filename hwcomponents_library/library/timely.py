"""
@INPROCEEDINGS{9138916,
  author={Li, Weitao and Xu, Pengfei and Zhao, Yang and Li, Haitong and Xie, Yuan and Lin, Yingyan},
  booktitle={2020 ACM/IEEE 47th Annual International Symposium on Computer Architecture (ISCA)},
  title={Timely: Pushing Data Movements And Interfaces In Pim Accelerators Towards Local And In Time Domain},
  year={2020},
  volume={},
  number={},
  pages={832-845},
  doi={10.1109/ISCA45697.2020.00073}}
"""

from hwcomponents_library.base import LibraryEstimatorClassBase
from hwcomponents.scaling import *
from hwcomponents import action
from .isaac import IsaacChip2ChipLink


# Original CSV contents:
# tech_node,global_cycle_period,energy,area,action
# 65nm,1e-9,0.0368,40,read|add
# 65nm,1e-9,0,40,write|update|leak
# # TIMELY says these don't contribute to area
# # Numbers from paper table II
class TimelyIAdder(LibraryEstimatorClassBase):
    """
    The current adder from the TIMELY paper. This unit will sum multiple currents into
    one.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    """

    def __init__(self, tech_node: float):
        super().__init__(leak_power=0.0, area=40.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            65e-9,
            tech_node_area,
            tech_node_energy,
            noscale,
            tech_node_leak,
        )

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency used to sum two currents.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """

        return 0.0368e-12, 0.0

    @action
    def add(self) -> tuple[float, float]:
        """
        Returns the energy and latency used to sum two currents.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """

        return 0.0368e-12, 0.0


# Original CSV contents:
# tech_node,global_cycle_period,n_instances,energy,area,action
# 65nm,1e-9,1,0.0023,5,drive|read|convert
# 65nm,1e-9,1,0,5,leak|update|write
# # Numbers from paper table II
class TimelyPSubBuf(LibraryEstimatorClassBase):
    """
    PSubBuf from the TIMELY paper. This unit will repeat & amplify an input voltage
    value.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    """

    def __init__(self, tech_node: float):
        super().__init__(leak_power=0.0, area=5.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            65e-9,
            tech_node_area,
            tech_node_energy,
            noscale,
            tech_node_leak,
        )

    @action
    def drive(self) -> tuple[float, float]:
        """
        Returns the energy and latency used to drive a voltage.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.0023e-12, 0.0

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency used to drive a voltage.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.0023e-12, 0.0


# Original CSV contents:
# tech_node,global_cycle_period,resolution,energy,area,action
# 65nm,1e-9,8,0.0375,240,convert|read
# 65nm,1e-9,8,0,240,write|leak|update
# # Numbers from paper table II
class TimelyDTC(LibraryEstimatorClassBase):
    """
    The digital-to-time converter (DTC) from the TIMELY paper. This unit will convert
    a digital value into a pulse width modulated (PWM) signal.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    resolution: int
        Resolution of the DTC in bits.
    """

    def __init__(self, tech_node: float, resolution: int = 8):
        super().__init__(leak_power=0.0, area=240.0e-12)
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

    @action
    def convert(self) -> tuple[float, float]:
        """
        Returns the energy and latency used to convert a digital value into a PWM signal.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.0375e-12, 0.0

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency used to convert a digital value into a PWM signal.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.0375e-12, 0.0


# Original CSV contents:
# tech_node,global_cycle_period,resolution,energy,area,action
# 65nm,1e-9,8,0.145,310,convert|read
# 65nm,1e-9,8,0,310,leak|write|update
class TimelyTDC(LibraryEstimatorClassBase):
    """
    The time-to-digital converter (TDC) from the TIMELY paper. This unit will convert
    a pulse width modulated (PWM) signal into a digital value.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    resolution: int
        Resolution of the TDC in bits.
    """

    def __init__(self, tech_node: float, resolution: int = 8):
        super().__init__(leak_power=0.0, area=310.0e-12)
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

    @action
    def convert(self) -> tuple[float, float]:
        """
        Returns the energy and latency used to convert a PWM signal into a digital value.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.145e-12, 0.0

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency used to convert a PWM signal into a digital value.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.145e-12, 0.0


# Original CSV contents:
# tech_node,global_cycle_period,rows,energy,area,action
# 65nm,1e-9,1,0.00062,5,read|drive|buffer
# 65nm,1e-9,1,0,5,leak|write|update
# # Numbers from paper table II
class TimelyXSubBuf(LibraryEstimatorClassBase):
    """
    The XSubBuf from the TIMELY paper. This unit will repeat & amplify an input current
    value.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    rows: int
        Number of rows of the CiM array that are applying current to the XSubBuf. Power
        will increase with more rows.
    """

    def __init__(self, tech_node: float, rows: int = 1):
        super().__init__(leak_power=0.0, area=5.0e-12)
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

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency used to repeat & amplify an input current.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.00062e-12, 0.0

    @action
    def drive(self) -> tuple[float, float]:
        """
        Returns the energy and latency used to repeat & amplify an input current.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.00062e-12, 0.0


# Original CSV contents:
# tech_node,global_cycle_period,energy,area,action
# 65nm,1e-9,0.0417,40,compare|read
# 65nm,1e-9,0,40,write|update|leak
# # Numbers from paper table II
class TimelyChargingComparator(LibraryEstimatorClassBase):
    """
    The charging comparator from the TIMELY paper. This unit will accumulate charge on a
    capacitor and trigger a singal once it exceed a reference charge.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    """

    def __init__(self, tech_node: float):
        super().__init__(leak_power=0.0, area=40.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            65e-9,
            tech_node_area,
            tech_node_energy,
            noscale,
            tech_node_leak,
        )

    @action
    def compare(self) -> tuple[float, float]:
        """
        Returns the energy and latency used to compare an input to the reference.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.0417e-12, 0.0

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency used to compare an input to the reference.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.0417e-12, 0.0


# Original CSV contents:
# tech_node,global_cycle_period,width|datawidth,depth,energy,area,action
# 65nm,1e-9,128,128,203.776,40,read
# 65nm,1e-9,128,128,496.624,40,write|update
# 65nm,1e-9,128,128,0,40,leak
class TimelyInputOutputBuffer(LibraryEstimatorClassBase):
    """
    The input/output buffers from the TIMELY paper. These digital buffers store inputs and outputs to the CiM arrays.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    width : int, optional
        The width of the read/write port of the buffer in bits. Total size = width * depth.
    depth: int
        The number of entries in the buffer, each with `width` bits. Total size = width
        * depth.
    """

    def __init__(self, tech_node: float, width: int = 128, depth: int = 128):
        super().__init__(leak_power=0.0, area=40.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            65e-9,
            tech_node_area,
            tech_node_energy,
            noscale,
            tech_node_leak,
        )
        self.width: int = self.scale(
            "width", width, 128, linear, linear, noscale, linear
        )
        self.depth: int = self.scale(
            "depth", depth, 128, linear, cacti_depth_energy, noscale, cacti_depth_energy
        )

    @action(bits_per_action="width")
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency used to read from the buffer.

        Parameters
        ----------
        bits_per_action: int
            The number of bits to read.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 203.776e-12, 0.0

    @action(bits_per_action="width")
    def write(self) -> tuple[float, float]:
        """
        Returns the energy and latency used to write to the buffer.

        Parameters
        ----------
        bits_per_action: int
            The number of bits to write.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 496.624e-12, 0.0


class TimelyChip2ChipLink(IsaacChip2ChipLink):
    pass
