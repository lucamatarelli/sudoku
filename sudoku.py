# Structure de la grille : [[[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]],
#                           [[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]],
#                           [[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]]]

class SudokuGrid:
    def __init__(self, filler):
        # Traduction de la structure d'une grille par imbrication de listes en compréhension (NB : dimensions non sujettes à variation)
        self.grid = [[[[filler for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
    def __str__(self):
        gridDisplay = "\n"
        for gridRow in self.grid:
            gridRowDisplay = ""
            # Formatage et séparateurs :
            for i in range(3):
                gridRowDisplay += str(gridRow[0][i]) + " | " + str(gridRow[1][i]) + " | " + str(gridRow[2][i]) + "\n"
            gridDisplay += str(gridRowDisplay) + 21 * "-" + "\n"
        # Nettoyage final de la chaine de caractères contenant la grille (remplacements chainés plus rapides) :
        gridDisplay = gridDisplay.replace("[","").replace("]","").replace(",","").replace("'","").rstrip("-\n")
        return gridDisplay

newGame = SudokuGrid("0")
print(newGame.grid)
print(newGame)