; Multiplication 6 x 7 = 42 par additions successives
; RAM[13] = résultat, RAM[14] = compteur, RAM[15] = constante 1

        LDI 0           ; résultat = 0
        STA 13
        LDI 7           ; compteur = 7
        STA 14
        LDI 1           ; constante 1
        STA 15

boucle: LDI 6           ; résultat = résultat + 6
        ADD 13
        STA 13
        LDA 14          ; compteur = compteur - 1
        SUB 15
        STA 14
        JZ fin          ; compteur = 0 : c'est fini
        JMP boucle      ; sinon on recommence

fin:    LDA 13
        OUT             ; affiche 42
