"""
@inproceedings{10.1145/3579371.3589062,
author = {Andrulis, Tanner and Emer, Joel S. and Sze, Vivienne},
title = {RAELLA: Reforming the Arithmetic for Efficient, Low-Resolution, and Low-Loss Analog PIM: No Retraining Required!},
year = {2023},
isbn = {9798400700958},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3579371.3589062},
doi = {10.1145/3579371.3589062},
abstract = {Processing-In-Memory (PIM) accelerators have the potential to efficiently run Deep Neural Network (DNN) inference by reducing costly data movement and by using resistive RAM (ReRAM) for efficient analog compute. Unfortunately, overall PIM accelerator efficiency is limited by energy-intensive analog-to-digital converters (ADCs). Furthermore, existing accelerators that reduce ADC cost do so by changing DNN weights or by using low-resolution ADCs that reduce output fidelity. These strategies harm DNN accuracy and/or require costly DNN retraining to compensate.To address these issues, we propose the RAELLA architecture. RAELLA adapts the architecture to each DNN; it lowers the resolution of computed analog values by encoding weights to produce near-zero analog values, adaptively slicing weights for each DNN layer, and dynamically slicing inputs through speculation and recovery. Low-resolution analog values allow RAELLA to both use efficient low-resolution ADCs and maintain accuracy without retraining, all while computing with fewer ADC converts.Compared to other low-accuracy-loss PIM accelerators, RAELLA increases energy efficiency by up to 4.9\texttimes{} and throughput by up to 3.3\texttimes{}. Compared to PIM accelerators that cause accuracy loss and retrain DNNs to recover, RAELLA achieves similar efficiency and throughput without expensive DNN retraining.},
booktitle = {Proceedings of the 50th Annual International Symposium on Computer Architecture},
articleno = {27},
numpages = {16},
keywords = {processing in memory, compute in memory, analog, neural networks, accelerator, architecture, slicing, ADC, ReRAM},
location = {Orlando, FL, USA},
series = {ISCA '23}
}
"""

from hwcomponents_library.base import LibraryEstimatorClassBase
from hwcomponents.scaling import *
from hwcomponents import action


# Original CSV contents:
# tech_node,global_cycle_period,energy,area,n_instances,action
# 40nm,1e-9,0.25,0,1,multiply|read,
# 40nm,1e-9,0,0,1,update|leak|write,
# # Assuming multiplication energy scales linearly with input, weight, and output energy
# # Efficient processing of DNNs (Sze, 2020): 8b*8b->16b multiply 0.2pJ
# # 16b * 8b -> 8b multiply: 0.2 pJ
# # We do this at the L2 (large) tile level, so area will be negligible
class RaellaQuantMultiplier(LibraryEstimatorClassBase):
    """
    The quantization & multipliler from the RAELLA paper. This unit will multiply a
    partial sum value by a quantization scale to apply linear quntization.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    """

    def __init__(self, tech_node: float, resolution: int = 16):
        super().__init__(leak_power=0.0, area=0.0e-12)
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
            "resolution", resolution, 16, linear, linear, noscale, linear
        )

    @action
    def multiply(self) -> tuple[float, float]:
        """
        Returns the energy and latency consumed by a multiply operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.25e-12, 0.0

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency consumed by a multiply operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return 0.25e-12, 0.0
