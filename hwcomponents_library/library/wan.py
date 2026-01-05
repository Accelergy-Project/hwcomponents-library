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
from hwcomponents import actionDynamicEnergy


# Original CSV contents:
# tech_node,n_repeats,global_cycle_period,resolution, voltage,energy,area,  action
# 130nm,     1,      1e-6,                8,          1.8,    0.1,   170,  read
# 130nm,     1,      1e-6,                8,          1.8,    0.1,   170,  write|update
# 130nm,     1,      1e-6,                8,          1.8,    0.1,   170,  leak
class WanShiftAdd(LibraryEstimatorClassBase):
    """
    The shift-and-add unit from the Wan et al. Nature 2022 paper. This unit will sum and
    accumulate values in a register, while also shifting the register contents to accept
    various power-of-two scaling factors for the summed values.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    n_repeats: int
        Number of times to repeat the shift-and-add operation.
    resolution: int
        Resolution of the shift-and-add unit in bits. This is the number of bits of each
        input value that is added to the register.
    voltage: float
        Voltage of the shift-and-add unit in volts.
    """

    def __init__(
        self,
        tech_node: float,
        n_repeats: int = 1,
        resolution: int = 8,
        voltage: float = 1.8,
    ):
        super().__init__(leak_power=1.00e-7, area=170.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            130e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.n_repeats: int = self.scale(
            "n_repeats", n_repeats, 1, linear, linear, linear
        )
        self.resolution: int = self.scale(
            "resolution", resolution, 8, pow_base(2), pow_base(2), pow_base(2)
        )
        self.voltage: float = self.scale("voltage", voltage, 1.8, noscale, quadratic, 1)

    @actionDynamicEnergy
    def read(self) -> float:
        """
        Returns zero Joules.

        Returns
        -------
        float
            Zero Joules.
        """
        return 0

    @actionDynamicEnergy
    def write(self) -> float:
        """
        Returns the energy used to perform a shift-and-add operation in Joules.

        Returns
        -------
        float
            The energy used to perform a shift-and-add operation in Joules.
        """
        return self.shift_and_add()

    @actionDynamicEnergy
    def shift_and_add(self) -> float:
        """
        Returns the energy used to perform a shift-and-add operation in Joules.

        Returns
        -------
        float
            The energy used to perform a shift-and-add operation in Joules.
        """
        return 0.1e-12


# Original CSV contents:
# tech_node,n_repeats,global_cycle_period,voltage,energy,area,  action
# 130nm,     1,      1e-6,                1.8,    0.3,  400,   read
# 130nm,     1,      1e-6,                1.8,    0,     400,   leak
# 130nm,     1,      1e-6,                1.8,    0,     400,   write|update
class WanVariablePrecisionADC(LibraryEstimatorClassBase):
    """
    The variable precision ADC from the Wan et al. Nature 2022 paper. This unit will
    convert a voltage to a digital value.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    n_repeats: int
        Number of times to repeat the ADC operation.
    voltage: float
        Voltage of the ADC unit in volts.
    """

    def __init__(self, tech_node: float, n_repeats: int = 1, voltage: float = 1.8):
        super().__init__(leak_power=0.0, area=400.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            130e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.n_repeats: int = self.scale(
            "n_repeats", n_repeats, 1, linear, linear, linear
        )
        self.voltage: float = self.scale("voltage", voltage, 1.8, noscale, quadratic, 1)

    @actionDynamicEnergy
    def convert(self) -> float:
        """
        Returns the energy used to convert a voltage to a digital value in Joules.

        Returns
        -------
        float
            The energy used to convert a voltage to a digital value in Joules.
        """
        return 0.3e-12

    @actionDynamicEnergy
    def read(self) -> float:
        """
        Returns the energy used to convert a voltage to a digital value in Joules.

        Returns
        -------
        float
            The energy used to convert a voltage to a digital value in Joules.
        """
        return self.convert()


# Original CSV contents:
# tech_node,global_cycle_period,voltage,energy,area,  action
# 130nm,     1e-6,                1.8,    1.2,   350,  read
# 130nm,     1e-6,                1.8,    0,     350,  leak
# 130nm,     1e-6,                1.8,    0,     350,  write|update
class WanAnalogSample(LibraryEstimatorClassBase):
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

    def __init__(self, tech_node: float, voltage: float = 1.8):
        super().__init__(leak_power=0.0, area=350.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            130e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.voltage: float = self.scale("voltage", voltage, 1.8, noscale, quadratic, 1)

    @actionDynamicEnergy
    def read(self) -> float:
        """
        Returns the energy used to sample an analog voltage in Joules.

        Returns
        -------
        float
            The energy used to sample an analog voltage in Joules.
        """
        return self.sample()

    @actionDynamicEnergy
    def sample(self) -> float:
        """
        Returns the energy used to sample an analog voltage in Joules.

        Returns
        -------
        float
            The energy used to sample an analog voltage in Joules.
        """
        return 1.2e-12


# Original CSV contents:
# tech_node,n_repeats,global_cycle_period,voltage,energy,area, action
# 130nm,     1,      1e-6,                 1.8,   0.25,  350,  read
# 130nm,     1,      1e-6,                1.8,    0,     350,  leak
# 130nm,     1,      1e-6,                1.8,    0,     350,  write|update
class WanAnalogIntegrator(LibraryEstimatorClassBase):
    """
    The analog integrator unit from the Wan et al. Nature 2022 paper. This unit will
    integrate charge over multiple samples.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    n_repeats: int
        Number of times to repeat the analog integration operation.
    voltage: float
        Voltage of the analog integrator unit in volts.
    """

    def __init__(self, tech_node: float, n_repeats: int = 1, voltage: float = 1.8):
        super().__init__(leak_power=0.0, area=350.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            130e-9,
            tech_node_energy,
            tech_node_area,
            tech_node_leak,
        )
        self.n_repeats: int = self.scale(
            "n_repeats", n_repeats, 1, linear, linear, linear
        )
        self.voltage: float = self.scale("voltage", voltage, 1.8, noscale, quadratic, 1)

    @actionDynamicEnergy
    def integrate(self) -> float:
        """
        Returns the energy used to integrate charge for a sample in Joules.

        Returns
        -------
        float
            The energy used to integrate charge for a sample in Joules.
        """
        return 0.25e-12

    @actionDynamicEnergy
    def read(self) -> float:
        """
        Returns the energy used to integrate charge for a sample in Joules.

        Returns
        -------
        float
            The energy used to integrate charge for a sample in Joules.
        """
        return self.integrate()
