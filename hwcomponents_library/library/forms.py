"""
@INPROCEEDINGS{9499856,
  author={Yuan, Geng and Behnam, Payman and Li, Zhengang and Shafiee, Ali and Lin, Sheng and Ma, Xiaolong and Liu, Hang and Qian, Xuehai and Bojnordi, Mahdi Nazm and Wang, Yanzhi and Ding, Caiwen},
  booktitle={2021 ACM/IEEE 48th Annual International Symposium on Computer Architecture (ISCA)},
  title={FORMS: Fine-grained Polarized ReRAM-based In-situ Computation for Mixed-signal DNN Accelerator},
  year={2021},
  volume={},
  number={},
  pages={265-278},
  doi={10.1109/ISCA52012.2021.00029}}
"""

from hwcomponents_library.base import LibraryEstimatorClassBase
from hwcomponents.scaling import *
from hwcomponents import action
from .isaac import IsaacDAC


# Original CSV contents:
# tech_node,global_cycle_period,resolution,energy,area,n_instances,action
# 32nm,1e-9,4,0.22619,284.375,1,convert|read
# 32nm,1e-9,4,0,284.375,1,update|write|leak
# # Energy: 15.2*10^-3 W / (2.1*32*10^9 ADC BW) * 10 ^ 12 J->pJ
# # 15.2*10^-3 / (2.1*32*10^9) * 10 ^ 12
# # Area: 9100um^2 / 32
class FormsADC(LibraryEstimatorClassBase):
    """
    The analog-digital-converter (ADC) from the FORMS paper.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    resolution: int
        Resolution of the ADC in bits.
    """

    def __init__(self, tech_node: float, resolution: int = 4):
        super().__init__(leak_power=0.0, area=284.375e-12)
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
            "resolution", resolution, 4, pow_base(2), pow_base(2), noscale, pow_base(2)
        )

    @action
    def convert(self) -> tuple[float, float]:
        """
        Returns the energy and latency of one ADC conversion.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds)
        """
        return 0.22619e-12, 0.0

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency of one ADC conversion operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds)
        """
        return 0.22619e-12, 0.0


class FormsDAC(IsaacDAC):
    pass
