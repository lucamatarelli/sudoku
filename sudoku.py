import random as rd

class SudokuGrid:
    m = ["A","B","C","D","E","F","G","H","I"]
    n = ["1","2","3","4","5","6","7","8","9"]

    def __init__(self):
        # Structure de la grille : [[[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]],
        #                           [[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]],
        #                           [[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]]]
        # Traduction de la structure d'une grille par imbrication de listes en compréhension (NB : dimensions non sujettes à variation) :
        self.grid = [[[[" " for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
        
        # Randomisation de la quantité de valeurs à préinsérer dans la grille :
        fillersAmount = rd.randint(10,20)
        for _ in range(fillersAmount):
            # Randomisation du jeu de coordonnées pour chacune des valeurs à préinsérer :
            fillerCoords = self.m[rd.randint(0,8)] + self.n[rd.randint(0,8)]
            # NB : Génération aléatoire sans remise :
            while self.getValue(fillerCoords) != " ":
                fillerCoords = self.m[rd.randint(0,8)] + self.n[rd.randint(0,8)]
            # Génération de la valeur en elle-même
            fillerValue = str(rd.randint(1,9))
            self.setValue(fillerCoords, fillerValue)
        print(fillersAmount)

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

    def getIndices(self, coords):
        coords = list(coords)
        if len(coords) != 2:
            print("Erreur : seulement 2 coordonnées à entrer")
            return
        elif (coords[0] not in self.m) or (coords[1] not in self.n):
            print("Erreur : format des coordonnées non valide")
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

            return (globalRow, globalCol, subgridRow, subgridCol)
    
    def getValue(self, coords):
        indices = self.getIndices(coords)
        if indices != None:
            globalRow, globalCol, subgridRow, subgridCol = indices
            return self.grid[globalRow][globalCol][subgridRow][subgridCol]

    def setValue(self, coords, value):
        if value not in self.n:
            print("Erreur : la valeur à insérer doit être un entier compris entre 1 et 9")
            return
        else:
            indices = self.getIndices(coords)
            if indices != None:
                globalRow, globalCol, subgridRow, subgridCol = indices
                self.grid[globalRow][globalCol][subgridRow][subgridCol] = value

    def isFillerValid(self, coords, value):
        indices = self.getIndices(coords)
        if indices != None:
            globalRow, globalCol, subgridRow, subgridCol = indices

            fillerRow = sum([self.grid[globalRow][i][subgridRow] for i in range(3)], [])
            fillerCol = [self.grid[i][globalCol][j][subgridCol] for i in range(3) for j in range(3)]
            fillerSubgrid = sum(self.grid[globalRow][globalCol], [])

            print(fillerRow)
            print(fillerCol)
            print(fillerSubgrid)
            
            if (value in fillerRow) or (value in fillerCol) or (value in fillerSubgrid):
                return False
            else:
                return True


newGame = SudokuGrid()
# newGame.setValue("F4", "9")
# newGame.setValue("F8", "4")
# newGame.setValue("G5", "3")
print(newGame)