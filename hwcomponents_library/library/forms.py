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
from hwcomponents import actionDynamicEnergy
from .isaac import IsaacDAC


# Original CSV contents:
# tech_node,global_cycle_period,resolution,energy,area,n_instances,action
# 32nm,1e-9,4,0.22619,284.375,1,convert|read
# 32nm,1e-9,4,0,284.375,1,update|write|leak
# # Energy: 15.2*10^-3 W / (2.1*32*10^9 ADC BW) * 10 ^ 12 J->pJ
# # 15.2*10^-3 / (2.1*32*10^9) * 10 ^ 12
# # Area: 9100um^2 / 32
class FormsADC(LibraryEstimatorClassBase):
    component_name = "forms_adc"
    percent_accuracy_0_to_100 = 90

    def __init__(self, tech_node: str, resolution: int = 4):
        super().__init__(leak_power=0.0, area=284.375e-12)
        self.tech_node: str = self.scale(
            "tech_node",
            tech_node,
            32e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.resolution: int = self.scale(
            "resolution", resolution, 4, pow_base(2), pow_base(2), pow_base(2)
        )

    @actionDynamicEnergy
    def convert(self) -> float:
        return 0.22619e-12

    @actionDynamicEnergy
    def read(self) -> float:
        return 0.22619e-12


class FormsDAC(IsaacDAC):
    pass
