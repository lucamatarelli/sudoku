import random as rd
from itertools import product
from copy import deepcopy

class SudokuGrid:
    m = ("A","B","C","D","E","F","G","H","I")
    n = ("1","2","3","4","5","6","7","8","9")
    allCoords = list(product(m, n))

    def __init__(self, difficultyLevel):
        # Structure de la grille : [[[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]],
        #                           [[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]],
        #                           [[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]]]
        self.grid = [[[[" " for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.randomGenerate() # Génération aléatoire d'une grille de sudoku remplie et valide
        self.randomDeletion(difficultyLevel) # Suppression aléatoire de valeurs pour créer une grille jouable

    def __str__(self):
        gridDisplay = "\n"
        gridDisplay += "  | 1 2 3 | 4 5 6 | 7 8 9\n" # Axe des colonnes
        for i, gridRow in enumerate(self.grid):
            gridRowDisplay = ""
            for j in range(3):
                gridRowDisplay += self.m[(i*3)+j] + " | " + str(gridRow[0][j]) + " | " + str(gridRow[1][j]) + " | " + str(gridRow[2][j]) + "\n" # Axe des rangées et contenu
            gridDisplay += 25 * "-" + "\n" + str(gridRowDisplay)
        gridDisplay = gridDisplay.replace("[","").replace("]","").replace(",","").replace("'","") # Nettoyage final
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
            # coords[0] conditionne globalRow et subgridRow
            indexM = self.m.index(coords[0])
            globalRow = indexM // 3
            subgridRow = indexM - 3 * (globalRow)
            # coords[1] conditionne globalCol et subgridCol
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
        if value not in (self.n + ("0",)):
            print("Erreur : la valeur à insérer doit être un entier compris entre 1 et 9")
            return
        else:
            indices = self.getIndices(coords)
            if indices != None:
                globalRow, globalCol, subgridRow, subgridCol = indices
                if value == "0":
                    self.grid[globalRow][globalCol][subgridRow][subgridCol] = " "
                else:
                    self.grid[globalRow][globalCol][subgridRow][subgridCol] = value

    def isFillerValid(self, coords, value):
        if value not in self.n:
            print("Erreur : la valeur à insérer doit être un entier compris entre 1 et 9")
            return
        else:
            indices = self.getIndices(coords)
            if indices != None:
                globalRow, globalCol, subgridRow, subgridCol = indices

                fillerRow = sum([self.grid[globalRow][i][subgridRow] for i in range(3)], [])
                valueindexRow = self.n.index(coords[1])
                del fillerRow[valueindexRow]

                fillerCol = [self.grid[i][globalCol][j][subgridCol] for i in range(3) for j in range(3)]
                valueindexCol = self.m.index(coords[0])
                del fillerCol[valueindexCol]

                fillerSubgrid = sum(self.grid[globalRow][globalCol], [])
                valueIndexSubgrid = (valueindexCol % 3) * 3 + (valueindexRow % 3)
                del fillerSubgrid[valueIndexSubgrid]

                if (value in fillerRow) or (value in fillerCol) or (value in fillerSubgrid):
                    return False
                else:
                    return True

    def isGridComplete(self):
        for coords in self.allCoords:
            if self.getValue(coords) == " ":
                return False
        return True

    def isGridValid(self):
        for coords in self.allCoords:
            currentValue = self.getValue(coords)
            if not self.isFillerValid(coords, currentValue):
                return False
        return True

    def randomGenerate(self):
        for coords in self.allCoords:
            if self.getValue(coords) == " ":
                possibleValues = rd.sample(self.n, 9)
                for randomValue in possibleValues:
                    if self.isFillerValid(coords, randomValue):
                        self.setValue(coords, randomValue)
                        if self.isGridComplete():
                            return True
                        if self.randomGenerate():
                            return True
                break
        self.setValue(coords, "0")
        return False

    def randomDeletion(self, difficulty):
        if difficulty == "1":
            deletionsAmount = rd.randint(20,29)
        elif difficulty == "2":
            deletionsAmount = rd.randint(30,39)
        elif difficulty == "3":
            deletionsAmount = rd.randint(40,49)
        allCoords = deepcopy(self.allCoords)
        for _ in range(deletionsAmount):
            coords = rd.choice(allCoords)
            allCoords.remove(coords)
            self.setValue(coords, "0")


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
        if game.isGridValid():
            print("\nFélicitations ! Vous êtes parvenu à résoudre la grille !\n")
            break
        else:
            print("\nLa grille n'est pas correcte... Courage, vous pouvez le faire !")