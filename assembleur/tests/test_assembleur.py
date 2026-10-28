import os
import shutil
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from assembleur import ErreurAssemblage, assembler_texte, ecrire_rom  # noqa: E402

RACINE = os.path.join(os.path.dirname(__file__), "..", "..")


def octets(texte):
    return assembler_texte(texte)


# ---------- traduction ----------

def test_une_instruction():
    assert octets("ADD 13")[0] == 0x4D


def test_toutes_les_instructions():
    texte = "\n".join(["NOP", "LDA 1", "LDI 2", "STA 3", "ADD 4", "SUB 5", "AND 6", "OR 7",
                       "NOT", "JMP 9", "JZ 10", "JC 11", "JN 12", "OUT", "HLT"])
    assert octets(texte)[:15] == [0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
                                  0x80, 0x99, 0xAA, 0xBB, 0xCC, 0xE0, 0xF0]


def test_minuscules_acceptees():
    assert octets("ldi 5")[0] == 0x25


def test_hexa_et_binaire():
    assert octets("LDI 0xF\nLDI 0b101")[:2] == [0x2F, 0x25]


def test_commentaires_et_lignes_vides():
    assert octets("; titre\n\n  LDI 1   ; commentaire\n\nOUT")[:2] == [0x21, 0xE0]


def test_complete_avec_nop():
    resultat = octets("HLT")
    assert len(resultat) == 16
    assert resultat[1:] == [0] * 15


def test_directive_byte():
    assert octets(".byte 0xAB")[0] == 0xAB


# ---------- étiquettes ----------

def test_etiquette_en_arriere():
    assert octets("boucle: NOP\nJMP boucle")[:2] == [0x00, 0x90]


def test_etiquette_en_avant():
    assert octets("JZ fin\nNOP\nfin: HLT")[:3] == [0xA2, 0x00, 0xF0]


def test_etiquette_seule_sur_sa_ligne():
    assert octets("NOP\nfin:\nHLT\nJMP fin")[:3] == [0x00, 0xF0, 0x91]


def test_programme_multiplication():
    with open(os.path.join(RACINE, "programmes", "mult.asm"), encoding="utf-8") as f:
        assert octets(f.read()) == [0x20, 0x3D, 0x27, 0x3E, 0x21, 0x3F, 0x26, 0x4D,
                                    0x3D, 0x1E, 0x5F, 0x3E, 0xAE, 0x96, 0x1D, 0xE0]


# ---------- erreurs ----------

@pytest.mark.parametrize("texte, message", [
    ("FOO 3", "ligne 1 : instruction inconnue 'FOO'"),
    ("NOP\nJMP nulle_part", "ligne 2 : étiquette inconnue 'nulle_part'"),
    ("LDI 16", "ligne 1 : opérande 16 hors limites (0 à 15)"),
    ("LDI -1", "ligne 1 : opérande -1 hors limites (0 à 15)"),
    ("ADD", "ligne 1 : ADD attend une opérande"),
    ("ADD 1 2", "ligne 1 : ADD attend une opérande"),
    ("OUT 3", "ligne 1 : OUT ne prend pas d'opérande"),
    ("a: NOP\na: NOP", "ligne 2 : étiquette 'a' définie deux fois"),
    ("2x: NOP", "ligne 1 : nom d'étiquette invalide '2x'"),
    (".byte 300", "ligne 1 : valeur 300 hors limites (0 à 255)"),
    ("NOP\n" * 17, "ligne 17 : programme trop long (maximum 16 instructions)"),
])
def test_erreurs(texte, message):
    with pytest.raises(ErreurAssemblage) as erreur:
        octets(texte)
    assert str(erreur.value) == message


# ---------- écriture dans le .circ ----------

def test_ecrire_rom(tmp_path):
    copie = tmp_path / "rg8.circ"
    shutil.copy(os.path.join(RACINE, "circuits", "rg8.circ"), copie)
    programme = list(range(0x10, 0x20))
    ecrire_rom(str(copie), programme)

    texte = copie.read_text(encoding="utf-8")
    rom = texte[texte.find('<circuit name="rom16x8">'):]
    rom = rom[:rom.find("</circuit>")]
    for valeur in programme:
        assert f'val="0x{valeur:02x}"' in rom
