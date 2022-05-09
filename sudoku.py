# Structure de la grille : [[[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]],
#                           [[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]],
#                           [[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]]]

class SudokuGrid:
    def __init__(self, filler):
        # Traduction de la structure d'une grille par imbrication de listes en compréhension (NB : dimensions non sujettes à variation)
        self.grid = [[[[filler for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]

    def __str__(self):
        gridDisplay = "\n"
        # Insertion de l'axe des colonnes :
        gridDisplay += "  | 1 2 3 | 4 5 6 | 7 8 9\n"
        # Axe des rangées, insérées lors du passage de la boucle imbriquée :
        rowsAxis = ["A","B","C","D","E","F","G","H","I"]
        for i, gridRow in enumerate(self.grid):
            gridRowDisplay = ""
            # Formatage des rangées (axe, sépérateurs et valeurs) :
            for j in range(3):
                gridRowDisplay += rowsAxis[(i*3)+j] + " | " + str(gridRow[0][j]) + " | " + str(gridRow[1][j]) + " | " + str(gridRow[2][j]) + "\n"
            gridDisplay += 25 * "-" + "\n" + str(gridRowDisplay)
        # Nettoyage final de la chaine de caractères contenant la grille (remplacements chainés plus rapides) :
        gridDisplay = gridDisplay.replace("[","").replace("]","").replace(",","").replace("'","")
        return gridDisplay
    
    def insert(self, coords, value):
        pass

newGame = SudokuGrid("8")
# print(newGame.grid)
print(newGame)
newGame.insert("B6", 4)