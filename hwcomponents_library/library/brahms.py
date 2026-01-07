"""
@INPROCEEDINGS{9586247,
  author={Song, Tao and Chen, Xiaoming and Zhang, Xiaoyu and Han, Yinhe},
  booktitle={2021 58th ACM/IEEE Design Automation Conference (DAC)},
  title={BRAHMS: Beyond Conventional RRAM-based Neural Network Accelerators Using Hybrid Analog Memory System},
  year={2021},
  volume={},
  number={},
  pages={1033-1038},
  doi={10.1109/DAC18074.2021.9586247}}
"""

from hwcomponents_library.base import LibraryEstimatorClassBase
from hwcomponents.scaling import *
from hwcomponents import action


# Original CSV contents:
# tech_node,global_cycle_period,resolution,energy,area,action
# 40nm,1e-9,8,0.291,438,read|convert
# 40nm,1e-9,8,0,438,update|write|leak
# # H. Chen,X. Zhot,F. Zhang and Q. Li,"A >3GHz ERBW 1.1GS/S 8B Two-Sten SAR ADC
# # with,Q. Yu Recursive-Weight DAC," 2018 IEEE Symposium on VLSI Circuits,pp.
# # 97-98,2018 doi: 10.1109/VLSIC.2018.8502370.
# # Reported energy: 0.32mW @ 1.1GHz
# # SAR ADC, so the DAC does 1 8b convert for every convert
# # E/op: .32e-3 W * 1 / 1.1e9 seconds * 1e12pJ/J =
# # .32e-3 / 1.1e9 * 1e12 = 0.291pJ/convert
# # Area from chip picture:
# # (Picture was scaled when I screencapped it)
# # 1629px * 743px / (2805px * 1625px) * 75e-6m * 22e-6m
# # = 1629 * 743 / (2805 * 1625) * 75 * 22 = 438um^2
class BrahmsDAC(LibraryEstimatorClassBase):
    """
    Digital-analog converter (DAC) from the BRAHMS paper

    Parameters
    ----------
    tech_node: float
        Technology node in meters
    resolution: int
        Resolution of the DAC in bits
    """

    def __init__(self, tech_node: float, resolution: int = 8):
        super().__init__(leak_power=0.0, area=438.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            40e-9,
            tech_node_area,
            tech_node_energy,
            noscale,
            tech_node_leak,
        )
        self.resolution: int = self.scale(
            "resolution", resolution, 8, pow_base(2), pow_base(2), noscale, pow_base(2)
        )

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency of one DAC conversion.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds)
        """
        return 0.291e-12, 0.0

    @action
    def convert(self) -> tuple[float, float]:
        """
        Returns the energy and latency of one DAC conversion.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds)
        """
        return 0.291e-12, 0.0
