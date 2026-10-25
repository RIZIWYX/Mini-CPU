# Roadmap : RG-8, un processeur 8 bits construit porte par porte

**Objectif final** : un CPU 8 bits dans Logisim-evolution, construit uniquement à partir de **portes logiques et de bascules** (aucun composant tout fait de Logisim : pas d'additionneur, de registre, de compteur, de RAM ni de ROM intégrés), programmable avec un assembleur Python et publié sur GitHub.

**Durée estimée** : 6 à 8 semaines, à raison de quelques heures par semaine.

**Règle du projet** : chaque bloc est un sous-circuit que tu as construit toi-même, testé seul avant d'être utilisé dans un bloc plus gros.

---

## Choix d'architecture : rester petit pour tout construire à la main

Construire 256 octets de mémoire porte par porte serait énorme (plus de 2 000 bascules). On adopte donc l'architecture classique des processeurs pédagogiques (type SAP-1) :

- **Données sur 8 bits** (UAL, accumulateur, sortie).
- **Adresses sur 4 bits**, soit **16 cases** de mémoire.
- **Instruction sur 8 bits** : 4 bits d'opcode et 4 bits d'adresse.
- **Mémoire programme** : 16 mots de 8 bits.
- **Mémoire de données** : 16 octets.

C'est assez pour faire tourner une multiplication, une boucle ou un compteur, et assez petit pour être construit entièrement à la main.

---

## Phase 0 : préparation (1 à 2 h)

- [ ] Créer le dépôt GitHub `rg8-cpu-logisim`, privé au début.
- [ ] Créer un dossier `tp/` avec les fichiers des TP d'origine (TP2, TP3, TP4, TP6, TP7, TP8), commit "base TP".
- [ ] Créer `circuits/rg8.circ`, le fichier principal où tu recopieras et amélioreras tes composants.
- [ ] Noter dans le README l'origine du projet : "Projet parti des TP de logique combinatoire et séquentielle de L1, étendu en processeur complet construit porte par porte".

## Phase 1 : jeu d'instructions (2 à 3 h, sans Logisim)

Format : `oooo aaaa` (opcode sur 4 bits, adresse ou valeur sur 4 bits).

| Opcode | Instruction | Effet |
|---|---|---|
| 0 | NOP | ne fait rien |
| 1 | LDA addr | ACC ← RAM[addr] |
| 2 | LDI val | ACC ← val (0 à 15) |
| 3 | STA addr | RAM[addr] ← ACC |
| 4 | ADD addr | ACC ← ACC + RAM[addr] |
| 5 | SUB addr | ACC ← ACC - RAM[addr] |
| 6 | AND addr | ACC ← ACC & RAM[addr] |
| 7 | OR addr | ACC ← ACC \| RAM[addr] |
| 8 | NOT | ACC ← non ACC |
| 9 | JMP addr | PC ← addr |
| A | JZ addr | si Z = 1 alors PC ← addr |
| B | JC addr | si C = 1 alors PC ← addr |
| C | JN addr | si N = 1 alors PC ← addr |
| E | OUT | SORTIE ← ACC |
| F | HLT | arrête l'horloge |

**Livrable** : `docs/isa.md`

---

## Phase 2 : bibliothèque de base (1 semaine) - reprend TP3 et TP4

Tous ces blocs sont construits uniquement avec des portes.

- [ ] **Demi-additionneur et additionneur complet** (TP3) : vérifier et nettoyer.
- [ ] **Additionneur 8 bits** : 8 additionneurs complets en cascade (ton `add8` du TP3).
- [ ] **Additionneur-soustracteur 8 bits** (TP3) : B passe par des XOR commandés par `sub`, et `sub` est injecté comme retenue d'entrée.
- [ ] **Décodeurs** : 2 vers 4 (TP4), puis **4 vers 16** construit avec des 2 vers 4. Il servira à l'adressage mémoire et au décodage de l'opcode.
- [ ] **Multiplexeurs** : 4 vers 1 sur 1 bit (TP4), puis versions **8 bits** (8 multiplexeurs en parallèle) et **16 vers 1**.

**Livrable** : sous-circuits `add_full`, `addsub8`, `dec2_4`, `dec4_16`, `mux4_8bits`, `mux16`, chacun testé.

## Phase 3 : l'UAL 8 bits (1 semaine) - reprend TP4

- [ ] Partir de ton **UAL 1 bit** du TP4 (NOT a, a OR b, a AND b, somme).
- [ ] Remplacer la somme par l'additionneur-soustracteur pour gérer SUB.
- [ ] Construire l'**UAL 8 bits** en chaînant 8 UAL 1 bit (ou deux UAL 4 bits du TP4).
- [ ] Produire les drapeaux (déjà vus au TP4) :
  - **Z** : NOR des 8 bits du résultat.
  - **N** : le bit 7 du résultat.
  - **C** : la retenue sortante.
  - **V** : dépassement signé (XOR des deux dernières retenues).
- [ ] Tester les cas limites : 0xFF + 0x01 → 0x00 avec C = 1 et Z = 1 ; 0x7F + 0x01 → 0x80 avec V = 1 et N = 1.

**Livrable** : `ual8` et `docs/tests.md`

## Phase 4 : registres (1 semaine) - reprend TP5 et TP6

- [ ] **Bascule D** construite avec des portes (NAND) : c'est le seul vrai composant de mémoire, tout le reste en découle.
- [ ] **Registre 1 bit** avec EN, R, W (ton `REGISTRE_1BI` du TP6).
- [ ] **Registre 8 bits** (8 registres 1 bit, comme ton `MOTS8`).
- [ ] **Registre 4 bits** pour les adresses.
- [ ] Instancier les registres du CPU :
  - **ACC** (8 bits) : l'accumulateur.
  - **IR** (8 bits) : le registre d'instruction.
  - **FLAGS** (4 bits) : Z, N, C, V mémorisés après chaque opération de l'UAL.
  - **OUT** (8 bits) : le registre de sortie.

**Livrable** : `bascule_d`, `reg1`, `reg4`, `reg8`, testés.

## Phase 5 : compteurs (3 à 5 jours) - reprend TP7

- [ ] **PC (compteur ordinal) 4 bits synchrone** avec bascules D, construit comme ton compteur du TP7.
- [ ] Ajouter le **chargement parallèle** (ton circuit `LOAD` du TP7) : quand Load = 1, PC prend la valeur de l'adresse. C'est le mécanisme des sauts.
- [ ] Ajouter une entrée **RAZ** pour redémarrer le programme.
- [ ] **Compteur d'étapes** (0 → 1 → 2 → 0) : c'est ton séquenceur 0 à 5 du TP7, réduit à 3 états.

**Livrable** : `pc4`, `compteur_etapes`, testés.

## Phase 6 : mémoires (1 semaine) - reprend TP6

- [ ] **RAM de données 16 × 8 bits** : 16 registres 8 bits, un décodeur 4 vers 16 pour choisir la case à écrire, et un multiplexeur 16 vers 1 (sur 8 bits) pour lire. C'est la version agrandie de ton `MOTS32` du TP6.
- [ ] **Mémoire programme 16 × 8 bits**, deux options :
  - **Option simple** : une "ROM" faite de 16 mots de **constantes** reliées au multiplexeur 16 vers 1. Pour changer de programme, tu modifies les constantes.
  - **Option avancée** : une seconde RAM 16 × 8 bits avec un mode **programmation** (interrupteurs pour l'adresse et la donnée, bouton d'écriture), comme sur les premiers ordinateurs.
- [ ] Tester l'écriture puis la relecture de chaque case.

**Livrable** : `ram16x8`, `rom16x8`, testés.

## Phase 7 : affichage (2 à 3 h) - reprend TP2

- [ ] Relier le registre **OUT** à ton convertisseur **OctetToBCD** (TP2).
- [ ] Brancher trois afficheurs 7 segments pilotés par ton décodeur `aff7dec` (TP2), pour afficher la valeur en décimal (0 à 255).
- [ ] Option : un second affichage en hexadécimal avec ton `affhexa`, pour PC et ACC (utile au débogage).

**Livrable** : `affichage_out`

## Phase 8 : chemin de données (1 semaine)

- [ ] Assembler dans un circuit `rg8` : PC, mémoire programme, IR, RAM, UAL, ACC, FLAGS, OUT.
- [ ] Ajouter tes multiplexeurs pour choisir :
  - l'entrée de l'ACC : RAM, UAL ou valeur immédiate (4 bits bas de l'IR, complétés par des zéros) ;
  - l'adresse de la RAM : les 4 bits bas de l'IR.
- [ ] Commander chaque signal avec des interrupteurs pour tester à la main une instruction complète.

**Livrable** : un CPU câblé, commandé à la main.

## Phase 9 : unité de commande (1 à 2 semaines, la plus difficile)

- [ ] Découper chaque instruction en étapes :
  - **T0 (fetch)** : IR ← PROG[PC]
  - **T1 (execute)** : selon l'opcode
  - **T2 (suivant)** : PC ← PC + 1, ou PC ← addr en cas de saut
- [ ] Décoder l'opcode avec ton **décodeur 4 vers 16** : une ligne active par instruction.
- [ ] Combiner chaque ligne d'instruction avec les étapes T0, T1, T2 à l'aide de portes AND et OR pour générer les signaux de commande (logique câblée, comme dans les vrais processeurs simples). Exemple : `W_ACC = T1 . (LDA + LDI + ADD + SUB + AND + OR + NOT)`.
- [ ] Sauts : `Load_PC = T2 . (JMP + JZ.Z + JC.C + JN.N)`.
- [ ] HLT : une bascule qui coupe l'horloge.
- [ ] Rédiger dans `docs/controle.md` le tableau des signaux actifs pour chaque instruction et chaque étape.

**Livrable** : un CPU qui exécute seul un programme.

## Phase 10 : programmes de test (2 à 3 h)

- [ ] **Addition** : 5 + 3 = 8.
- [ ] **Compte à rebours** : de 9 à 0 avec JZ.
- [ ] **Multiplication** : 6 × 7 = 42 par additions successives, affiché en décimal (démo principale).

**Livrable** : `programs/` avec résultats attendus.

## Phase 11 : assembleur Python (1 semaine)

- [ ] Traduire chaque instruction en un octet.
- [ ] Gérer les **étiquettes** (deux passes) et les directives de données (`.byte 7`).
- [ ] Gérer les commentaires (`;`), l'hexadécimal et le décimal.
- [ ] Afficher des **erreurs claires** avec numéro de ligne (instruction inconnue, étiquette absente, programme de plus de 16 instructions, valeur hors limites).
- [ ] Générer automatiquement les valeurs des constantes de la ROM, voire **modifier directement le fichier `.circ`** (c'est du XML) pour y injecter le programme.
- [ ] Tests avec `pytest`.

**Livrable** : `assembleur/assembleur.py` et ses tests.

## Phase 12 (bonus) : simulateur Python

- [ ] `simulateur.py` exécute le même code machine.
- [ ] Comparer les résultats avec Logisim.
- [ ] Mode pas à pas affichant PC, IR, ACC et les drapeaux.

## Phase 13 : publication (3 à 4 h)

- [ ] **README** :
  - L'accroche : "RG-8 : un processeur 8 bits construit porte par porte dans Logisim, avec son assembleur Python".
  - Un GIF de la multiplication qui affiche 42.
  - Un schéma de l'architecture (draw.io).
  - Un schéma de la **hiérarchie des composants** : porte → additionneur → UAL → CPU, bascule → registre → RAM.
  - Le jeu d'instructions et le mode d'emploi.
  - L'origine (les TP) et ce qui a été ajouté.
- [ ] Organisation du dépôt :

```
circuits/rg8.circ
assembleur/assembleur.py
assembleur/tests/
simulateur/simulateur.py
programs/*.asm
docs/isa.md
docs/controle.md
docs/tests.md
docs/architecture.png
tp/            (fichiers d'origine)
```

- [ ] Passer le dépôt en public, l'épingler sur GitHub, l'ajouter au portfolio (catégorie Dev - systèmes / bas niveau).

---

## Récapitulatif

| Phase | Contenu | TP repris | Durée |
|---|---|---|---|
| 0-1 | Préparation, jeu d'instructions | - | ~4 h |
| 2 | Additionneurs, décodeurs, multiplexeurs | TP3, TP4 | 1 sem. |
| 3 | UAL 8 bits + drapeaux | TP4 | 1 sem. |
| 4 | Bascule D, registres | TP5, TP6 | 1 sem. |
| 5 | PC et compteur d'étapes | TP7 | 3-5 j |
| 6 | RAM et ROM 16 × 8 | TP6 | 1 sem. |
| 7 | Affichage décimal | TP2 | ~3 h |
| 8 | Chemin de données | TP8 | 1 sem. |
| 9 | Unité de commande | TP7, TP8 | 1-2 sem. |
| 10 | Programmes de test | - | ~3 h |
| 11 | Assembleur Python | - | 1 sem. |
| 12 | Simulateur (bonus) | - | 3-5 j |
| 13 | Publication | - | ~4 h |

**Conseils** :
- Teste chaque sous-circuit seul avant de l'utiliser : une erreur dans un additionneur complet se retrouve multipliée par 8 dans l'UAL.
- Fais un commit à chaque composant terminé : l'historique Git montrera ta progression du bas vers le haut.
- Si le temps manque, garde la phase 9 en logique câblée et passe directement à la publication après la phase 11.
