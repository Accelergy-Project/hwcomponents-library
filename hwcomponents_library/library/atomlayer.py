"""
@INPROCEEDINGS{8465832,
  author={Qiao, Ximing and Cao, Xiong and Yang, Huanrui and Song, Linghao and Li, Hai},
  booktitle={2018 55th ACM/ESDA/IEEE Design Automation Conference (DAC)},
  title={AtomLayer: A Universal ReRAM-Based CNN Accelerator with Atomic Layer Computation},
  year={2018},
  volume={},
  number={},
  pages={1-6},
  doi={10.1109/DAC.2018.8465832}}
"""

from hwcomponents_library.base import LibraryEstimatorClassBase
from hwcomponents.scaling import *
from hwcomponents import actionDynamicEnergy
from .isaac import IsaacADC
from .isaac import IsaacDAC
from .isaac import IsaacEDRAM
from .isaac import IsaacEDRAMBus
from .isaac import IsaacRouter
from .isaac import IsaacShiftAdd


# Original CSV contents:
# tech_node,global_cycle_period,width|datawidth,depth,energy,area,action
# 32nm,1e-9,16,128,0.083,1620,read|write,energy in pJ;  area in um^2;
# 32nm,1e-9,16,128,0,1620,update|leak
# # 1 read, 1 write per DAC activation
# # Reported power = 0.39 / 4 x DAC
# # 0.166015625 / 2 = 0.083
class AtomlayerRegisterLadder(LibraryEstimatorClassBase):
    component_name = "atomlayer_register_ladder"
    priority = 0.9

    def __init__(self, tech_node: str, width: int = 16, depth: int = 128):
        super().__init__(leak_power=0.0, area=1620.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            32e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.width: int = self.scale("width", width, 16, linear, linear, linear)
        self.depth: int = self.scale(
            "depth", depth, 128, linear, cacti_depth_energy, cacti_depth_energy
        )

    @actionDynamicEnergy(bits_per_action="width")
    def read(self) -> float:
        return 0.083e-12

    @actionDynamicEnergy(bits_per_action="width")
    def write(self) -> float:
        return 0.083e-12


# Original CSV contents:
# tech_node,global_cycle_period,width|datawidth,depth,energy,area,action
# 32nm,1e-9,16,128,6.46,2100,read, energy in pJ;  area in um^2;
# 32nm,1e-9,16,128,0,2100,write|update|leak
# # Power calculation for input buffers:
# # Power * Time / (Reads+Writes) = Energy per read/write
# # (1.24e-3 W) power * (16 * 100e-9s time/MAC / 1.2) / (128+128 reads+writes)
# # (1.24e-3) * (16 * 100e-9 / 1.2) / (128+128) * 1e12
# # Now for the transfers calculation, we also mark write energy = 0 so we don't
# # double charge for writes with the actual buffers. Only charge for reads when
# # another
# # buffer reads from the inter-buffer transfer network.
class AtomlayerInputBufferTransfers(LibraryEstimatorClassBase):
    component_name = "atomlayer_input_buffer_transfers"
    priority = 0.9

    def __init__(self, tech_node: str, width: int = 16, depth: int = 128):
        super().__init__(leak_power=0.0, area=2100.0e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            32e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.width: int = self.scale("width", width, 16, linear, linear, linear)
        self.depth: int = self.scale(
            "depth", depth, 128, linear, cacti_depth_energy, cacti_depth_energy
        )

    @actionDynamicEnergy(bits_per_action="width")
    def read(self) -> float:
        return 6.46e-12


class AtomlayerADC(IsaacADC):
    pass


class AtomlayerDAC(IsaacDAC):
    pass


class AtomlayerRouter(IsaacRouter):
    pass


class AtomlayerEDRAM(IsaacEDRAM):
    pass


class AtomlayerEDRAMBus(IsaacEDRAMBus):
    pass


class AtomlayerShiftAdd(IsaacShiftAdd):
    pass
