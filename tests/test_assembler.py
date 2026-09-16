from PyCPU.program.assembler import Assembler
import pytest

def test_compile_program_without_labels():
    assembler = Assembler()

    source = [
        ("MOV", "R0", 10),
        ("ADD", "R0", 1),
    ]

    result = assembler.compile(source)

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

    result = assembler.compile(source)

    assert result == [
        ("MOV", "R0", 10),
        ("SUB", "R0", 1),
        ("CMP", "R0", 0),
        ("JG", 1),
    ]

def test_forward_label():
    assembler = assembler()

    source = [
        ("JUMP", "START"),
        ("MOV", "R0", 100),
        ("LABEL", "START"),
        ("MOV", "R0", 42),
    ]

    result = assembler.compile(source)

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

    result = assembler.compile(source)

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
        assembler.compile(source)

def test_unknown_label_raises():
    assembler = Assembler()

    source = [
        ("MOV", "R0", 10),
        ("JG", "DOES_NOT_EXIST"),
    ]

    with pytest.raises(ValueError, match="Unknown label"):
        assembler.compile(source)

def test_label_without_name_raises():
    assembler = Assembler()

    source = [
        ("LABEL",),
    ]

    with pytest.raises(ValueError, match="LABEL expects exactly one argument"):
        assembler.compile(source)

def test_label_without_name_raises():
    assembler = Assembler()

    source = [
        ("LABEL",),
    ]

    with pytest.raises(ValueError, match="LABEL expects exactly one argument"):
        assembler.compile(source)

def test_numeric_jump_is_not_modified():
    assembler = Assembler()

    source = [
        ("MOV", "R0", 10),
        ("JUMP", 0),
    ]

    result = assembler.compile(source)

    assert result == [
        ("MOV", "R0", 10),
        ("JUMP", 0),
    ]