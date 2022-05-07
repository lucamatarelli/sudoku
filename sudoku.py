# Structure de la grille : [[[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]],
#                           [[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]],
#                           [[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]]]

class SudokuGrid:
    def __init__(self, filler):
        # Traduction de la structure d'une grille par imbrication de listes en compréhension (NB : dimensions non sujettes à variation)
        self.grid = [[[[filler for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
    def __str__(self):
        return self

newGame = SudokuGrid(7)
print(newGame.grid)