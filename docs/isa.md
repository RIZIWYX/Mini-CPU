# Jeu d'instructions RG-8

## Format

Chaque instruction tient sur **8 bits** :

```
  7   6   5   4   3   2   1   0
+---+---+---+---+---+---+---+---+
|    opcode     |   opérande    |
+---+---+---+---+---+---+---+---+
```

- **opcode** (4 bits) : l'instruction à exécuter.
- **opérande** (4 bits) : une adresse de la RAM (0 à 15) ou une valeur immédiate (0 à 15).

## Registres

| Registre | Taille | Rôle |
|---|---|---|
| PC | 4 bits | Adresse de la prochaine instruction |
| IR | 8 bits | Instruction en cours |
| ACC | 8 bits | Accumulateur, reçoit les résultats |
| FLAGS | 4 bits | Drapeaux Z, N, C, V |
| OUT | 8 bits | Valeur affichée |

## Drapeaux

| Drapeau | Signification | Calcul |
|---|---|---|
| Z | Résultat nul | NOR des 8 bits du résultat |
| N | Résultat négatif | Bit 7 du résultat |
| C | Retenue | Retenue sortante de l'additionneur |
| V | Dépassement signé | XOR des retenues des bits 6 et 7 |

Les drapeaux sont mis à jour **uniquement** par ADD, SUB, AND, OR et NOT. LDA, LDI et STA ne les changent pas : un `JZ` placé après un `LDA` teste le résultat du calcul précédent.

Pour SUB, l'UAL calcule A + (non B) + 1 : C vaut 1 quand il n'y a **pas** d'emprunt (A ≥ B).

## Instructions

| Opcode | Mnémonique | Effet | Drapeaux |
|---|---|---|---|
| 0 | `NOP` | Ne fait rien | - |
| 1 | `LDA addr` | ACC ← RAM[addr] | - |
| 2 | `LDI val` | ACC ← val | - |
| 3 | `STA addr` | RAM[addr] ← ACC | - |
| 4 | `ADD addr` | ACC ← ACC + RAM[addr] | Z N C V |
| 5 | `SUB addr` | ACC ← ACC - RAM[addr] | Z N C V |
| 6 | `AND addr` | ACC ← ACC & RAM[addr] | Z N |
| 7 | `OR addr` | ACC ← ACC \| RAM[addr] | Z N |
| 8 | `NOT` | ACC ← non ACC | Z N |
| 9 | `JMP addr` | PC ← addr | - |
| A | `JZ addr` | si Z = 1 : PC ← addr | - |
| B | `JC addr` | si C = 1 : PC ← addr | - |
| C | `JN addr` | si N = 1 : PC ← addr | - |
| D | - | Réservé | - |
| E | `OUT` | OUT ← ACC | - |
| F | `HLT` | Arrête l'horloge | - |

## Cycle d'exécution

Chaque instruction s'exécute en 3 étapes :

| Étape | Nom | Action |
|---|---|---|
| T0 | Fetch | IR ← PROG[PC] |
| T1 | Execute | Selon l'opcode |
| T2 | Suivant | PC ← PC + 1, ou PC ← addr si saut |

## Exemple : 5 + 3

| Adresse | Code | Instruction |
|---|---|---|
| 0 | `25` | LDI 5 |
| 1 | `3F` | STA 15 |
| 2 | `23` | LDI 3 |
| 3 | `4F` | ADD 15 |
| 4 | `E0` | OUT |
| 5 | `F0` | HLT |

Résultat attendu : **8** affiché.
