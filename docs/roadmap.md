# Roadmap : RG-8, un processeur 8 bits construit porte par porte

**Objectif** : un CPU 8 bits dans Logisim-evolution, construit uniquement à partir de portes logiques (aucun additionneur, registre, compteur ni mémoire tout fait), programmable avec un assembleur Python.

**Règle du projet** : chaque bloc est un sous-circuit testé seul avant d'être utilisé dans un bloc plus gros. Voir [architecture.md](architecture.md) pour savoir qui utilise qui.

## Architecture retenue

- Données sur **8 bits**, adresses sur **4 bits** (16 cases)
- Instruction sur 8 bits : 4 bits d'opcode + 4 bits d'opérande (voir [isa.md](isa.md))
- Mémoire programme 16 × 8 bits, mémoire de données 16 × 8 bits

---

## Phase 1 : jeu d'instructions ✅

- [x] Définir les instructions et leur encodage (`docs/isa.md`)

## Phase 2 : arithmétique ✅

- [x] Demi-additionneur, additionneur complet
- [x] Additionneurs 4 et 8 bits
- [x] Additionneur-soustracteur 8 bits (XOR sur B, `sub` en retenue d'entrée)

## Phase 3 : sélection ✅

- [x] Décodeurs 2 vers 4 et 4 vers 16
- [x] Multiplexeurs 4 vers 1 (1 bit et 8 bits) et 16 vers 1 (8 bits)

## Phase 4 : UAL 8 bits ✅

- [x] ADD, SUB, AND, OR, NOT
- [x] Drapeaux Z, N, C, V

## Phase 5 : mémorisation ✅

- [x] Verrou D en portes NAND, avec mise à 1 et remise à zéro
- [x] Bascule D maître-esclave
- [x] Registres 1, 4 et 8 bits
- [x] RAM 16 × 8 bits

## Phase 6 : compteurs

- [x] Compteur 3 bits avec chargement
- [ ] **PC (compteur ordinal) 4 bits** : `reg4` + `add4` (+1) + multiplexeur pour charger l'adresse d'un saut
- [ ] **Compteur d'étapes** T0 → T1 → T2 → T0

## Phase 7 : mémoire programme

- [ ] ROM 16 × 8 bits : 16 constantes + `mux16_8`

## Phase 8 : affichage

- [ ] Convertisseur octet → décimal (BCD) en portes, algorithme « double dabble »
- [ ] Trois afficheurs 7 segments pilotés par `seg7_dec`

## Phase 9 : chemin de données

- [ ] Relier PC, ROM, IR, RAM, UAL, ACC, FLAGS et OUT
- [ ] Multiplexeur devant l'ACC : RAM, UAL ou valeur immédiate
- [ ] Bouton RESET relié à tous les `raz`

## Phase 10 : unité de commande

- [ ] Cycle en 3 étapes : T0 fetch, T1 execute, T2 suivant
- [ ] Décodage de l'opcode avec `dec4_16`
- [ ] Génération des signaux de commande en logique câblée
- [ ] Sauts conditionnels JZ, JC, JN
- [ ] HLT
- [ ] Respecter la règle : `EN` et les adresses ne changent que quand `W` vaut 0
- [ ] Documenter les signaux dans `docs/controle.md`

## Phase 11 : programmes de test

- [ ] Addition 5 + 3
- [ ] Compte à rebours de 9 à 0
- [ ] Multiplication 6 × 7 = 42 (démo principale)

## Phase 12 : assembleur Python

- [ ] Traduction des instructions en octets
- [ ] Étiquettes (deux passes) et directive `.byte`
- [ ] Commentaires, valeurs hexadécimales et décimales
- [ ] Messages d'erreur avec numéro de ligne
- [ ] Génération du contenu de la ROM dans le fichier `.circ`
- [ ] Tests `pytest`

## Phase 13 (bonus) : simulateur Python

- [ ] Exécution du même code machine, mode pas à pas

## Phase 14 : publication

- [ ] Supprimer les circuits inutilisés (`ual1`)
- [ ] README final : GIF de démo, schéma, jeu d'instructions
- [ ] Passer le dépôt en public, l'épingler, l'ajouter au portfolio
