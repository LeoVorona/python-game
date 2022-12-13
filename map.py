from utils import randbool
from utils import randcell
from utils import randcell2


# 0 - 🟩
# 1 - 🌲
# 2 - 🌊
# 3 - 🏥
# 4 - 🏭
# 5 - 🔥

CELL_TYPES = '🟩🌲🌊🏥🏭🔥'
TREE_BONUS = 100
UPGRADE_COST = 2000 
LIFE_COST = 1000

class Map:

    def __init__(self,w,h):
        self.w = w
        self.h = h
        self.cells = [[0 for i in range (w)] for j in range(h)]
        self.generate_forest(3, 10)
        self.generate_river(10)
        self.generate_river(10)
        self.generate_upgrade_shop()
        self.generate_hospital()

    def check_bounds(self, x ,y):
        if (x < 0 or y < 0 or x >= self.h or y >= self.w):
            return False
        return True

    def print_map(self, hel, clouds):
        print("⬛" * (self.w +2))
        for ri in range(self.h):
            print("⬛", end='')
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if (clouds.cells[ri][ci] == 1):
                    print('⚪', end='')
                elif (clouds.cells[ri][ci] == 2):
                    print('🔵', end='')

                elif (hel.x == ri and hel.y == ci):
                    print('🚁', end='')
                elif (cell >= 0 and cell < len(CELL_TYPES)):
                    print(CELL_TYPES[cell], end='')    
            print("⬛")   
        print("⬛" * (self.w +2))  


    def generate_upgrade_shop(self):
        rc = randcell(self.w, self.h)
        rx, ry = rc[0], rc[1]   
        self.cells[rx][ry] = 4  
    
    def generate_hospital(self):
        rc = randcell(self.w, self.h)
        rx, ry = rc[0], rc[1]
        if self.cells[rx][ry] != 4:
            self.cells[rx][ry] = 3 
        else:
            self.generate_hospital()    


    def generate_river(self, l):
        rc = randcell(self.w, self.h)
        rx, ry = rc[0], rc[1]
        self.cells[rx][ry] = 2
        while l > 0:
            rc2 = randcell2(rx, ry)
            rx2, ry2 = rc2[0], rc2[1]
            if (self.check_bounds(rx2, ry2)):
                self.cells[rx2][ry2] = 2
                rx, ry = rx2, ry2
                l -= 1

    def generate_forest(self, r, mxr):
        for ri in range(self.h):
            for ci in range(self.w):
                if randbool(r, mxr):
                    self.cells[ri][ci] = 1

    def generate_tree(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if (self.check_bounds(cx, cy) and self.cells[cx][cy] == 0):
            self.cells[cx][cy] = 1


    def add_fire(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.cells[cx][cy] == 1:
            self.cells[cx][cy] = 5

    def update_fires(self):
        for ri in range(self.h):
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if cell == 5:
                    self.cells[ri][ci] = 0
        for i in range(10):        
            self.add_fire()


    def process_helicopter(self, hel, clouds):
        c = self.cells[hel.x][hel.y] 
        d = clouds.cells[hel.x][hel.y]
        if (c == 2):
            hel.tank = hel.mxtank
        if (c == 5 and hel.tank > 0):
            hel.tank -= 1
            hel.score += TREE_BONUS
            self.cells[hel.x][hel.y] = 1
        if (c == 4 and hel.score >= UPGRADE_COST):
            hel.mxtank += 1
            hel.score -= UPGRADE_COST
        if (c == 3 and hel.score >= LIFE_COST):
            hel.lives += 10
            hel.score -= LIFE_COST
        if (d == 2):
            hel.lives -= 1
            if (hel.lives <= 0):
                hel.game_over()


    def export_data(self):
        return{'cells':self.cells}

    def import_data(self,data):
        self.cells = data['cells'] or [[0 for i in range(self.w)]for j in range(self.h)]