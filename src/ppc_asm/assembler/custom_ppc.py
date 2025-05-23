from __future__ import annotations

import typing as _typing

from ppc_asm.assembler import ppc

if _typing.TYPE_CHECKING:
    from collections.abc import Iterator


class CompositeInstruction(ppc.BaseInstruction):
    def __init__(self, instructions: tuple[ppc.BaseInstruction, ...]):
        super().__init__()
        self.instructions = instructions

    def bytes_for(self, address: int, symbols: dict[str, int]) -> Iterator[int]:
        for instruction in self.instructions:
            yield from instruction.bytes_for(address, symbols=symbols)
            address += instruction.byte_count

    def __eq__(self, other: object) -> bool:
        return isinstance(other, CompositeInstruction) and other.instructions == self.instructions

    @property
    def byte_count(self) -> int:
        return sum(instruction.byte_count for instruction in self.instructions)


class CurrentAddressInstruction(ppc.BaseInstruction):
    def __init__(self, output_register: ppc.GeneralRegister, offset: int):
        super().__init__()
        self.output_register = output_register
        self.offset = offset

    def bytes_for(self, address: int, symbols: dict[str, int]) -> Iterator[int]:
        return load_unsigned_32bit(self.output_register, address + self.offset).bytes_for(address, symbols=symbols)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, CurrentAddressInstruction) and (
            other.output_register,
            other.offset,
        ) == (self.output_register, self.offset)

    @property
    def byte_count(self) -> int:
        return 8


def load_unsigned_32bit(output_register: ppc.GeneralRegister, value: int) -> CompositeInstruction:
    return CompositeInstruction(
        (
            ppc.lis(output_register, value >> 16),
            ppc.ori(output_register, output_register, value & 0xFFFF),
        )
    )


def load_current_address(output_register: ppc.GeneralRegister, instruction_offset: int = 0) -> ppc.BaseInstruction:
    return CurrentAddressInstruction(output_register, instruction_offset * 4)
