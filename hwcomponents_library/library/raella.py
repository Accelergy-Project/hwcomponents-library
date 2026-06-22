from hwcomponents import ComponentModel, action, ActionCost
from hwcomponents_library.library.misc import SmartBufferSRAM
from hwcomponents_library.library.aladdin import AladdinAdder, AladdinMultiplier
from hwcomponents.scaling import *
from hwcomponents_library.base import LibraryEstimatorClassBase
from hwcomponents_library.library.isaac import IsaacEDRAM


class RaellaOutputCenterOffsetCorrect(ComponentModel):
    """
    Center+offset output correction unit from RAELLA. Reads the stored per-output
    center-offset values from a small buffer and multiplies them into each output to
    undo RAELLA's center+offset weight encoding.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    n_bits_per_output: int
        Number of bits in each output value.
    cycle_period: float
        Cycle period in seconds.
    n_center_entries: int
        Number of center-offset entries stored in the buffer.
    n_center_entry_bits: int
        Number of bits in each center-offset entry.
    """

    def __init__(
        self,
        tech_node: float,
        n_bits_per_output: int,
        cycle_period: float,
        n_center_entries: int,
        n_center_entry_bits: int = 4,
    ):

        self.tech_node = tech_node
        self.n_bits_per_output = n_bits_per_output
        self.n_center_entries = n_center_entries
        self.cycle_period = cycle_period

        self.n_center_entry_bits = n_center_entry_bits

        self.offsets_buf = SmartBufferSRAM(
            tech_node=tech_node,
            size=self.n_center_entry_bits * self.n_center_entries,
        )
        self.multiplier = AladdinMultiplier(
            tech_node=tech_node, width_a=4, width_b=n_bits_per_output
        )

        super().__init__(subcomponents=[self.offsets_buf, self.multiplier])

    @action(bits_per_action="n_bits_per_output")
    def read(self) -> ActionCost:
        """
        Returns the cost consumed by one center+offset output correction.

        Returns
        -------
        ActionCost: The cost of this action
        """
        self.offsets_buf.read(bits_per_action=self.n_center_entry_bits)
        self.multiplier.multiply()


class RaellaInputBuffer(ComponentModel):
    """
    Input buffer and running-sum adder from RAELLA. Holds input slices and accumulates
    partial sums. When speculation is disabled the buffer is read twice as often, so its
    energy is scaled by two.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    speculation_enabled: bool
        Whether speculation is enabled. When disabled, the buffer energy is scaled by two.
    entry_bits: int
        Number of bits in each buffer entry.
    size: int
        Total size of the buffer in bits.
    """

    def __init__(
        self,
        tech_node: float,
        speculation_enabled: bool,
        entry_bits: int,
        size: int,
    ):
        self.tech_node = tech_node
        self.entry_bits = entry_bits
        self.speculation_enabled = speculation_enabled

        self.buf = SmartBufferSRAM(tech_node=tech_node, size=size)
        self.adder = AladdinAdder(tech_node=tech_node, width=entry_bits * 2)
        super().__init__(subcomponents=[self.buf, self.adder])

        # Assume adder does not bottleneck
        self.adder.scale_latency(0)
        self.adder.scale_throughput(float("inf"))

    @action(bits_per_action="entry_bits")
    def read(self) -> tuple:
        """
        Returns the cost consumed to read one input entry and accumulate it.

        Returns
        -------
        ActionCost: The cost of this action
        """
        self.buf.read(bits_per_action=self.entry_bits)
        # One read for speculation + one for recovery
        if self.speculation_enabled:
            self.buf.read(bits_per_action=self.entry_bits)
        self.adder.add()

    @action(bits_per_action="entry_bits")
    def write(self) -> tuple:
        """
        Returns the cost consumed to write one input entry and accumulate it.

        Returns
        -------
        ActionCost: The cost of this action
        """
        self.buf.write(bits_per_action=self.entry_bits)
        self.adder.add()


class RaellaFlagRegister(ComponentModel):
    """
    Speculation flag buffer from RAELLA. Stores one speculation flag per column to tell
    whether the ADC may have overflown for that column.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    n_flags: int
        Number of speculation flags stored.
    speculation_enabled: bool
        Whether speculation is enabled. The flags are only accessed when enabled.
    """

    def __init__(
        self,
        tech_node: float,
        n_flags: int,
        speculation_enabled: bool,
    ):
        self.tech_node = tech_node
        self.n_flags = n_flags
        self.speculation_enabled = speculation_enabled
        self.flag_buf = SmartBufferSRAM(tech_node=tech_node, size=n_flags)
        super().__init__(subcomponents=[self.flag_buf])

    @action
    def read(self) -> tuple:
        """
        Returns the cost consumed to write and read back one speculation flag.

        Returns
        -------
        ActionCost: The cost of this action
        """
        # Write the flags in during non-speculation and read them during speculation
        if self.speculation_enabled:
            self.flag_buf.write(bits_per_action=1)
            self.flag_buf.read(bits_per_action=1)


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
    width: int
        Width of the to-be-quantized values in bits.
    """

    def __init__(self, tech_node: float, width: int = 16):
        super().__init__(leak_power=0.0, area=0.0e-12)
        self.tech_node: float = self.scale(
            "tech_node",
            tech_node,
            40e-9,
            area_scale_function=tech_node_area,
            energy_scale_function=tech_node_energy,
            latency_scale_function=tech_node_latency,
            throughput_scale_function=tech_node_throughput,
            leak_power_scale_function=tech_node_leak,
        )
        self.width: int = self.scale(
            "resolution",
            width,
            16,
            area_scale_function=linear,
            energy_scale_function=linear,
            latency_scale_function=noscale,
            throughput_scale_function=noscale,
            leak_power_scale_function=linear,
        )

    @action
    def multiply(self) -> ActionCost:
        """
        Returns the energy and latency consumed by a multiply operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return ActionCost(energy=0.25e-12, throughput=1 / 1e-9, latency=1e-9)

    @action
    def read(self) -> ActionCost:
        """
        Returns the energy and latency consumed by a multiply operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        return ActionCost(energy=0.25e-12, throughput=1 / 1e-9, latency=1e-9)


class RaellaQuantEDRAM(LibraryEstimatorClassBase):
    """
    The quantization & multipliler from the RAELLA paper. This unit will multiply a
    partial sum value by a quantization scale to apply linear quntization. It also
    includes an EDRAM buffer to store quantization scales and offsets.

    Parameters
    ----------
    tech_node: float
        Technology node in meters.
    size: int
        Total size of the EDRAM buffer in bits.
    width: int
        Width of the to-be-quantized values in bits.
    """

    def __init__(self, tech_node: float, size, width):
        self.edram = IsaacEDRAM(tech_node=tech_node, size=size)
        self.multiplier = RaellaQuantMultiplier(tech_node=tech_node, width=width)

    @action
    def multiply(self) -> ActionCost:
        """
        Returns the energy and latency consumed by a quantization operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        self.edram.read()
        self.multiplier.multiply()

    @action
    def read(self) -> ActionCost:
        """
        Returns the energy and latency consumed by a multiply operation.

        Returns
        -------
        (energy, latency): Tuple in (Joules, seconds).
        """
        self.multiply()
