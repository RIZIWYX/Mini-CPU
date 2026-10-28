; Compte à rebours : affiche 3, 2, 1, 0
        LDI 3
        STA 15          ; RAM[15] = compteur
        LDI 1
        STA 14          ; RAM[14] = constante 1
boucle: LDA 15
        OUT
        JZ fin          ; drapeaux du dernier SUB : 0 -> fini
        SUB 14
        STA 15
        JMP boucle
fin:    HLT
