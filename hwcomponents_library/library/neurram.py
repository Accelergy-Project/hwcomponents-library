"""
@article{wan2022compute,
  title={A compute-in-memory chip based on resistive random-access memory},
  author={Wan, Weier and Kubendran, Rajkumar and Schaefer, Clemens and Eryilmaz, Sukru Burc and Zhang, Wenqiang and Wu, Dabin and Deiss, Stephen and Raina, Priyanka and Qian, He and Gao, Bin and others},
  journal={Nature},
  volume={608},
  number={7923},
  pages={504--512},
  year={2022},
  publisher={Nature Publishing Group UK London}
}
"""

from hwcomponents_library.base import LibraryEstimatorClassBase
from hwcomponents.scaling import *
from hwcomponents import action, ActionCost


# Original CSV contents:
# tech_node,n_repeats,global_cycle_period,resolution, voltage,energy,area,  action
# 130nm,     1,      1e-6,                8,          1.8,    0.1,   170,  read
# 130nm,     1,      1e-6,                8,          1.8,    0.1,   170,  write|update
# 130nm,     1,      1e-6,                8,          1.8,    0.1,   170,  leak
class NeurramShiftAdd(LibraryEstimatorClassBase):
    """
    The shift-and-add unit from the Wan et al. Nature 2022 paper. This unit will sum and
    accumulate values in a register, while also shifting the register contents to accept
    various power-of-two scaling factors for the summed values.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    resolution: int
        Resolution of the shift-and-add unit in bits. This is the number of bits of each
        input value that is added to the register.
    voltage: float
        Voltage of the shift-and-add unit in volts.
    """

    def __init__(
        self,
        tech_node: float,
        resolution: int = 8,
        voltage: float = 1.8,
    ):
        super().__init__(
            leak_power=5.00e-9, area=170.0e-12
        )  # 130nm digital static power
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            130e-9,
            area_scale_function=tech_node_area,
            energy_scale_function=tech_node_energy,
            latency_scale_function=tech_node_latency,
            throughput_scale_function=tech_node_throughput,
            leak_power_scale_function=tech_node_leak,
        )
        self.resolution: int = self.scale(
            "resolution",
            resolution,
            8,
            area_scale_function=pow_base(2),
            energy_scale_function=pow_base(2),
            latency_scale_function=noscale,
            throughput_scale_function=noscale,
            leak_power_scale_function=noscale,
        )
        self.voltage: float = self.scale(
            "voltage",
            voltage,
            1.8,
            area_scale_function=quadratic,
            energy_scale_function=quadratic,
            latency_scale_function=noscale,
            throughput_scale_function=noscale,
            leak_power_scale_function=quadratic,
        )

    @action
    def read(self) -> ActionCost:
        """
        Returns the cost consumed by a shift-and-add operation.

        Returns
        -------
        ActionCost: The cost of this action
        """
        return self.shift_and_add()

    @action
    def write(self) -> ActionCost:
        """
        Returns the cost consumed by a shift-and-add operation.

        Returns
        -------
        ActionCost: The cost of this action
        """
        return self.shift_and_add()

    @action
    def shift_and_add(self) -> ActionCost:
        """
        Returns the cost consumed by a shift-and-add operation.

        Returns
        -------
        ActionCost: The cost of this action
        """
        return ActionCost(energy=0.1e-12, throughput=float("inf"), latency=0.0)


# Original CSV contents:
# tech_node,n_repeats,global_cycle_period,voltage,energy,area,  action
# 130nm,     1,      1e-6,                1.8,    0.3,  400,   read
# 130nm,     1,      1e-6,                1.8,    0,     400,   leak
# 130nm,     1,      1e-6,                1.8,    0,     400,   write|update
class NeurramVariablePrecisionADC(LibraryEstimatorClassBase):
    """
    The variable precision ADC from the Wan et al. Nature 2022 paper. This unit will
    convert a voltage to a digital value.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    voltage: float
        Voltage of the ADC unit in volts.
    """

    def __init__(self, tech_node: float, voltage: float = 1.8):
        super().__init__(leak_power=1e-8, area=400.0e-12)  # 130nm ADC static power
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            130e-9,
            area_scale_function=tech_node_area,
            energy_scale_function=tech_node_energy,
            latency_scale_function=tech_node_latency,
            throughput_scale_function=tech_node_throughput,
            leak_power_scale_function=tech_node_leak,
        )
        self.voltage: float = self.scale(
            "voltage",
            voltage,
            1.8,
            area_scale_function=quadratic,
            energy_scale_function=quadratic,
            latency_scale_function=noscale,
            throughput_scale_function=noscale,
            leak_power_scale_function=quadratic,
        )

    @action
    def convert(self) -> ActionCost:
        """
        Returns the cost consumed to convert a voltage to a digital value.

        Returns
        -------
        ActionCost: The cost of this action
        """
        return ActionCost(energy=0.3e-12, throughput=float("inf"), latency=0.0)

    @action
    def read(self) -> ActionCost:
        """
        Returns the cost consumed to convert a voltage to a digital value.

        Returns
        -------
        ActionCost: The cost of this action
        """
        return self.convert()


# Original CSV contents:
# tech_node,global_cycle_period,voltage,energy,area,  action
# 130nm,     1e-6,                1.8,    1.2,   350,  read
# 130nm,     1e-6,                1.8,    0,     350,  leak
# 130nm,     1e-6,                1.8,    0,     350,  write|update
class NeurramAnalogSample(LibraryEstimatorClassBase):
    """
    The analog sample unit from the Wan et al. Nature 2022 paper. This unit will sample
    an analog charge and add it to an analog integrator.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    voltage: float
        Voltage of the analog sample unit in volts.
    """

    def __init__(self, tech_node: float, width: int = 1, voltage: float = 1.8):
        super().__init__(
            leak_power=1e-8, area=45.0e-12
        )  # 130nm analog sample static power
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            130e-9,
            area_scale_function=tech_node_area,
            energy_scale_function=tech_node_energy,
            latency_scale_function=tech_node_latency,
            throughput_scale_function=tech_node_throughput,
            leak_power_scale_function=tech_node_leak,
        )
        self._width = width
        self.width: int = self.scale(
            "width",
            width,
            1,
            area_scale_function=linear,
            energy_scale_function=noscale,
            latency_scale_function=noscale,
            throughput_scale_function=noscale,
            leak_power_scale_function=noscale,
        )
        self.voltage: float = self.scale(
            "voltage",
            voltage,
            1.8,
            area_scale_function=quadratic,
            energy_scale_function=quadratic,
            latency_scale_function=noscale,
            throughput_scale_function=noscale,
            leak_power_scale_function=quadratic,
        )

    @action
    def read(self) -> ActionCost:
        """
        Returns the cost consumed to sample an analog charge.

        Returns
        -------
        ActionCost: The cost of this action
        """
        return self.sample()

    @action
    def sample(self) -> ActionCost:
        """
        Returns the cost consumed to sample an analog charge.

        Returns
        -------
        ActionCost: The cost of this action
        """
        return ActionCost(energy=1.2e-12, throughput=float("inf"), latency=0.0)


# Original CSV contents:
# tech_node,n_repeats,global_cycle_period,voltage,energy,area, action
# 130nm,     1,      1e-6,                 1.8,   0.25,  350,  read
# 130nm,     1,      1e-6,                1.8,    0,     350,  leak
# 130nm,     1,      1e-6,                1.8,    0,     350,  write|update
class NeurramAnalogIntegrator(LibraryEstimatorClassBase):
    """
    The analog integrator unit from the Wan et al. Nature 2022 paper. This unit will
    integrate charge over multiple samples.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    voltage: float
        Voltage of the analog integrator unit in volts.
    """

    def __init__(self, tech_node: float, voltage: float = 1.8):
        super().__init__(
            leak_power=5e-9, area=350.0e-12
        )  # 130nm integrator static power
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            130e-9,
            area_scale_function=tech_node_area,
            energy_scale_function=tech_node_energy,
            latency_scale_function=tech_node_latency,
            throughput_scale_function=tech_node_throughput,
            leak_power_scale_function=tech_node_leak,
        )
        self.voltage: float = self.scale(
            "voltage",
            voltage,
            1.8,
            area_scale_function=quadratic,
            energy_scale_function=quadratic,
            latency_scale_function=noscale,
            throughput_scale_function=noscale,
            leak_power_scale_function=quadratic,
        )

    @action
    def integrate(self) -> ActionCost:
        """
        Returns the cost consumed to integrate charge for a sample.

        Returns
        -------
        ActionCost: The cost of this action
        """
        return ActionCost(energy=0.25e-12, throughput=float("inf"), latency=0.0)

    @action
    def read(self) -> ActionCost:
        """
        Returns the cost consumed to integrate charge for a sample.

        Returns
        -------
        ActionCost: The cost of this action
        """
        return self.integrate()
