from ppc_asm.assembler import ppc


def _b(instruction: ppc.BaseInstruction, address: int = 0, symbols=None) -> list[int]:
    if symbols is None:
        symbols = {}
    return list(instruction.bytes_for(address, symbols=symbols))


def test_instruction_iter():
    assert _b(ppc.Instruction(1234)) == [0x00, 0x00, 0x04, 0xD2]


def test_instruction_eq():
    assert ppc.Instruction(1234) == ppc.Instruction(1234)


def test_instruction_with_label():
    instruction = ppc.Instruction(1234)
    assert instruction.label is None

    with_label = instruction.with_label("foobar")
    assert instruction is with_label
    assert instruction.label == "foobar"


def test_stw():
    assert _b(ppc.stw(ppc.r31, 0x1C, ppc.r1)) == [0x93, 0xE1, 0x00, 0x1C]


def test_stfs():
    assert _b(ppc.stfs(ppc.f0, 0x1000, ppc.r2)) == [208, 2, 16, 0]


def test_lfs():
    assert _b(ppc.lfs(ppc.f0, (0x8041A4A8 - 0x804223C0), ppc.r2)) == [
        0xC0,
        0x02,
        0x80,
        0xE8,
    ]


def test_addi():
    assert _b(ppc.addi(ppc.r3, ppc.r1, 0x8)) == [0x38, 0x61, 0x00, 0x08]


def test_or():
    assert _b(ppc.or_(ppc.r31, ppc.r3, ppc.r3)) == [124, 127, 27, 120]


def test_lmw():
    assert _b(ppc.lmw(ppc.r25, 0x774, ppc.r25)) == [187, 57, 7, 116]


def test_lwz():
    assert _b(ppc.lwz(ppc.r10, 0x774, ppc.r25)) == [0x81, 0x59, 0x07, 0x74]


def test_lwzx():
    assert _b(ppc.lwzx(ppc.r0, ppc.r4, ppc.r0)) == [0x7C, 0x04, 0x00, 0x2E]


def test_lhz():
    assert _b(ppc.lhz(ppc.r6, -0x40DA, ppc.r2)) == [0xA0, 0xC2, 0xBF, 0x26]


def test_lbz():
    assert _b(ppc.lbz(ppc.r4, 0x2, ppc.r3)) == [0x88, 0x83, 0x00, 0x02]


def test_rlwinm():
    assert _b(ppc.rlwinm(ppc.r0, ppc.r0, 0x2, 0x0, 0x1D)) == [0x54, 0x00, 0x10, 0x3A]


def test_cmpwi_a():
    assert _b(ppc.cmpwi(ppc.r30, 0)) == [0x2C, 0x1E, 0x00, 0x00]


def test_cmpwi_b():
    assert _b(ppc.cmpwi(ppc.r4, -1)) == [0x2C, 0x04, 0xFF, 0xFF]


def test_cmpw():
    assert _b(ppc.cmpwi(ppc.r4, -1)) == [0x2C, 0x04, 0xFF, 0xFF]


def test_b():
    assert _b(ppc.b(0x80085760), address=0x80085760 + 0x9C) == [0x4B, 0xFF, 0xFF, 0x64]


def test_bl():
    assert _b(ppc.bl(0x80085760), address=0x80085760 + 0x9C) == [0x4B, 0xFF, 0xFF, 0x65]


def test_bdnz():
    assert _b(ppc.bdnz(16, relative=True)) == [0x42, 0x00, 0x00, 0x10]


def test_beq():
    assert _b(ppc.beq(0x80038094), address=0x80038034) == [0x41, 0x82, 0x00, 0x60]


def test_beq_symbol():
    symbols = {"TheFunPlace": 0x80038094}
    assert _b(ppc.beq("TheFunPlace"), address=0x80038034, symbols=symbols) == [
        0x41,
        0x82,
        0x00,
        0x60,
    ]


def test_bge():
    assert _b(ppc.bge(0x801C93F8), address=0x801C93EC) == [0x40, 0x80, 0x00, 0x0C]


def test_bne():
    assert _b(ppc.bne(0x80038094), address=0x80038034) == [0x40, 0x82, 0x00, 0x60]


def test_blr():
    assert _b(ppc.blr()) == [0x4E, 0x80, 0x00, 0x20]


def test_bctrl():
    assert _b(ppc.bctrl()) == [0x4E, 0x80, 0x04, 0x21]


def test_li():
    assert _b(ppc.li(ppc.r5, 9999)) == [56, 160, 39, 15]


def test_stwu():
    assert _b(ppc.stwu(ppc.r1, -0x2C, ppc.r1)) == [0x94, 0x21, 0xFF, 0xD4]


def test_stmw():
    assert _b(ppc.stmw(ppc.r25, -0x2C, ppc.r1)) == [191, 33, 255, 212]


def test_sync():
    assert _b(ppc.sync()) == [0x7C, 0x00, 0x04, 0xAC]


def test_isync():
    assert _b(ppc.isync()) == [0x4C, 0x00, 0x01, 0x2C]


def test_dcbi():
    assert _b(ppc.dcbi(1, 2)) == [0x7C, 0x01, 0x13, 0xAC]


def test_mfspr_LR():
    assert _b(ppc.mfspr(ppc.r0, ppc.LR)) == [0x7C, 0x08, 0x02, 0xA6]


def test_mtctr():
    assert _b(ppc.mtctr(ppc.r12)) == [0x7D, 0x89, 0x03, 0xA6]


def test_nop():
    assert _b(ppc.nop()) == [96, 0, 0, 0]
