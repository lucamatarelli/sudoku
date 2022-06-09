import random as rd
from itertools import product
from copy import deepcopy


class SudokuGrid:
    ROWS = ("A", "B", "C", "D", "E", "F", "G", "H", "I")
    COLS = ("1", "2", "3", "4", "5", "6", "7", "8", "9")
    ALL_COORDS = ["".join(coords) for coords in list(product(ROWS, COLS))]

    def __init__(self, difficulty_level: str):
        # Structure de la grille : [[[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]],
        #                           [[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]],
        #                           [[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]]]
        self.grid = [
            [[[" " for _ in range(3)] for _ in range(3)] for _ in range(3)]
            for _ in range(3)
        ]
        self.initial_fillers_coords = []
        # Génération aléatoire d'une grille de sudoku remplie et valide
        self.random_generate()
        # Suppression aléatoire de valeurs pour créer une grille jouable
        self.random_deletion(difficulty_level)
        # Attribut contenant la collection de toutes les valeurs initialement remplies par la machine, afin de garantir leur immutabilité
        self.initial_fillers_coords = self.existing_fillers()
        self.last_filler_coords = ""

    def __str__(self):
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
        if mode == "error":
            text_out = f"\033[1;31m{text}\033[0;0m"
        elif mode == "player_filler":
            text_out = f"\033[1;36m{text}\033[0;0m"
        elif mode == "player_last_filler":
            text_out = f"\033[1;33m{text}\033[0;0m"
        return text_out

    def get_indices(self, coords: str) -> (tuple[int, int, int, int] | None):
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
        indices = self.get_indices(coords)
        if indices is not None:
            global_row, global_col, subgrid_row, subgrid_col = indices
            return self.grid[global_row][global_col][subgrid_row][subgrid_col]
        return None

    def set_value(self, coords: str, value: str) -> None:
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
        for coords in self.ALL_COORDS:
            if self.get_value(coords) == " ":
                return False
        return True

    def is_grid_valid(self) -> bool:
        for coords in self.ALL_COORDS:
            current_value = self.get_value(coords)
            if not self.is_filler_valid(coords, current_value):
                return False
        return True

    def random_generate(self) -> bool:
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
        fillers_coords = []
        for coords in self.ALL_COORDS:
            if self.get_value(coords) != " ":
                fillers_coords.append(coords)
        return fillers_coords
