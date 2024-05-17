import tkinter as tk
import time

class Main:
    def __init__(self) -> None:
        self.N = 35
        self.tmp = None
        self.map = []
        self.cell_size = 25
        self.size = self.cell_size * self.N
        self.tk = tk.Tk()
        self.tk.title("Game of Life")
        self.cv = tk.Canvas(self.tk, height=self.size, width=self.size, bg='white')
        self.cv.pack()
        self.tk.title("Game of Life"+str(self.size)+"x"+str(self.size))
    
    def generate_map(self) -> None:
        self.map = [[0] * self.N for _ in range(self.N)]
    
    def put_life(self, starting_point_x, starting_point_y, life_array) -> None:
        xlen = len(life_array[0])
        ylen = len(life_array)

        for yi in range(ylen):
            for xj in range(xlen):
                if life_array[yi][xj] <= 0:
                    continue
                x = starting_point_x + xj
                y = starting_point_y + yi
                self.map[y][x] = life_array[yi][xj] if ( 0 <= x < self.N and 0 <= y < self.N ) else None

    def print_map(self):
        for row in self.map:
            print(row)
        print("-" * 10)

    def start2(self):
        self.tmp = [row.copy() for row in self.map]

        for yi in range(self.N):
            for xj in range(self.N):
                count = 0
                try:
                    count += 1 if self.tmp[yi+1][xj]   > 0 else 0
                    count += 1 if self.tmp[yi+1][xj+1] > 0 else 0
                    count += 1 if self.tmp[yi][xj+1]   > 0 else 0
                    count += 1 if self.tmp[yi-1][xj-1] > 0 else 0
                    count += 1 if self.tmp[yi-1][xj]   > 0 else 0
                    count += 1 if self.tmp[yi][xj-1]   > 0 else 0
                    count += 1 if self.tmp[yi-1][xj+1] > 0 else 0
                    count += 1 if self.tmp[yi+1][xj-1] > 0 else 0
                except:
                    pass
                
                if self.tmp[yi][xj] == 0:#white
                    if count == 3:#3
                        self.map[yi][xj] = 1
                else:#black
                    if count == 2 or count == 3:# 2 3
                        self.map[yi][xj] = 1
                    else:
                        self.map[yi][xj] = 0
    def show(self):
        self.cv.delete("all")
        cell_size = self.cell_size
        for y in range(self.N):
            for x in range(self.N):
                color = 'black' if self.map[y][x] > 0 else 'white'
                self.cv.create_rectangle(
                    x * cell_size, y * cell_size,
                    (x + 1) * cell_size, (y + 1) * cell_size,
                    fill=color,
                    outline='gray'
                )
        self.tk.update()
    
    def run(self):
        self.generate_map()
        self.put_life(2, 2, [[0, 0, 0, 1, 0],
                             [0, 1, 0, 0, 1],
                             [0, 0, 0, 1, 0],
                             [0, 0, 1, 1, 0],
                             [0, 0, 0, 0, 0]
                            ])
        self.show()
        self.tk.after(1000, self.update)

    def update(self):
        self.start2()
        self.show()
        self.tk.after(1000, self.update)


# メインプログラム
life_game = Main()
life_game.run()
life_game.print_map()
life_game.tk.mainloop()
