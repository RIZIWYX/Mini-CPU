# RG-8 : un processeur 8 bits construit porte par porte

RG-8 est un processeur 8 bits conçu dans [Logisim-evolution](https://github.com/logisim-evolution/logisim-evolution), construit uniquement à partir de portes logiques et de bascules, sans aucun composant tout fait (additionneur, registre, compteur ou mémoire de la bibliothèque Logisim).

> Projet en cours de construction. Voir la [roadmap](docs/roadmap.md).

## Caractéristiques

- Données sur **8 bits**, adresses sur **4 bits**
- Mémoire programme de 16 mots et mémoire de données de 16 octets
- UAL 8 bits : ADD, SUB, AND, OR, NOT, avec les drapeaux Z, N, C et V
- 15 instructions, dont des sauts conditionnels (voir [le jeu d'instructions](docs/isa.md))
- Affichage du résultat en décimal sur des afficheurs 7 segments
- Assembleur Python (à venir)

## Hiérarchie des composants

```
portes logiques
├── additionneur complet → additionneur-soustracteur 8 bits → UAL 8 bits
├── décodeurs et multiplexeurs
└── bascule D → registres → RAM 16 × 8 bits
                         └── compteur ordinal
                                    ↓
                                  RG-8
```

## Organisation du dépôt

| Dossier | Contenu |
|---|---|
| `circuits/` | Le processeur (`rg8.circ`) |
| `docs/` | Architecture, roadmap, jeu d'instructions |
| `assembleur/` | Assembleur Python (à venir) |
| `programs/` | Programmes d'exemple (à venir) |

## Lancer le projet

1. Installer Logisim-evolution (version 3.8 ou supérieure).
2. Ouvrir `circuits/rg8.circ`.
3. Lancer la simulation avec `Simulation > Tics activés`.

## Auteur

Rayane Graïne - [GitHub](https://github.com/RIZIWYX) - [LinkedIn](https://linkedin.com/in/rayane-graine)
