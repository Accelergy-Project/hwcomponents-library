"""
@ARTICLE{9082159,
  author={Jia, Hongyang and Valavi, Hossein and Tang, Yinqi and Zhang, Jintao and Verma, Naveen},
  journal={IEEE Journal of Solid-State Circuits},
  title={A Programmable Heterogeneous Microprocessor Based on Bit-Scalable In-Memory Computing},
  year={2020},
  volume={55},
  number={9},
  pages={2609-2621},
  doi={10.1109/JSSC.2020.2987714}}
"""

from hwcomponents_library.base import LibraryEstimatorClassBase
from hwcomponents.scaling import *
from hwcomponents import ComponentModel, action
from math import ceil, log2
from hwcomponents import ComponentModel, action, ActionCost
from hwcomponents.scaling import linear, quadratic, reciprocal
from hwcomponents_library.library.aladdin import AladdinComparator, AladdinCounter
from hwcomponents_neurosim import FlipFlop, AdderTree


# Original CSV contents:
# tech_node,global_cycle_period,resolution,voltage,energy,area,action
# 65nm,      540e-9,              8,         1.2,   2.25,   5000,read
# 65nm,      540e-9,              8,         1.2,   1.2,    5000,leak
# 65nm,      540e-9,              8,         1.2,   0,      5000,write|update
class JiaShiftAdd(LibraryEstimatorClassBase):
    """
    The shift-and-add unit from Jia et al. JSSC 2020. This unit will sum and accumulate
    values in a register, while also shifting the register contents to accept various
    power-of-two scaling factors for the summed values.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    resolution: int
        Resolution of the shift-and-add unit in bits. This is the number of bits of each
        input value that is added to the register.
    voltage: float
        Voltage of the shift-and-add unit in volts.
    cycle_period: float
        Cycle period of the system clock in seconds. One cycle = one activation of the
        analog array.
    """

    def __init__(self, tech_node: float, resolution: int = 8, voltage: float = 1.2, cycle_period: float = 540e-9):
        super().__init__(leak_power=2.22e-6, area=5000.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            65e-9,
            tech_node_area,
            tech_node_energy,
            tech_node_latency,
            tech_node_leak,
        )
        self.resolution: int = self.scale(
            "resolution", resolution, 8, pow_base(2), pow_base(2), noscale, pow_base(2)
        )
        self.voltage: float = self.scale(
            "voltage", voltage, 1.2, noscale, quadratic, noscale, quadratic
        )
        self.cycle_period: float = cycle_period

    @action
    def shift_and_add(self) -> tuple[float, float]:
        """
        Returns the costv consumed by a shift+add operation.

        Returns
        -------
        ActionCost: The cost of this action
        """
        return ActionCost(
            energy=2.25e-12,
            latency=self.cycle_period / 8,
            throughput=8 / self.cycle_period,
        )
    
    @action
    def write(self) -> tuple[float, float]:
        """
        Returns the cost consumed by a shift+add operation.

        Returns
        -------
        ActionCost: The cost of this action
        """
        return self.shift_and_add()

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the cost consumed by a shift+add operation.

        Returns
        -------
        ActionCost: The cost of this action
        """
        return self.shift_and_add()


# Original CSV contents:
# tech_node,global_cycle_period,voltage,energy,area,  action
# 65nm,      540e-9,              1.2,   12,     10535,read
# 65nm,      540e-9,              1.2,   2.4,    10535,leak
# 65nm,      540e-9,              1.2,   0,      10535,write|update
class JiaDatapath(LibraryEstimatorClassBase):
    """
    The datapath in Jia et al. JSSC 2020. This datapath will perform quantization and
    activation functions on accumulated ouputs.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    voltage: float
        Voltage of the datapath in volts.
    cycle_period: float
        Cycle period of the system clock in seconds. One cycle = one activation of the
        analog array.

    """

    def __init__(self, tech_node: float, voltage: float = 1.2, cycle_period: float = 540e-9):
        super().__init__(leak_power=4.44e-6, area=10535.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            65e-9,
            tech_node_area,
            tech_node_energy,
            tech_node_latency,
            tech_node_leak,
        )
        self.voltage: float = self.scale(
            "voltage", voltage, 1.2, noscale, quadratic, noscale, quadratic
        )
        self.cycle_period: float = cycle_period

    @action
    def process(self) -> ActionCost:
        """
        Returns the cost consumed by the datapath to quantize and apply activation
        functions on a single input.

        Returns
        -------
        ActionCost: The cost of this action
        """
        return ActionCost(
            energy=12e-12,
            latency=self.cycle_period / 8,
            throughput=8 / self.cycle_period,
        )

    @action
    def read(self) -> tuple[float, float]:
        """
        Returns the cost consumed by the datapath to quantize and apply activation
        functions on a single input.

        Returns
        -------
        ActionCost: The cost of this action
        """
        return self.process()


class JiaZeroComparator(LibraryEstimatorClassBase):
    """
    Counts the number of zeros in a list of values. Includes a flag for each zero.

    Based on the zero gating logic in the paper: A Programmable Heterogeneous
    Microprocessor Based on Bit-Scalable In-Memory Computing, by Hongyang Jia, Hossein
    Valavi, Yinqi Tang, Jintao Zhang, and Naveen Verma, JSSC 2020
    10.1109/JSSC.2020.2987714

    Parameters
    ----------
    n_comparators: int
        The number of comparators to include.
    n_bits: int
        The number of bits of each comparator.
    tech_node: str
        The technology node of the comparators.
    voltage: float
        The voltage of the comparators.
    """

    def __init__(
        self,
        n_comparators: int,
        n_bits: int,
        tech_node: str,
        voltage: float = 0.85,
        cycle_period: float = 1e-9,
    ):
        self.n_comparators = n_comparators
        self.n_bits = n_bits

        # Scale up the comparator to handle all the comparators
        self.comparator = AladdinComparator(
            width=n_bits,
            tech_node=tech_node,
        )
        self.comparator.area_scale *= n_comparators
        self.comparator.leak_power_scale *= n_comparators
        self.comparator.throughput_scale *= n_comparators

        # Flip flops are used one bit at a time, so we only make one bit and scale the
        # energy and latency
        self.flip_flop = FlipFlop(
            n_bits=1,
            tech_node=tech_node,
            cycle_period=cycle_period,
        )
        n_flip_flops = n_comparators * n_bits  # One flip flop per bit per comparator
        n_flip_flops_serial = n_bits  # Only one flip flop active at a time
        self.flip_flop.area_scale *= n_flip_flops
        self.flip_flop.leak_power_scale *= n_flip_flops
        self.flip_flop.throughput_scale *= n_flip_flops

        # Charging per-input, not for all
        self.flip_flop.energy_scale *= n_flip_flops_serial 
        self.flip_flop.latency_scale *= n_flip_flops_serial

        self.zeros_counter = AdderTree(
            n_bits=1,
            n_adder_tree_inputs=n_comparators,
            tech_node=tech_node,
            cycle_period=cycle_period
        )
        # Adder tree charges energy and throughput for ALL inputs, but this component
        # charges per-input, so scale down by the number of inputs.
        self.zeros_counter.energy_scale /= n_comparators
        self.zeros_counter.throughput_scale *= n_comparators
        
        self.flip_flop.energy_scale = 0

        super().__init__(
            subcomponents=[
                self.comparator,
                self.flip_flop,
                self.zeros_counter,
            ],
        )

        for subcomponent in self.subcomponents:
            subcomponent.scale(
                "voltage",
                voltage,
                0.85,
                area_scale_function=linear,
                energy_scale_function=quadratic,
                latency_scale_function=reciprocal,
                throughput_scale_function=linear,
                leak_power_scale_function=linear,
            )
            subcomponent.leak_power_scale *= 0.02  # Low-leakage technology

    @action
    def read(self) -> ActionCost:
        """
        Processes ONE value through the comparator and updates the flip flop and zeros
        counter accordingly.

        Returns
        -------
        ActionCost: The cost of this action
        """
        self.comparator.read()
        self.flip_flop.read()
        self.zeros_counter.read()
