"""
@ARTICLE{9131838,
  author={Giterman, Robert and Shalom, Amir and Burg, Andreas and Fish, Alexander and Teman, Adam},
  journal={IEEE Solid-State Circuits Letters},
  title={A 1-Mbit Fully Logic-Compatible 3T Gain-Cell Embedded DRAM in 16-nm FinFET},
  year={2020},
  volume={3},
  number={},
  pages={110-113},
  keywords={Random access memory;FinFETs;Temperature measurement;Leakage currents;Power demand;Voltage measurement;Embedded DRAM;gain cell (GC);low voltage;retention time;SRAM},
  doi={10.1109/LSSC.2020.3006496}}
"""

from hwcomponents_library.base import LibraryEstimatorClassBase
from hwcomponents.scaling import *
from hwcomponents import action
from hwcomponents_cacti import SRAM
from hwcomponents_library.library.aladdin import AladdinRegister, AladdinAdder


# Original CSV contents:
# tech_node,global_cycle_period,width|datawidth,depth,energy,area,action
# 16nm,1e-9,1024,1024,2641.92,131570,read
# 16nm,1e-9,1024,1024,2519.04,131570,write|update
# 16nm,1e-9,1024,1024,0.381,131570,leak
# # Read: 2.58 uW / MHz
# # Write: 2.46 uW / MHz
# # Leak + Refresh: (105uw leak) + (276uW refresh) = 381uW
# # @ARTICLE{9131838,
# #   author={Giterman, Robert and Shalom, Amir and Burg, Andreas and Fish, Alexander and Teman, Adam},
# #   journal={IEEE Solid-State Circuits Letters},
# #   title={A 1-Mbit Fully Logic-Compatible 3T Gain-Cell Embedded DRAM in 16-nm FinFET},
# #   year={2020},
# #   volume={3},
# #   number={},
# #   pages={110-113},
# #   keywords={Random access memory;FinFETs;Temperature measurement;Leakage currents;Power demand;Voltage measurement;Embedded DRAM;gain cell (GC);low voltage;retention time;SRAM},
# #   doi={10.1109/LSSC.2020.3006496}}
class RaaamEDRAM(LibraryEstimatorClassBase):
    """
    RAAAM EDRAM from Giterman et al. LSSC 2020. This is a MB-class embedded DRAM unit.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    width: int
        Width of the eDRAM in bits. This is the width of a read/write port. Total size =
        width * depth.
    depth: int
        The number of entries in the eDRAM, each with `width` bits. Total size = width *
        depth.
    """

    def __init__(self, tech_node: float, width: int = 1024, depth: int = 1024):
        super().__init__(leak_power=3.81e-4, area=131570.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            16e-9,
            tech_node_area,
            tech_node_energy,
            noscale,
            tech_node_leak,
        )
        self.width: int = self.scale(
            "width", width, 1024, linear, linear, noscale, linear
        )
        self.depth: int = self.scale(
            "depth",
            depth,
            1024,
            linear,
            cacti_depth_energy,
            noscale,
            cacti_depth_energy,
        )

    @action(bits_per_action="width")
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency consumed by a read operation.

        Parameters
        ----------
        bits_per_action: int
            The number of bits to read.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 2641.92e-12, 0.0

    @action(bits_per_action="width")
    def write(self) -> tuple[float, float]:
        """
        Returns the energy and latency consumed by a write operation.

        Parameters
        ----------
        bits_per_action: int
            The number of bits to write.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 2519.04e-12, 0.0


class SmartBufferSRAM(LibraryEstimatorClassBase):
    """
    An SRAM with an address generator that sequentially reads addresses in the SRAM.

    Parameters
    ----------
        tech_node: The technology node in meters.
        width: The width of the read and write ports in bits. This is the number of bits
            that are accssed by any one read/write. Total size = width * depth.
        depth: The number of entries in the SRAM, each with `width` bits. Total size =
            width * depth.
        n_rw_ports: The number of read/write ports. Bandwidth will increase with more
            ports.
        n_banks: The number of banks. Bandwidth will increase with more banks.

    Attributes
    ----------
        sram: The SRAM buffer.
        address_reg: The register that holds the current address.
        delta_reg: The register that holds the increment value.
        adder: The adder that adds the increment value to the current address.
    """

    component_name = ["smart_buffer_sram", "smartbuffer_sram", "smartbuffersram"]
    priority = 0.3

    def __init__(
        self,
        tech_node: float,
        width: int,
        depth: int,
        n_rw_ports: int = 1,
        n_banks: int = 1,
    ):
        self.sram: SRAM = SRAM(
            tech_node=tech_node,
            width=width,
            depth=depth,
            n_rw_ports=n_rw_ports,
            n_banks=n_banks,
        )
        self.address_bits = max(math.ceil(math.log2(depth)), 1)
        self.width = width
        self.depth = depth
        self.n_rw_ports = n_rw_ports
        self.n_banks = n_banks

        self.address_reg = AladdinRegister(width=self.address_bits, tech_node=tech_node)
        self.delta_reg = AladdinRegister(width=self.address_bits, tech_node=tech_node)
        self.adder = AladdinAdder(width=self.address_bits, tech_node=tech_node)

        super().__init__(
            subcomponents=[
                self.sram,
                self.address_reg,
                self.delta_reg,
                self.adder,
            ]
        )

    @action(bits_per_action="width")
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency consumed by a read operation.

        Parameters
        ----------
        bits_per_action: int
            The number of bits to read.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        self.sram.read(bits_per_action=self.width)
        self.address_reg.read()
        self.delta_reg.read()
        self.adder.add()
        return 0.0, 0.0

    @action(bits_per_action="width")
    def write(self) -> tuple[float, float]:
        """
        Returns the energy and latency consumed by a write operation.

        Parameters
        ----------
        bits_per_action: int
            The number of bits to write.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        self.sram.write(bits_per_action=self.width)
        self.address_reg.write()
        self.delta_reg.read()
        self.adder.add()
        return 0.0, 0.0
