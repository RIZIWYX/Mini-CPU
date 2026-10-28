"""Assembleur du processeur RG-8.

Utilisation :
    python3 assembleur/assembleur.py programme.asm
    python3 assembleur/assembleur.py programme.asm --rom circuits/rg8.circ
"""
import re
import sys

# nom -> opcode
OPCODES = {
    "NOP": 0x0, "LDA": 0x1, "LDI": 0x2, "STA": 0x3,
    "ADD": 0x4, "SUB": 0x5, "AND": 0x6, "OR":  0x7,
    "NOT": 0x8, "JMP": 0x9, "JZ":  0xA, "JC":  0xB,
    "JN":  0xC, "OUT": 0xE, "HLT": 0xF,
}

SANS_OPERANDE = {"NOP", "NOT", "OUT", "HLT"}

TAILLE_ROM = 16


class ErreurAssemblage(Exception):
    """Erreur dans le programme, avec le numéro de ligne."""

    def __init__(self, numero, message):
        super().__init__(f"ligne {numero} : {message}")


def nettoyer(texte):
    """Renvoie la liste des (numéro, étiquette, instruction) utiles."""
    lignes = []
    for numero, ligne in enumerate(texte.splitlines(), start=1):
        ligne = ligne.split(";")[0].strip()
        if ligne == "":
            continue

        etiquette = None
        if ":" in ligne:
            etiquette, ligne = ligne.split(":", 1)
            etiquette = etiquette.strip()
            ligne = ligne.strip()
            if not re.fullmatch(r"[A-Za-z_]\w*", etiquette):
                raise ErreurAssemblage(numero, f"nom d'étiquette invalide '{etiquette}'")

        lignes.append((numero, etiquette, ligne))
    return lignes


def premier_passage(lignes):
    """Note l'adresse de chaque étiquette."""
    etiquettes = {}
    adresse = 0
    for numero, etiquette, instruction in lignes:
        if etiquette is not None:
            if etiquette in etiquettes:
                raise ErreurAssemblage(numero, f"étiquette '{etiquette}' définie deux fois")
            etiquettes[etiquette] = adresse
        if instruction != "":
            adresse += 1
    return etiquettes


def lire_operande(numero, texte, etiquettes):
    """Transforme '13', '0xD', '0b1101' ou 'boucle' en nombre de 0 à 15."""
    if texte in etiquettes:
        valeur = etiquettes[texte]
    else:
        try:
            valeur = int(texte, 0)
        except ValueError:
            raise ErreurAssemblage(numero, f"étiquette inconnue '{texte}'") from None
    if not 0 <= valeur <= 15:
        raise ErreurAssemblage(numero, f"opérande {valeur} hors limites (0 à 15)")
    return valeur


def assembler_instruction(numero, instruction, etiquettes):
    """Traduit 'ADD 13' en un octet (0x4D)."""
    morceaux = instruction.split()
    nom = morceaux[0].upper()

    # .byte : valeur brute
    if nom == ".BYTE":
        if len(morceaux) != 2:
            raise ErreurAssemblage(numero, ".byte attend une seule valeur")
        try:
            valeur = int(morceaux[1], 0)
        except ValueError:
            raise ErreurAssemblage(numero, f"valeur invalide '{morceaux[1]}'") from None
        if not 0 <= valeur <= 255:
            raise ErreurAssemblage(numero, f"valeur {valeur} hors limites (0 à 255)")
        return valeur

    if nom not in OPCODES:
        raise ErreurAssemblage(numero, f"instruction inconnue '{morceaux[0]}'")

    if nom in SANS_OPERANDE:
        if len(morceaux) != 1:
            raise ErreurAssemblage(numero, f"{nom} ne prend pas d'opérande")
        operande = 0
    else:
        if len(morceaux) != 2:
            raise ErreurAssemblage(numero, f"{nom} attend une opérande")
        operande = lire_operande(numero, morceaux[1], etiquettes)

    return (OPCODES[nom] << 4) | operande


def assembler_texte(texte):
    """Traduit tout un programme en une liste de 16 octets."""
    lignes = nettoyer(texte)
    etiquettes = premier_passage(lignes)

    octets = []
    for numero, _, instruction in lignes:
        if instruction == "":
            continue
        if len(octets) == TAILLE_ROM:
            raise ErreurAssemblage(numero, f"programme trop long (maximum {TAILLE_ROM} instructions)")
        octets.append(assembler_instruction(numero, instruction, etiquettes))

    octets += [0] * (TAILLE_ROM - len(octets))
    return octets


def ecrire_rom(chemin_circ, octets):
    """Remplace les 16 constantes du sous-circuit rom16x8 dans le fichier .circ."""
    with open(chemin_circ, encoding="utf-8") as f:
        texte = f.read()

    debut = texte.find('<circuit name="rom16x8">')
    if debut == -1:
        raise ValueError("sous-circuit rom16x8 introuvable dans le fichier")
    fin = texte.find("</circuit>", debut)
    rom = texte[debut:fin]

    motif = re.compile(
        r'<comp lib="0" loc="\((\d+),(\d+)\)" name="Constant"\s*/>'
        r'|<comp lib="0" loc="\((\d+),(\d+)\)" name="Constant">.*?</comp>',
        re.S,
    )
    constantes = list(motif.finditer(rom))
    if len(constantes) != TAILLE_ROM:
        raise ValueError(f"{len(constantes)} constantes trouvées dans rom16x8 au lieu de {TAILLE_ROM}")

    # adresse 0 = constante du haut
    def position(m):
        x = int(m.group(1) or m.group(3))
        y = int(m.group(2) or m.group(4))
        return (y, x)

    ordre = sorted(constantes, key=position)
    adresse = {id(m): i for i, m in enumerate(ordre)}

    def remplacer(m):
        x, y = position(m)[1], position(m)[0]
        valeur = octets[adresse[id(m)]]
        return (f'<comp lib="0" loc="({x},{y})" name="Constant">\n'
                f'      <a name="value" val="0x{valeur:02x}"/>\n'
                f'      <a name="width" val="8"/>\n'
                f'    </comp>')

    morceaux = []
    dernier = 0
    for m in constantes:
        morceaux.append(rom[dernier:m.start()])
        morceaux.append(remplacer(m))
        dernier = m.end()
    morceaux.append(rom[dernier:])
    nouvelle_rom = "".join(morceaux)

    with open(chemin_circ, "w", encoding="utf-8") as f:
        f.write(texte[:debut] + nouvelle_rom + texte[fin:])


def main(arguments):
    if len(arguments) not in (1, 3) or (len(arguments) == 3 and arguments[1] != "--rom"):
        print(__doc__)
        return 1

    try:
        with open(arguments[0], encoding="utf-8") as f:
            octets = assembler_texte(f.read())
    except FileNotFoundError:
        print(f"Erreur : fichier '{arguments[0]}' introuvable")
        return 1
    except ErreurAssemblage as e:
        print(f"Erreur {arguments[0]}, {e}")
        return 1

    print(" ".join(f"{o:02X}" for o in octets))

    if len(arguments) == 3:
        try:
            ecrire_rom(arguments[2], octets)
        except (OSError, ValueError) as e:
            print(f"Erreur : {e}")
            return 1
        print(f"ROM écrite dans {arguments[2]} (ferme Logisim avant, puis rouvre le fichier)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
