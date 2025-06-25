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
from hwcomponents import actionDynamicEnergy


# Original CSV contents:
# tech_node,global_cycle_seconds,width|datawidth,depth,energy,area,action
# 32nm,1e-9,256,2048,20.45,83000,read|write|update,energy in pJ;  area in um^2;
# 32nm,1e-9,256,2048,0,83000,leak
# # Power * Time / (Reads+Writes) = Energy per read/write
# # (20.7e-3 / 12 W/IMA) power
# # (16384 / ((128*8*10^7*1.2) * 100 / 128)) time for DACs/ADCs to consume entire input buffer
# # (16384 + 2048) * 2 / 256 reads+writes, including IMA<->eDRAM<->network
# # (20.7e-3 / 12) * (16384 / ((128*8*10^7*1.2) * 100 / 128)) / ((16384 + 2048) * 2 / 256) * 1e12
class IsaacEDRAM(LibraryEstimatorClassBase):
    component_name = "isaac_eDRAM"
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str, width: int = 256, depth: int = 2048):
        super().__init__(leak_power=0.0, area=83000.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            32e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.width: int = self.scale("width", width, 256, linear, linear, linear)
        self.depth: int = self.scale(
            "depth", depth, 2048, linear, cacti_depth_energy, cacti_depth_energy
        )

    @actionDynamicEnergy
    def read(self) -> float:
        return 20.45e-12

    @actionDynamicEnergy
    def write(self) -> float:
        return 20.45e-12


# Original CSV contents:
# tech_node,global_cycle_seconds,width|datawidth,energy,area,action
# 65nm,1e-9,128,26,23000000,read|write|update
# 65nm,1e-9,128,0, 23000000,leak
class IsaacChip2ChipLink(LibraryEstimatorClassBase):
    component_name = "isaac_chip2chip_link"
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str, width: int = 128):
        super().__init__(leak_power=0.0, area=23000000.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            65e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.width: int = self.scale("width", width, 128, linear, linear, linear)

    @actionDynamicEnergy
    def read(self) -> float:
        return 26.0e-12

    @actionDynamicEnergy
    def write(self) -> float:
        return 26.0e-12


# Original CSV contents:
# tech_node,global_cycle_seconds,width|datawidth,energy,area,action
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
    component_name = "isaac_router_shared_by_four"
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str, width: int = 256):
        super().__init__(leak_power=0.0, area=37500.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            32e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.width: int = self.scale("width", width, 256, linear, linear, linear)

    @actionDynamicEnergy
    def read(self) -> float:
        return 20.74e-12


# Original CSV contents:
# tech_node,global_cycle_seconds,resolution,energy,area,n_instances,action
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
class IsaacAdc(LibraryEstimatorClassBase):
    component_name = "isaac_adc"
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str, resolution: int = 8):
        super().__init__(leak_power=0.0, area=1200.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            32e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.resolution: int = self.scale(
            "resolution", resolution, 8, pow_base(2), pow_base(2), pow_base(2)
        )

    @actionDynamicEnergy
    def convert(self) -> float:
        return 1.666666667e-12

    @actionDynamicEnergy
    def read(self) -> float:
        return 1.666666667e-12


# Original CSV contents:
# tech_node,global_cycle_seconds,width|datawidth,energy,area,action
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
    component_name = "isaac_router"
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str, width: int = 256):
        super().__init__(leak_power=0.0, area=150000.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            32e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.width: int = self.scale("width", width, 256, linear, linear, linear)

    @actionDynamicEnergy
    def read(self) -> float:
        return 20.74e-12


# Original CSV contents:
# tech_node,global_cycle_seconds,width|datawidth,energy,area,action
# 32nm,1e-9,16,0.021,60,shift_add|read|write,energy in pJ;  area in um^2
# 32nm,1e-9,16,0.00E+00,60,leak|update
# # Energy: 16*10^-3 W / (1.2*8*10^9 ADC BW) * 10 ^ 12 J->pJ
# # Energy: .2e-3 W / (1.2*8*10^9 ADC BW) * 10 ^ 12 J->pJ
# # .2e-3 / (1.2*8*10^9) * 10 ^ 12
# # There are 4 of these in an ISAAC IMA
class IsaacShiftAdd(LibraryEstimatorClassBase):
    component_name = "isaac_shift_add"
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str, width: int = 16):
        super().__init__(leak_power=0.0, area=60.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            32e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.width: int = self.scale("width", width, 16, linear, linear, linear)

    @actionDynamicEnergy
    def shift_add(self) -> float:
        return 0.021e-12

    @actionDynamicEnergy
    def read(self) -> float:
        return 0.021e-12

    @actionDynamicEnergy
    def write(self) -> float:
        return 0.021e-12


# Original CSV contents:
# tech_node,global_cycle_seconds,width|datawidth,energy,area,action
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
    component_name = "isaac_eDRAM_bus"
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str, width: int = 1):
        super().__init__(leak_power=0.0, area=29.296875e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            32e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.width: int = self.scale("width", width, 1, linear, linear, linear)

    @actionDynamicEnergy
    def read(self) -> float:
        return 0.054e-12


# Original CSV contents:
# tech_node,global_cycle_seconds,resolution,energy,area,rows,action
# 32nm,1e-9,1,0.41667,0.166015625,1,drive|read
# 32nm,1e-9,1,0,0.166015625,1,write|leak|update
# # Energy: 4*10^-3 W / (128*8*10^7*1.2 DAC BW) * 10 ^ 12 J->pJ * 128/100 underutilized due to ADC
# # 4e-3 / (128 * 8 * 1.2 * 10 ^ 7) * 10 ^ 12 * 128/100
# # 0.3255 * 8 * 128 * 1.2e9 / 100 * 1e-9
# # Area: 170um^2 / 128 / 8
class IsaacDac(LibraryEstimatorClassBase):
    component_name = "isaac_dac"
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str, resolution: int = 1, rows: int = 1):
        super().__init__(leak_power=0.0, area=0.166015625e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            32e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.resolution: int = self.scale(
            "resolution", resolution, 1, pow_base(2), pow_base(2), pow_base(2)
        )
        self.rows: int = self.scale("rows", rows, 1, linear, noscale, noscale)

    @actionDynamicEnergy
    def drive(self) -> float:
        return 0.41667e-12

    @actionDynamicEnergy
    def read(self) -> float:
        return 0.41667e-12
