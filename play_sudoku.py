from sudokugrid import SudokuGrid


def main():
    difficultyLevelPlayer = input("\nChoisissez un niveau de difficulté (1 = Facile, 2 = Moyen, 3 = Difficile) : ")
    while difficultyLevelPlayer not in ("1","2","3"):
        difficultyLevelPlayer = input("Entrez un niveau de difficulté valide (1, 2 ou 3): ")
    game = SudokuGrid(difficultyLevelPlayer)
    playerAction = ""
    while playerAction != "3":
        print(game)
        print("Actions :\n1) Insérer/Remplacer un chiffre dans la grille\n2) Réinitialiser la grille\n3) Quitter le jeu\n")
        if game.isGridComplete():
            print("4) Valider votre grille\n")
        playerAction = input("Entrez le numéro de l'action à effectuer : ")
        if playerAction == "1":
            playerCoords = input("À quel emplacement souhaitez-vous insérer un chiffre ? ")
            playerValue = input("Quel chiffre souhaitez-vous insérer ? ")
            game.setValue(playerCoords, playerValue)
        elif playerAction == "2":
            resetConfirmation = input("Votre progression sera perdue. Entrez \"reset\" pour confirmer : ")
            if resetConfirmation == "reset":    
                difficultyLevelPlayer = input("\nChoisissez un niveau de difficulté (1 = Facile, 2 = Moyen, 3 = Difficile) : ")
                while difficultyLevelPlayer not in ("1","2","3"):
                    difficultyLevelPlayer = input("Entrez un niveau de difficulté valide (1, 2 ou 3): ")
                game = SudokuGrid(difficultyLevelPlayer)
        elif playerAction == "4":
            if not game.isGridComplete():
                continue
            elif game.isGridValid():
                print("\nFélicitations ! Vous êtes parvenu à résoudre la grille !\n")
                break
            else:
                print("\nLa grille n'est pas correcte... Courage, vous pouvez le faire !")


if __name__ == "__main__":
    main()