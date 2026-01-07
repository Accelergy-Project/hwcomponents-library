"""
@ARTICLE{8474954,
  author={Nag, Anirban and Balasubramonian, Rajeev and Srikumar, Vivek and Walker, Ross and Shafiee, Ali and Strachan, John Paul and Muralimanohar, Naveen},
  journal={IEEE Micro},
  title={Newton: Gravitating Towards the Physical Limits of Crossbar Acceleration},
  year={2018},
  volume={38},
  number={5},
  pages={41-49},
  doi={10.1109/MM.2018.053631140}}
"""

from hwcomponents_library.base import LibraryEstimatorClassBase
from hwcomponents.scaling import *
from hwcomponents import action
from .isaac import IsaacADC
from .isaac import IsaacDAC
from .isaac import IsaacEDRAM
from .isaac import IsaacEDRAMBus
from .isaac import IsaacRouter
from .isaac import IsaacShiftAdd


# Original CSV contents:
# tech_node,global_cycle_period,resolution,energy,area,action
# 32nm,1e-9,9,2.58333333333,1500,convert|read
# 32nm,1e-9,9,0,1500,write|update|leak
# # Energy: 3.1*10^-3 W / (1.2*10^9 ADC BW) * 10 ^ 12 J->pJ
# # Newton's adapative ADC resolution table:
# # 9,9,7,5,1,0,9,3
# # 9,9,8,6,2,0,9,4
# # 9,9,9,7,3,1,9,5
# # 9,9,9,8,4,2,9,6
# # 8,9,9,9,5,3,9,7
# # 7,9,9,9,6,4,9,8
# # 6,8,9,9,7,5,9,9
# # 5,7,9,9,8,6,9,9
# # 4,6,9,9,9,7,8,9
# # 3,5,9,9,9,8,7,9
# # 2,4,8,9,9,9,6,9
# # 1,3,7,9,9,9,5,9
# # 0,2,6,8,9,9,4,9
# # 0,1,5,7,9,9,3,9
# # 0,0,4,6,9,9,2,8
# # 0,0,3,5,9,9,1,7
# # Newton assumes a linear scaling: 9-bit ADC uses X/9 power for X-bit convert.
# # Matches with the table above:
# #    Sum of this table is 832. Sum of full-resolution (all table entries = 9)
# #    is 1152. This is a 40% reduction, matching with the reported 40%
# #    ADC power reduction in the paper.
class NewtonADC(LibraryEstimatorClassBase):
    """
    The ADC from the Newton paper. This is a 9-bit ADC that can optionally stop
    quantizing after a certain number of bits.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    resolution: int
        Resolution of the ADC in bits.
    """

    def __init__(self, tech_node: float, resolution: int = 9):
        super().__init__(leak_power=0.0, area=1500.0e-12)
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
            "resolution", resolution, 9, pow_base(2), noscale, pow_base(2), pow_base(2)
        )

    @action
    def convert(self) -> tuple[float, float]:
        """
        Returns the energy and latency consumed by a convert operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 2.58333333333e-12, 0.0

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency consumed by a convert operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 2.58333333333e-12, 0.0


class NewtonADC(IsaacADC):
    pass


class NewtonDAC(IsaacDAC):
    pass


class NewtonRouter(IsaacRouter):
    pass


class NewtonEDRAM(IsaacEDRAM):
    pass


class NewtonEDRAMBus(IsaacEDRAMBus):
    pass


class NewtonShiftAdd(IsaacShiftAdd):
    pass
