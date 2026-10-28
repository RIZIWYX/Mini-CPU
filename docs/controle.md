# Unité de commande

L'unité de commande (`commande`) décide, à chaque étape, quels registres écrivent et ce que fait l'UAL. Elle est en **logique câblée** : uniquement des portes AND et OR derrière un décodeur 4 vers 16.

## Le cycle en 3 étapes

Chaque instruction prend 3 coups d'horloge. Le circuit `etapes` est un compteur en anneau à 2 bascules :

| Étape | Nom | Action |
|---|---|---|
| T0 | Fetch | IR ← ROM[PC] |
| T1 | Execute | Selon l'opcode : calcul, chargement, écriture en RAM… |
| T2 | Suivant | PC ← PC + 1, ou PC ← adresse si le saut est pris |

## Entrées

| Entrée | Taille | Origine |
|---|---|---|
| `t0`, `t1`, `t2` | 1 bit chacune | Compteur d'étapes |
| `opcode` | 4 bits | Les 4 bits de gauche de l'IR |
| `z`, `c`, `n` | 1 bit chacune | Sortie du registre FLAGS |

L'opcode passe dans un `dec4_16` : une seule sortie `Bk` vaut 1, celle de l'instruction en cours (B4 pour ADD, B9 pour JMP…).

## Sorties et équations

| Signal | Rôle | Équation |
|---|---|---|
| `en_ir` | écrire l'IR | `t0` |
| `en_pc` | écrire le PC | `t2` |
| `en_acc` | écrire l'ACC | `t1 · (LDA + LDI + ADD + SUB + AND + OR + NOT)` |
| `en_flag` | écrire FLAGS | `t1 · (ADD + SUB + AND + OR + NOT)` |
| `en_ram` | écrire la RAM | `t1 · STA` |
| `en_out` | écrire OUT | `t1 · OUT` |
| `hlt` | arrêter l'horloge | `t1 · HLT` |
| `sub` | soustraction dans l'UAL | `SUB` |
| `op[0]` | choix de l'opération UAL | `AND + NOT` |
| `op[1]` | choix de l'opération UAL | `OR + NOT` |
| `src[0]` | source de l'ACC | `LDA` |
| `src[1]` | source de l'ACC | `LDI` |
| `saut` | charger l'adresse dans le PC | `JMP + JZ · z + JC · c + JN · n` |

### Opérations de l'UAL (`op`)

| `op` | Opération |
|---|---|
| 00 | ADD ou SUB (selon `sub`) |
| 01 | AND |
| 10 | OR |
| 11 | NOT |

### Source de l'ACC (`src`)

| `src` | L'ACC reçoit |
|---|---|
| 00 | le résultat de l'UAL |
| 01 | la RAM (LDA) |
| 10 | la valeur immédiate, les 4 bits de droite de l'IR (LDI) |

## Horloge et écritures

- Le compteur d'étapes avance au **front montant** de l'horloge.
- Les registres écrivent au **milieu de l'étape**, quand l'horloge repasse à 0 : chaque signal d'écriture vaut `en_x AND nclk`, avec `nclk = NOR(clk, raz)`.
- Les signaux de commande ont ainsi le temps de se stabiliser avant l'écriture, et `raz` bloque toute écriture pendant la remise à zéro.

## HLT

L'instruction HLT met à 1 la bascule « arrêt » par son entrée `s`. Sa sortie inversée coupe l'horloge du compteur d'étapes (porte AND) : le processeur se fige. `raz` remet la bascule à 0 et relance le processeur.

## À savoir pour programmer

Seules ADD, SUB, AND, OR et NOT mettent à jour les drapeaux. Un `JZ` placé juste après un `LDA` teste donc le résultat du **calcul précédent**, pas la valeur chargée.
