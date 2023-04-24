import tkinter as tk
from random import randint, choice

Width = 500
Height = 500

root = tk.Tk()
root.title("2048")
canvas = tk.Canvas(width=Width, height=Height)
canvas.pack()


class Game:
    def __init__(self):
        self.rows = 5
        self.cols = 5
        self.box_size = 80
        self.x = (Width - self.rows * self.box_size) // 2
        self.y = (Height - self.cols * self.box_size) // 2
        self.playground = []
        self.create_playground()
        self.add_num_to_random_place()
        self.add_num_to_random_place()
        self.draw_playground()

    def restart(self, _):
        self.x = self.x
        self.y = self.y
        self.rows = self.rows
        self.cols = self.cols
        self.box_size = self.box_size
        self.playground = []
        self.create_playground()
        self.add_num_to_random_place()
        self.add_num_to_random_place()
        self.draw_playground()

    def create_playground(self):
        for row in range(self.cols):
            new_row = []
            for col in range(self.rows):
                new_row.append(0)
            self.playground.append(new_row)

    def draw_playground(self):
        canvas.delete("all")
        next_row = -self.box_size
        for row in self.playground:
            next_col = -self.box_size
            next_row += self.box_size
            for col in row:
                next_col += self.box_size
                canvas.create_rectangle(self.x + next_col, self.y + next_row,
                                        self.x + self.box_size + next_col, self.y + self.box_size + next_row, width=3)
                if col:
                    canvas.create_text(self.x + next_col + self.box_size // 2,
                                       self.y + next_row + self.box_size // 2,
                                       text=col, font=("Arial", 19))

    def add_num_to_random_place(self):
        free_rows = [i for i in self.playground if 0 in i]
        if free_rows:
            random_row = randint(0, len(free_rows)-1)
            random_free_row = free_rows[random_row]
            free_col_index = []
            for i in range(0, len(random_free_row)):
                if random_free_row[i] == 0:
                    free_col_index.append(i)
            random_col = choice(free_col_index)
            free_rows[random_row][random_col] = 2
        else:
            return "Full board"

    def nulls_to_side(self, row, left):
        new_row = []
        nulls = 0
        for num in row:
            if num:
                new_row.append(num)
            else:
                nulls += 1
        for null in range(nulls):
            if left:
                new_row.append(0)
            else:
                new_row.insert(0, 0)
        return new_row

    def move_rows(self, left):
        moved = False
        for j in range(self.cols):
            if sum(self.playground[j]) == 0:
                continue
            else:
                row = self.nulls_to_side(self.playground[j], left)
                if left:
                    start = 0
                    step = 1
                    end = self.rows - 1
                    next_tile = 1
                else:
                    start = self.rows - 1
                    step = -1
                    end = 0
                    next_tile = -1
                for i in range(start, end, step):
                    if row[i] == row[i + next_tile]:
                        row[i] += row[i + next_tile]
                        row[i + next_tile] = 0
                        row = self.nulls_to_side(row, left)
            if self.playground[j] != row:
                moved = True
            self.playground[j] = row
        if moved:
            self.add_num_to_random_place()
            self.draw_playground()

    def move_cols(self, up):
        moved = False
        for j in range(self.rows):
            cols = []
            for k in range(self.cols):
                cols.append(self.playground[k][j])
            if sum(cols) == 0:
                continue
            else:
                col = self.nulls_to_side(cols, up)
                if up:
                    start = 0
                    step = 1
                    end = self.cols - 1
                    next_tile = 1
                else:
                    start = self.cols - 1
                    step = -1
                    end = 0
                    next_tile = -1
                for i in range(start, end, step):
                    if col[i] == col[i + next_tile]:
                        col[i] += col[i + next_tile]
                        col[i + next_tile] = 0
                        col = self.nulls_to_side(col, up)
            if cols != col:
                moved = True
            for k in range(self.cols):
                self.playground[k][j] = col[k]
        if moved:
            self.add_num_to_random_place()
            self.draw_playground()

    def move_blocks(self, event):
        if event.keysym == "Left":
            self.move_rows(True)
        elif event.keysym == "Right":
            self.move_rows(False)
        elif event.keysym == "Up":
            self.move_cols(True)
        elif event.keysym == "Down":
            self.move_cols(False)


game = Game()


canvas.bind_all("<Key>", game.move_blocks)
canvas.bind_all("r", game.restart)
canvas.mainloop()
