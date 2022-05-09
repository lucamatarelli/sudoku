class SudokuGrid:
    m = ["A","B","C","D","E","F","G","H","I"]
    n = ["1","2","3","4","5","6","7","8","9"]

    def __init__(self, filler):
        # Structure de la grille : [[[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]],
        #                           [[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]],
        #                           [[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]]]
        # Traduction de la structure d'une grille par imbrication de listes en compréhension (NB : dimensions non sujettes à variation) :
        self.grid = [[[[filler for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]

    def __str__(self):
        gridDisplay = "\n"
        # Insertion de l'axe des colonnes :
        gridDisplay += "  | 1 2 3 | 4 5 6 | 7 8 9\n"
        for i, gridRow in enumerate(self.grid):
            gridRowDisplay = ""
            # Formatage des rangées (axe, sépérateurs et valeurs) :
            for j in range(3):
                gridRowDisplay += self.m[(i*3)+j] + " | " + str(gridRow[0][j]) + " | " + str(gridRow[1][j]) + " | " + str(gridRow[2][j]) + "\n"
            gridDisplay += 25 * "-" + "\n" + str(gridRowDisplay)
        # Nettoyage final de la chaine de caractères contenant la grille (remplacements chainés plus rapides) :
        gridDisplay = gridDisplay.replace("[","").replace("]","").replace(",","").replace("'","")
        return gridDisplay
    
    def insert(self, coords, value):
        coords = list(coords)
        if len(coords) != 2:
            print("Erreur : seulement 2 coordonnées à entrer")
            return
        elif (coords[0] not in self.m) or (coords[1] not in self.n):
            print("Erreur : format des coordonnées non valide")
            return
        elif value not in self.n:
            print("Erreur : la valeur à insérer doit être un chiffre compris entre 1 et 9")
            return
        else:
            # Accès type à une case : SudokuGrid.grid[rangée globale][colonne globale][rangée dans sous-grille][colonne dans sous-grille]
            # coords[0] conditionne globalRow + subgridRow
            indexM = self.m.index(coords[0])
            globalRow = indexM // 3
            subgridRow = indexM - 3 * (globalRow)
            # coords[1] conditionne globalCol + subgridCol
            indexN = self.n.index(coords[1])
            globalCol = indexN // 3
            subgridCol = indexN - 3 * (globalCol)

            self.grid[globalRow][globalCol][subgridRow][subgridCol] = value

newGame = SudokuGrid("_")
newGame.insert("F4", "9")
newGame.insert("F8", "4")
newGame.insert("G5", "3")
newGame.insert("A2", "2")
newGame.insert("H7", "5")
newGame.insert("A1", "7")
newGame.insert("I9", "4")
newGame.insert("H8", "1")
newGame.insert("C4", "2")
print(newGame.grid)
print(newGame)