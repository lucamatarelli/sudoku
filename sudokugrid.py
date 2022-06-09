import random as rd
from itertools import product
from copy import deepcopy


class SudokuGrid:
    """
    Représentation d'une grille de sudoku standard\n
    Attributs de classe :
    - ROWS : tuple contenant les valeurs (str) des rangées de la grille ("A" -> "I")
    - COLS : tuple contenant les valeurs (str) des colonnes de la grille ("1" -> "9")
    - ALL_COORDS : liste contenant toutes les coordonnées (str) de la grille ("A1" -> "I9")\n
    Attributs d'instance :
    - grid : structure de données contenant contenant la grille (liste quadruplement imbriquée)
    - initial_fillers_coords : liste des coordonnées (str) des valeurs initialement remplies
    - last_filler_coords : coordonnées (str) de la dernière valeur ajoutée dans la grille\n
    Méthodes :
    - game_display : renvoie l'affichage souhaité de certains éléments du jeu dans certaines couleurs sur le terminal.
    - get_indices : à partir de coordonnées, renvoie un tuple contenant les 4 entiers indexant successivement
        SudokuGrid.grid pour accéder à l'emplacement correspondant à ces coordonnées.
    - get_value : renvoie la valeur dans SudokuGrid.grid correspondant à des coordonnées données.
    - set_value : remplace, dans SudokuGrid.grid, la valeur correspondant à des coordonnées données par une valeur donnée.
    - is_filler_valid : renvoie la validité d'une valeur donnée à des coordonnées données de la grille, selon les 3 contraintes du sudoku
        (unicité dans la rangée, dans la colonne et dans la sous-grille).
    - is_grid_complete : renvoie l'état de complétion de la grille.
    - is_grid_valid : renvoie la validité globale de la grille.
    - random_generate : génère aléatoirement et récursivement une grille de sudoku (dans SudokuGrid.grid) complètement remplie et valide.
    - random_deletion : supprime aléatoirement des valeurs dans SudokuGrid.grid pour produire une grille jouable.
        Le niveau de difficulté choisi conditionne la quantité de valeurs supprimées.
    - existing_fillers : renvoie une liste contenant toutes les coordonnées d'emplacements non vides dans la grille.
    """

    ROWS = ("A", "B", "C", "D", "E", "F", "G", "H", "I")
    COLS = ("1", "2", "3", "4", "5", "6", "7", "8", "9")
    ALL_COORDS: list[str] = ["".join(coords) for coords in list(product(ROWS, COLS))]

    def __init__(self, difficulty_level: str):
        """
        Initialise une nouvelle grille de sudoku randomisée.
        Le niveau de difficulté choisi conditionne la quantité de valeurs initiales.
        pre: 1 <= difficulty_level <= 3
        post: une instance de SudokuGrid
        """
        # Structure de la grille (exemple avec 0 pour remplisseur fictif):
        # [
        #  [[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]],
        #  [[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]],
        #  [[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]]
        #  ]
        self.grid: list[list[list[list[str]]]] = [
            [[[" " for _ in range(3)] for _ in range(3)] for _ in range(3)]
            for _ in range(3)
        ]
        self.initial_fillers_coords = []
        self.random_generate()
        self.random_deletion(difficulty_level)
        self.initial_fillers_coords = self.existing_fillers()
        self.last_filler_coords = ""

    def __str__(self):
        """Renvoie la représentation textuelle affichable de la grille."""
        grid_display = "\n  | 1 2 3 | 4 5 6 | 7 8 9\n"
        for coords in self.ALL_COORDS:
            current_value = self.get_value(coords)
            if coords[1] == "1":
                if coords[0] == "A" or coords[0] == "D" or coords[0] == "G":
                    grid_display += 25 * "-" + "\n"
                grid_display += coords[0] + " |"
            elif coords[1] == "4" or coords[1] == "7":
                grid_display += " |"
            if coords in self.initial_fillers_coords:
                grid_display += " " + current_value
            elif coords == self.last_filler_coords:
                grid_display += " " + self.game_display(
                    current_value, "player_last_filler"
                )
            else:
                grid_display += " " + self.game_display(current_value, "player_filler")
            if coords[1] == "9":
                grid_display += "\n"
        return grid_display

    def game_display(self, text: str, mode: str) -> str:
        """Renvoie l'affichage souhaité de certains éléments du jeu dans certaines couleurs sur le terminal."""
        if mode == "error":
            text_out = f"\033[1;31m{text}\033[0;0m"
        elif mode == "player_filler":
            text_out = f"\033[1;36m{text}\033[0;0m"
        elif mode == "player_last_filler":
            text_out = f"\033[1;33m{text}\033[0;0m"
        return text_out

    def get_indices(self, coords: str) -> (tuple[int, int, int, int] | None):
        """
        À partir de coordonnées, Renvoie un tuple contenant les 4 entiers indexant successivement
        SudokuGrid.grid pour accéder à l'emplacement correspondant à ces coordonnées.
        pre: "A1" <= coords <= "I9"
        post: (indice de rangée globale, indice de colonne globale, indice de rangée dans la sous-grille, indice de colonne dans la sous-grille)
        """
        if len(coords) != 2:
            print(
                self.game_display("Erreur : seulement 2 coordonnées à entrer", "error")
            )
            return None
        elif (coords[0].upper() not in self.ROWS) or (coords[1] not in self.COLS):
            print(
                self.game_display("Erreur : format des coordonnées non valide", "error")
            )
            return None
        else:
            coords = coords.capitalize()
            # Accès type à une case : SudokuGrid.grid[rangée globale][colonne globale][rangée dans sous-grille][colonne dans sous-grille]
            # coords[0] conditionne global_row et subgrid_row
            index_row = self.ROWS.index(coords[0])
            global_row = index_row // 3
            subgrid_row = index_row - 3 * (global_row)
            # coords[1] conditionne global_col et subgrid_col
            index_col = self.COLS.index(coords[1])
            global_col = index_col // 3
            subgrid_col = index_col - 3 * (global_col)

            return (global_row, global_col, subgrid_row, subgrid_col)

    def get_value(self, coords: str) -> (str | None):
        """
        Renvoie la valeur dans SudokuGrid.grid correspondant à des coordonnées données.
        pre: "A1" <= coords <= "I9"
        post: "1" <= valeur <= "9" | " "
        """
        indices = self.get_indices(coords)
        if indices is not None:
            global_row, global_col, subgrid_row, subgrid_col = indices
            return self.grid[global_row][global_col][subgrid_row][subgrid_col]
        return None

    def set_value(self, coords: str, value: str) -> None:
        """
        Remplace, dans SudokuGrid.grid, la valeur correspondant à des coordonnées données par une valeur donnée.
        pre: "A1" <= coords <= "I9"
        pre: "0" <= value <= "9"
        post: /
        """
        if value not in (self.COLS + ("0",)):
            print(
                self.game_display(
                    "Erreur : la valeur à insérer doit être un entier compris entre 0 et 9\n(Vous pouvez vider une case en choisissant la valeur 0)",
                    "error",
                )
            )
            return
        else:
            indices = self.get_indices(coords)
            if indices is not None:
                if coords.capitalize() in self.initial_fillers_coords:
                    print(
                        self.game_display(
                            "Erreur : vous ne pouvez pas modifier les valeurs initiales de la grille",
                            "error",
                        )
                    )
                    return None
                global_row, global_col, subgrid_row, subgrid_col = indices
                if value == "0":
                    self.grid[global_row][global_col][subgrid_row][subgrid_col] = " "
                else:
                    self.grid[global_row][global_col][subgrid_row][subgrid_col] = value
                    self.last_filler_coords = coords.capitalize()

    def is_filler_valid(self, coords: str, value: str) -> (bool | None):
        """
        Renvoie la validité d'une valeur donnée à des coordonnées données de la grille,
        selon les 3 contraintes du sudoku (unicité dans la rangée, dans la colonne et dans la sous-grille).
        pre: "A1" <= coords <= "I9"
        pre: "0" <= value <= "9"
        post: True | False
        """
        indices = self.get_indices(coords)
        if indices is not None:
            global_row, global_col, subgrid_row, subgrid_col = indices

            filler_row: list[str] = sum(
                [self.grid[global_row][i][subgrid_row] for i in range(3)], []
            )
            value_index_row = self.COLS.index(coords[1])
            del filler_row[value_index_row]

            filler_col: list[str] = [
                self.grid[i][global_col][j][subgrid_col]
                for i in range(3)
                for j in range(3)
            ]
            value_index_col = self.ROWS.index(coords[0])
            del filler_col[value_index_col]

            filler_subgrid: list[str] = sum(self.grid[global_row][global_col], [])
            value_index_subgrid = (value_index_col % 3) * 3 + (value_index_row % 3)
            del filler_subgrid[value_index_subgrid]

            if (
                (value in filler_row)
                or (value in filler_col)
                or (value in filler_subgrid)
            ):
                return False
            else:
                return True
        return None

    def is_grid_complete(self) -> bool:
        """
        Renvoie l'état de complétion de la grille.
        pre: /
        post: True | False
        """
        for coords in self.ALL_COORDS:
            if self.get_value(coords) == " ":
                return False
        return True

    def is_grid_valid(self) -> bool:
        """
        Renvoie la validité globale de la grille.
        pre: /
        post: True | False
        """
        for coords in self.ALL_COORDS:
            current_value = self.get_value(coords)
            if not self.is_filler_valid(coords, current_value):
                return False
        return True

    def random_generate(self) -> bool:
        """
        Génère aléatoirement et récursivement une grille de sudoku (dans SudokuGrid.grid) complètement remplie et valide.
        pre: /
        post: True | False
        """
        for coords in self.ALL_COORDS:
            if self.get_value(coords) == " ":
                possible_values = rd.sample(self.COLS, 9)
                for random_value in possible_values:
                    if self.is_filler_valid(coords, random_value):
                        self.set_value(coords, random_value)
                        if self.is_grid_complete():
                            return True
                        if self.random_generate():
                            return True
                break
        self.set_value(coords, "0")
        return False

    def random_deletion(self, difficulty_level: str) -> None:
        """
        Supprime aléatoirement des valeurs dans SudokuGrid.grid pour produire une grille jouable.
        Le niveau de difficulté choisi conditionne la quantité de valeurs supprimées.
        pre: "1" <= difficulty_level <= "3"
        post: /
        """
        if difficulty_level == "1":
            deletions_amount = rd.randint(20, 29)
        elif difficulty_level == "2":
            deletions_amount = rd.randint(30, 39)
        elif difficulty_level == "3":
            deletions_amount = rd.randint(40, 49)
        all_coords = deepcopy(self.ALL_COORDS)
        for _ in range(deletions_amount):
            del_coords = rd.choice(all_coords)
            all_coords.remove(del_coords)
            self.set_value(del_coords, "0")

    def existing_fillers(self) -> list[str]:
        """
        Renvoie une liste contenant toutes les coordonnées d'emplacements non vides dans la grille.
        pre: /
        post: liste de coordonnées ("A1" -> "I9")
        """
        fillers_coords = []
        for coords in self.ALL_COORDS:
            if self.get_value(coords) != " ":
                fillers_coords.append(coords)
        return fillers_coords
