from PyCPU.program.assembler import Assembler
import pytest

def test_assemble_program_without_labels():
    assembler = Assembler()

    source = [
        ("MOV", "R0", 10),
        ("ADD", "R0", 1),
    ]

    result = assembler.assemble(source)

    assert result == [
        ("MOV", "R0", 10),
        ("ADD", "R0", 1),
    ]

def test_backward_label():
    assembler = Assembler()

    source = [
        ("MOV", "R0", 10),
        ("LABEL", "LOOP"),
        ("SUB", "R0", 1),
        ("CMP", "R0", 0),
        ("JG", "LOOP"),
    ]

    result = assembler.assemble(source)

    assert result == [
        ("MOV", "R0", 10),
        ("SUB", "R0", 1),
        ("CMP", "R0", 0),
        ("JG", 1),
    ]

def test_forward_label():
    assembler = Assembler()

    source = [
        ("JUMP", "START"),
        ("MOV", "R0", 100),
        ("LABEL", "START"),
        ("MOV", "R0", 42),
    ]

    result = assembler.assemble(source)

    assert result == [
        ("JUMP", 2),
        ("MOV", "R0", 100),
        ("MOV", "R0", 42),
    ]

def test_multiple_labels():
    assembler = Assembler()

    source = [
        ("LABEL", "START"),
        ("MOV", "R0", 10),

        ("LABEL", "LOOP"),
        ("SUB", "R0", 1),
        ("CMP", "R0", 0),
        ("JG", "LOOP"),

        ("LABEL", "END"),
        ("NOP",),
    ]

    result = assembler.assemble(source)

    assert result == [
        ("MOV", "R0", 10),
        ("SUB", "R0", 1),
        ("CMP", "R0", 0),
        ("JG", 1),
        ("NOP",),
    ]

    assert assembler.labels == {
        "START": 0,
        "LOOP": 1,
        "END": 4,
    }

def test_duplicate_label_raises():
    assembler = Assembler()

    source = [
        ("LABEL", "LOOP"),
        ("NOP",),
        ("LABEL", "LOOP"),
    ]

    with pytest.raises(ValueError, match="Duplicate label"):
        assembler.assemble(source)

def test_unknown_label_raises():
    assembler = Assembler()

    source = [
        ("MOV", "R0", 10),
        ("JG", "DOES_NOT_EXIST"),
    ]

    with pytest.raises(ValueError, match="Unknown label"):
        assembler.assemble(source)


def test_label_without_name_raises():
    assembler = Assembler()

    source = [
        ("LABEL",),
    ]

    with pytest.raises(ValueError, match="LABEL expects exactly one argument"):
        assembler.assemble(source)

def test_numeric_jump_is_not_modified():
    assembler = Assembler()

    source = [
        ("MOV", "R0", 10),
        ("JUMP", 0),
    ]

    result = assembler.assemble(source)

    assert result == [
        ("MOV", "R0", 10),
        ("JUMP", 0),
    ]

def test_assmbler_resets_labels_between_programs():
    assembler = Assembler()

    assembler.assemble([
        ("LABEL", "FIRST"),
        ("NOP",),
    ])

    assert "FIRST" in assembler.labels

    assembler.assemble([
        ("LABEL", "SECOND"),
        ("NOP",),
    ])

    assert "FIRST" not in assembler.labels
    assert "SECOND" in assembler.labels

def test_consecutive_labels_point_to_same_instruction():
    assembler = Assembler()

    source = [
        ("LABEL", "START"),
        ("LABEL", "ENTRY"),
        ("MOV", "R0", 42),
        ("JUMP", "START"),
    ]

    result = assembler.assemble(source)

    assert assembler.labels["START"] == 0
    assert assembler.labels["ENTRY"] == 0

    assert result == [
        ("MOV", "R0", 42),
        ("JUMP", 0),
    ]

@pytest.mark.parametrize(
    "opcode",
    ["JUMP", "JG", "JL", "JE"]
)

def test_all_jump_instructions_resolve_labels(opcode):
    assembler = Assembler()

    source = [
        ("LABEL", "TARGET"),
        ("NOP",),
        (opcode, "TARGET"),
    ]

    result = assembler.assemble(source)

    assert result == [
        ("NOP",),
        (opcode, 0),
    ]