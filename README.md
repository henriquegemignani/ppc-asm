# ppc-asm

This package provides allows one to easily modify existing Nintendo GameCube or Wii game executables.


## Usage

```python

import pathlib
from ppc_asm.dol_file import DolFile
from ppc_asm.assembler.ppc import *

dol_file = DolFile(pathlib.Path("main.dol"))
dol_file.set_editable(True)
with dol_file:
    dol_file.write_instructions(
        0x800857F0,
        [
            or_(r3, r30, r30),
            li(r4, 0x29),
            li(r5, 9999),
            bl(0x80085760),
        ]
    )

```