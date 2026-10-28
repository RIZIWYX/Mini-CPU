# Table des instructions : nom -> opcode (les 4 bits de gauche)
OPCODES = {
    "NOP": 0x0, "LDA": 0x1, "LDI": 0x2, "STA": 0x3,
    "ADD": 0x4, "SUB": 0x5, "AND": 0x6, "OR":  0x7,
    "NOT": 0x8, "JMP": 0x9, "JZ":  0xA, "JC":  0xB,
    "JN":  0xC, "OUT": 0xE, "HLT": 0xF,
}


def assembler_ligne(ligne):
    """Traduit une ligne comme 'ADD 13' en un octet (0x4D)."""
    morceaux = ligne.split()          # 'ADD 13' -> ['ADD', '13']
    nom = morceaux[0].upper()         # 'ADD'
    opcode = OPCODES[nom]             # 0x4

    if len(morceaux) > 1:
        operande = int(morceaux[1], 0)  # '13' -> 13, '0xD' -> 13 aussi
    else:
        operande = 0                    # OUT, HLT, NOT... n'en ont pas

    return (opcode << 4) | operande   # 0x4 décalé de 4 bits, plus 13 -> 0x4D


if __name__ == "__main__":
    for l in ["LDI 6", "ADD 13", "JZ 14", "OUT", "HLT"]:
        print(f"{l:8} -> {assembler_ligne(l):02X}")
