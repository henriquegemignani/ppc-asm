from __future__ import annotations

import copy
import typing

from ppc_asm.assembler.ppc import BaseInstruction, Instruction

if typing.TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

__all__ = [
    "BaseInstruction",
    "Instruction",
    "assemble_instructions",
    "byte_count",
]


def assemble_instructions(
    address: int,
    instructions: Sequence[BaseInstruction],
    symbols: Mapping[str, int] | None = None,
) -> typing.Iterable[int]:
    symbols = copy.copy(symbols) if symbols is not None else {}

    b = address
    for instruction in instructions:
        if instruction.label is not None:
            symbols[instruction.label] = b
        b += instruction.byte_count

    for i, instruction in enumerate(instructions):
        data = list(instruction.bytes_for(address, symbols=symbols))
        yield from data
        address += len(data)


def byte_count(instructions: typing.Iterable[BaseInstruction]) -> int:
    return sum(instruction.byte_count for instruction in instructions)
