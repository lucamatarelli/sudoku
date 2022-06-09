from sudokugrid import SudokuGrid


def main():
    player_difficulty_level = input(
        "\nChoisissez un niveau de difficulté (1 = Facile, 2 = Moyen, 3 = Difficile) : "
    )
    while player_difficulty_level not in ("1", "2", "3"):
        player_difficulty_level = input(
            "Entrez un niveau de difficulté valide (1, 2 ou 3): "
        )
    game = SudokuGrid(player_difficulty_level)
    player_action = ""
    while player_action != "3":
        print(game)
        print(
            "\033[1;33m[Dernière valeur insérée]\033[0;0m\n\033[1;36m[Précédentes valeurs insérées]\033[0;0m\n"
        )
        print(
            "Actions :\n1) Insérer/Remplacer/Supprimer un chiffre dans la grille\n2) Réinitialiser la grille\n3) Quitter le jeu\n"
        )
        if game.is_grid_complete():
            print("4) Valider votre grille\n")
        player_action = input("Entrez le numéro de l'action à effectuer : ")
        if player_action == "1":
            player_coords = input(
                "À quel emplacement souhaitez-vous insérer un chiffre ? "
            )
            player_value = input(
                "Quel chiffre souhaitez-vous insérer (NB : 0 pour vider une case) ? "
            )
            game.set_value(player_coords, player_value)
        elif player_action == "2":
            reset_confirmation = input(
                'Votre progression sera perdue. Entrez "reset" pour confirmer : '
            )
            if reset_confirmation == "reset":
                player_difficulty_level = input(
                    "\nChoisissez un niveau de difficulté (1 = Facile, 2 = Moyen, 3 = Difficile) : "
                )
                while player_difficulty_level not in ("1", "2", "3"):
                    player_difficulty_level = input(
                        "Entrez un niveau de difficulté valide (1, 2 ou 3): "
                    )
                game = SudokuGrid(player_difficulty_level)
        elif player_action == "4":
            if not game.is_grid_complete():
                continue
            elif game.is_grid_valid():
                print(
                    "\n\033[3;32mFélicitations ! Vous êtes parvenu à résoudre la grille !\033[0;0m\n"
                )
                break
            else:
                print(
                    "\n\033[3;31mLa grille n'est pas correcte... Courage, vous pouvez le faire !\033[0;0m"
                )


if __name__ == "__main__":
    main()
