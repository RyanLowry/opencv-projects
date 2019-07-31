class Grid():
    # list [x,y],[x,y]
    def __init__(self,cameraSize,gridSize):
        self.gridSize = gridSize
        self.cameraSize = cameraSize

        self.grid = [[0] * self.gridSize[0] for i in range(self.gridSize[1])]
        self.fill_grid()

    def fill_grid(self):
        currY = 0
        yRange = self.cameraSize[1] / self.gridSize[1]
        for x in range(0,self.gridSize[0]):
            currY += yRange
            currX = 0
            xRange =  self.cameraSize[0] / self.gridSize[0]
            for y in range(0,self.gridSize[1]):
                currX += xRange
                print(self.grid[x][y])
                self.grid[x][y] = [int(currX),int(currY)]
                
    def contains_in(self,pos):
        return (self._contains_in_x(pos[0]),self._contains_in_y(pos[1]))

    def _contains_in_x(self,posX):
        #Loop values with same y pos
        for i,x in enumerate(self.grid[0]):
            if i == 0:
                if posX < x[0]:
                    return i
            else:
                if posX > self.grid[0][i-1][0] and posX < self.grid[0][i][0]:
                    return i

    def _contains_in_y(self,posY):
        #Loop values with same x pos
        for i,y in enumerate(self.grid):
            if i == 0:
                if posY < self.grid[i][0][1]:
                    return i
            else:
                if posY > self.grid[i-1][0][1] and posY < self.grid[i][0][1]:
                    return i