"""
@INPROCEEDINGS{7551379,
  author={Shafiee, Ali and Nag, Anirban and Muralimanohar, Naveen and Balasubramonian, Rajeev and Strachan, John Paul and Hu, Miao and Williams, R. Stanley and Srikumar, Vivek},
  booktitle={2016 ACM/IEEE 43rd Annual International Symposium on Computer Architecture (ISCA)},
  title={ISAAC: A Convolutional Neural Network Accelerator with In-Situ Analog Arithmetic in Crossbars},
  year={2016},
  volume={},
  number={},
  pages={14-26},
  doi={10.1109/ISCA.2016.12}}
"""

from hwcomponents_library.base import LibraryEstimatorClassBase
from hwcomponents.scaling import *
from hwcomponents import action


# Original CSV contents:
# tech_node,global_cycle_period,width|datawidth,depth,energy,area,action
# 32nm,1e-9,256,2048,20.45,83000,read|write|update,energy in pJ;  area in um^2;
# 32nm,1e-9,256,2048,0,83000,leak
# # Power * Time / (Reads+Writes) = Energy per read/write
# # (20.7e-3 / 12 W/IMA) power
# # (16384 / ((128*8*10^7*1.2) * 100 / 128)) time for DACs/ADCs to consume entire input buffer
# # (16384 + 2048) * 2 / 256 reads+writes, including IMA<->eDRAM<->network
# # (20.7e-3 / 12) * (16384 / ((128*8*10^7*1.2) * 100 / 128)) / ((16384 + 2048) * 2 / 256) * 1e12
class IsaacEDRAM(LibraryEstimatorClassBase):
    """
    The embedded DRAM from the ISAAC paper.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    width: int
        Width of the eDRAM in bits. This is the width of a reads/write port. Total size =
        width * depth.
    depth: int
        Depth of the eDRAM in bits. This is the number of entries in the eDRAM, each
        with `width` bits. Total size = width * depth.
    """

    def __init__(self, tech_node: float, width: int = 256, depth: int = 2048):
        super().__init__(leak_power=0.0, area=83000.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            32e-9,
            tech_node_area,
            tech_node_energy,
            noscale,
            tech_node_leak,
        )
        self.width: int = self.scale(
            "width", width, 256, linear, linear, noscale, linear
        )
        self.depth: int = self.scale(
            "depth",
            depth,
            2048,
            linear,
            cacti_depth_energy,
            noscale,
            cacti_depth_energy,
        )

    @action(bits_per_action="width")
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency of one read operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds)
        """
        return 20.45e-12, 0.0

    @action(bits_per_action="width")
    def write(self) -> tuple[float, float]:
        """
        Returns the energy and latency of one write operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds)
        """
        return 20.45e-12, 0.0


# Original CSV contents:
# tech_node,global_cycle_period,width|datawidth,energy,area,action
# 65nm,1e-9,128,26,23000000,read|write|update
# 65nm,1e-9,128,0, 23000000,leak
class IsaacChip2ChipLink(LibraryEstimatorClassBase):
    """
    The chip-to-chip link from the ISAAC paper. This connects multiple chips together.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    width: int
        Width of the link in bits. This is the width of a read/write port.
    """

    def __init__(self, tech_node: float, width: int = 128):
        super().__init__(leak_power=0.0, area=23000000.0e-12)
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

    @action(bits_per_action="width")
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency of one read operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds)
        """
        return 26.0e-12, 0.0

    @action(bits_per_action="width")
    def write(self) -> tuple[float, float]:
        """
        Returns the energy and latency of one write operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds)
        """
        return 26.0e-12, 0.0


# Original CSV contents:
# tech_node,global_cycle_period,width|datawidth,energy,area,action
# 32nm,1e-9,256,20.74,37500,read,energy in pJ;  area in um^2;
# 32nm,1e-9,256,0,37500,leak|update|write
# # To match the paper where ISAAC shares each of these between 4 tiles. Quarter the area
# # relative to isaac_router
# # Assuming router BW = eDRAM BW per tile
# # Power * Time / (Reads+Writes) = Energy per read/write
# # (42e-3 / 4 / 12) power
# # (16384 / ((128*8*10^7*1.2) * 100 / 128)) time for DACs/ADCs to consume entire input buffer
# # (16384 + 2048) / 256 reads+writes
# # (42e-3 / 4 / 12) * (16384 / ((128*8*10^7*1.2) * 100 / 128)) / ((16384 + 2048) / 256) * 1e12
class IsaacRouterSharedByFour(LibraryEstimatorClassBase):
    """
    This is the router from the ISAAC paper. In the paper, it is shared by four tiles,
    so this area is divided by four to match the paper.
    """

    def __init__(self, tech_node: float, width: int = 256):
        super().__init__(leak_power=0.0, area=37500.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            32e-9,
            tech_node_area,
            tech_node_energy,
            noscale,
            tech_node_leak,
        )
        self.width: int = self.scale(
            "width", width, 256, linear, linear, noscale, linear
        )

    @action(bits_per_action="width")
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency to transfer data.

        Parameters
        ----------
        bits_per_action: int
            The number of bits transferred.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds)
        """
        return self.transfer()

    @action(bits_per_action="width")
    def write(self) -> tuple[float, float]:
        """
        Write returns zero because transfer costs are already included in the read energy.

        Parameters
        ----------
        bits_per_action: int
            The number of bits transferred.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds)
        """
        return 0.0, 0.0

    @action(bits_per_action="width")
    def transfer(self) -> tuple[float, float]:
        """
        Returns the energy and latency to transfer data.

        Parameters
        ----------
        bits_per_action: int
            The number of bits transferred.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds)
        """
        return 20.74e-12, 0.0


# Original CSV contents:
# tech_node,global_cycle_period,resolution,energy,area,n_instances,action
# 32nm,1e-9,8,1.666666667,1200,1,convert|read
# 32nm,1e-9,8,0,1200,1,leak|update|write
# # Energy: 16*10^-3 W / (1.2*8*10^9 ADC BW) * 10 ^ 12 J->pJ
# # 16*10^-3 / (1.2*8*10^9) * 10 ^ 12
# # Area: 9600um^2 / 8
# # L. Kull et al.," ""A 3.1mW 8b 1.2GS/s single-channel asynchronous SAR ADC
# # with alternate comparators for enhanced speed in 32nm digital SOI
# # CMOS",2013,pp. 468-469,doi: 10.1109/ISSCC.2013.6487818.," 2013 IEEE
# # International Solid-State Circuits Conference Digest of Technical Papers
# # Below are scaled versions based on M. Saberi, R. Lotfi, K. Mafinezhad, W.
# # Serdijn et al., “Analysis of Power Consumption and Linearity in Capacitive
# # Digital-to-Analog Converters used in Successive Approximation ADCs,” 2011.
# # 32nm,1e-9,4,0.79,361.04,1,convert|read
# # 32nm,1e-9,5,0.99,476.91,1,convert|read
# # 32nm,1e-9,6,1.20,626.91,1,convert|read
# # 32nm,1e-9,7,1.42,845.18,1,convert|read
# # 32nm,1e-9,8,1.67,1200,1,convert|read
# # 32nm,1e-9,9,1.969078145,1827.911647,1,convert|read
# # 32nm,1e-9,10,2.379022742,3002.008032,1,convert|read
class IsaacADC(LibraryEstimatorClassBase):
    """
    The analog-digital-converter (ADC) from the ISAAC paper.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    resolution: int
        Resolution of the ADC in bits.
    """

    def __init__(self, tech_node: float, resolution: int = 8):
        super().__init__(leak_power=0.0, area=1200.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            32e-9,
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
        Returns the energy and latency of one ADC conversion.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds)
        """
        return 1.666666667e-12, 0.0

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency of one ADC conversion.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds)
        """
        return 1.666666667e-12, 0.0


# Original CSV contents:
# tech_node,global_cycle_period,width|datawidth,energy,area,action
# 32nm,1e-9,256,20.74,150000,read,energy in pJ;  area in um^2;
# 32nm,1e-9,256,0,150000,leak|update|write
# # ISAAC shares each of these between 4 tiles
# # Assuming router BW = eDRAM BW per tile
# # Power * Time / (Reads+Writes) = Energy per read/write
# # (42e-3 / 4 / 12) power
# # (16384 / ((128*8*10^7*1.2) * 100 / 128)) time for DACs/ADCs to consume entire input buffer
# # (16384 + 2048) / 256 reads+writes
# # (42e-3 / 4 / 12) * (16384 / ((128*8*10^7*1.2) * 100 / 128)) / ((16384 + 2048) / 256) * 1e12
class IsaacRouter(LibraryEstimatorClassBase):
    """
    The router from the ISAAC paper. This is the router shared by four tiles in the
    paper, so divide this area by four if you'd like to get the per-tile area from the
    paper.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    width: int
        Width of the router in bits. This is the width of a read/write port.
    """

    def __init__(self, tech_node: float, width: int = 256):
        super().__init__(leak_power=0.0, area=150000.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            32e-9,
            tech_node_area,
            tech_node_energy,
            noscale,
            tech_node_leak,
        )
        self.width: int = self.scale(
            "width", width, 256, linear, linear, noscale, linear
        )

    @action(bits_per_action="width")
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency to transfer data.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds)
        """
        return self.transfer()

    @action(bits_per_action="width")
    def write(self) -> tuple[float, float]:
        """
        Returns the energy and latency to transfer data.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.0, 0.0

    @action(bits_per_action="width")
    def transfer(self) -> tuple[float, float]:
        """
        Returns the energy and latency to transfer data.

        Parameters
        ----------
        bits_per_action: int
            The number of bits transferred.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 20.74e-12, 0.0


# Original CSV contents:
# tech_node,global_cycle_period,width|datawidth,energy,area,action
# 32nm,1e-9,16,0.021,60,shift_add|read|write,energy in pJ;  area in um^2
# 32nm,1e-9,16,0.00E+00,60,leak|update
# # Energy: 16*10^-3 W / (1.2*8*10^9 ADC BW) * 10 ^ 12 J->pJ
# # Energy: .2e-3 W / (1.2*8*10^9 ADC BW) * 10 ^ 12 J->pJ
# # .2e-3 / (1.2*8*10^9) * 10 ^ 12
# # There are 4 of these in an ISAAC IMA
class IsaacShiftAdd(LibraryEstimatorClassBase):
    """
    The shift-and-add unit from the ISAAC paper. This unit will sum and accumulate
    values in a register, while also shifting the register contents to accept various
    power-of-two scaling factors for the summed values.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    width: int
        Width of the shift-and-add unit in bits. This is the number of bits of each
        input value that is added to the register.
    """

    def __init__(self, tech_node: float, width: int = 16):
        super().__init__(leak_power=0.0, area=60.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            32e-9,
            tech_node_area,
            tech_node_energy,
            noscale,
            tech_node_leak,
        )
        self.width: int = self.scale(
            "width", width, 16, linear, linear, noscale, linear
        )

    @action
    def shift_add(self) -> tuple[float, float]:
        """
        Returns the energy and latency of one shift-and-add operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.021e-12, 0.0

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency to read the shift-and-add unit's output.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.0, 0.0

    @action
    def write(self) -> tuple[float, float]:
        """
        Returns the energy and latency of one shift-and-add operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.021e-12, 0.0


# Original CSV contents:
# tech_node,global_cycle_period,width|datawidth,energy,area,action
# 32nm,1e-9,1,0.054,29.296875,read,energy in pJ;  area in um^2;
# 32nm,1e-9,1,0,29.296875,leak|update|write,energy in pJ;  area in um^2;
# # Power * Time / (Reads+Writes) = Energy per read/write
# # (7e-3 / 12 W/IMA) power
# # (16384 / ((128*8*10^7*1.2) * 100 / 128)) time for DACs/ADCs to consume entire input buffer
# # (16384 + 2048) * reads+writes
# # (7e-3 / 12) * (16384 / ((128*8*10^7*1.2) * 100 / 128)) / ((16384 + 2048)) * 1e12
# # Assuming bus BW = eDRAM BW
# # Area reported per IMA. In ISAAC, a bus connects 12 IMAs
# # Area: 7500 / (Width 256) = 29.296875 um^2 per bit width
class IsaacEDRAMBus(LibraryEstimatorClassBase):
    """
    The eDRAM bus from the ISAAC paper. This bus connects the eDRAM to the router.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    width: int
        Width of the eDRAM bus in bits. This is the width of a read/write port.
    """

    def __init__(self, tech_node: float, width: int = 1):
        super().__init__(leak_power=0.0, area=29.296875e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            32e-9,
            tech_node_area,
            tech_node_energy,
            noscale,
            tech_node_leak,
        )
        self.width: int = self.scale("width", width, 1, linear, linear, noscale, linear)

    @action(bits_per_action="width")
    def read(self) -> float:
        """
        Returns the energy to read the eDRAM bus in Joules.

        Parameters
        ----------
        bits_per_action: int
            The number of bits transferred.

        Returns
        -------
        float
            Energy to read the eDRAM bus in Joules
        """
        return self.transfer()

    @action(bits_per_action="width")
    def transfer(self) -> float:
        """
        Returns the energy to transfer data in Joules.

        Parameters
        ----------
        bits_per_action: int
            The number of bits transferred.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds)
        """
        return 0.054e-12, 0.0

    @action(bits_per_action="width")
    def write(self) -> tuple[float, float]:
        """
        Returns zero because transfer costs are already included in the read energy.

        Parameters
        ----------
        bits_per_action: int
            The number of bits transferred.

        Returns
        -------
        (energy, latency): (0.0, 0.0)
        """
        return 0.0, 0.0


# Original CSV contents:
# tech_node,global_cycle_period,resolution,energy,area,rows,action
# 32nm,1e-9,1,0.41667,0.166015625,1,drive|read
# 32nm,1e-9,1,0,0.166015625,1,write|leak|update
# # Energy: 4*10^-3 W / (128*8*10^7*1.2 DAC BW) * 10 ^ 12 J->pJ * 128/100 underutilized due to ADC
# # 4e-3 / (128 * 8 * 1.2 * 10 ^ 7) * 10 ^ 12 * 128/100
# # 0.3255 * 8 * 128 * 1.2e9 / 100 * 1e-9
# # Area: 170um^2 / 128 / 8
class IsaacDAC(LibraryEstimatorClassBase):
    """
    The digital-analog converter (DAC) from the ISAAC paper.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    resolution: int
        Resolution of the DAC in bits.
    """

    def __init__(self, tech_node: float, resolution: int = 1, rows: int = 1):
        super().__init__(leak_power=0.0, area=0.166015625e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            32e-9,
            tech_node_area,
            tech_node_energy,
            noscale,
            tech_node_leak,
        )
        self.resolution: int = self.scale(
            "resolution", resolution, 1, pow_base(2), pow_base(2), noscale, pow_base(2)
        )
        self.rows: int = self.scale("rows", rows, 1, linear, noscale, noscale, linear)

    @action
    def convert(self) -> tuple[float, float]:
        """
        Returns the energy and latency to convert with the the DAC.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds)
        """
        return 0.41667e-12, 0.0

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency to read the DAC.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds)
        """
        return 0.41667e-12, 0.0
