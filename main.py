from tkinter import Tk, BOTH, Canvas
import time
import random

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=True)

        self.__running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def get_canvas(self):
        return self.__canvas

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point1.x, self.point1.y,
            self.point2.x, self.point2.y,
            fill=fill_color, width=2
        )


class Cell:
    def __init__(self, win=None):
        self.__win = win
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False

        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1

    def draw(self, x1, y1, x2, y2, wall_color="black"):
        self.__x1, self.__y1, self.__x2, self.__y2 = x1, y1, x2, y2
        if not self.__win:
            return

        bg_color = "#d9d9d9"

        self.__win.draw_line(Line(Point(x1, y1), Point(x1, y2)),
                             wall_color if self.has_left_wall else bg_color)
        self.__win.draw_line(Line(Point(x1, y1), Point(x2, y1)),
                             wall_color if self.has_top_wall else bg_color)
        self.__win.draw_line(Line(Point(x2, y1), Point(x2, y2)),
                             wall_color if self.has_right_wall else bg_color)
        self.__win.draw_line(Line(Point(x1, y2), Point(x2, y2)),
                             wall_color if self.has_bottom_wall else bg_color)

    def draw_move(self, to_cell, undo=False):
        if not self.__win:
            return

        color = "gray" if undo else "red"
        x1 = (self.__x1 + self.__x2) // 2
        y1 = (self.__y1 + self.__y2) // 2
        x2 = (to_cell.__x1 + to_cell.__x2) // 2
        y2 = (to_cell.__y1 + to_cell.__y2) // 2
        self.__win.draw_line(Line(Point(x1, y1), Point(x2, y2)), color)


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []

        if seed is not None:
            random.seed(seed)

        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

    def __create_cells(self):
        for col in range(self.__num_cols):
            col_cells = []
            for row in range(self.__num_rows):
                cell = Cell(self.__win)
                col_cells.append(cell)
            self.__cells.append(col_cells)

        if self.__win:
            for i in range(self.__num_cols):
                for j in range(self.__num_rows):
                    self.__draw_cell(i, j)

    def __draw_cell(self, i, j):
        if not self.__win:
            return

        cell = self.__cells[i][j]
        x1 = self.__x1 + i * self.__cell_size_x
        y1 = self.__y1 + j * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        cell.draw(x1, y1, x2, y2)
        self.__animate()

    def __animate(self):
        if self.__win:
            self.__win.redraw()
            time.sleep(0.05)

    def __break_entrance_and_exit(self):
        entrance = self.__cells[0][0]
        entrance.has_top_wall = False
        self.__draw_cell(0, 0)

        exit_cell = self.__cells[self.__num_cols - 1][self.__num_rows - 1]
        exit_cell.has_bottom_wall = False
        self.__draw_cell(self.__num_cols - 1, self.__num_rows - 1)

    def __break_walls_r(self, i, j):
        current = self.__cells[i][j]
        current.visited = True

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)

        for dx, dy in directions:
            ni, nj = i + dx, j + dy
            if 0 <= ni < self.__num_cols and 0 <= nj < self.__num_rows:
                neighbor = self.__cells[ni][nj]
                if not neighbor.visited:
                    if dx == -1:
                        current.has_left_wall = False
                        neighbor.has_right_wall = False
                    elif dx == 1:
                        current.has_right_wall = False
                        neighbor.has_left_wall = False
                    elif dy == -1:
                        current.has_top_wall = False
                        neighbor.has_bottom_wall = False
                    elif dy == 1:
                        current.has_bottom_wall = False
                        neighbor.has_top_wall = False

                    self.__draw_cell(i, j)
                    self.__draw_cell(ni, nj)

                    self.__break_walls_r(ni, nj)

    def __reset_cells_visited(self):
        for col in self.__cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self.__solve_r(0, 0)

    def __solve_r(self, i, j):
        self.__animate()
        current = self.__cells[i][j]
        current.visited = True

        if i == self.__num_cols - 1 and j == self.__num_rows - 1:
            return True

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            ni, nj = i + dx, j + dy
            if 0 <= ni < self.__num_cols and 0 <= nj < self.__num_rows:
                neighbor = self.__cells[ni][nj]
                if not neighbor.visited:
                    if dx == -1 and not current.has_left_wall:
                        current.draw_move(neighbor)
                        if self.__solve_r(ni, nj):
                            return True
                        current.draw_move(neighbor, undo=True)
                    elif dx == 1 and not current.has_right_wall:
                        current.draw_move(neighbor)
                        if self.__solve_r(ni, nj):
                            return True
                        current.draw_move(neighbor, undo=True)
                    elif dy == -1 and not current.has_top_wall:
                        current.draw_move(neighbor)
                        if self.__solve_r(ni, nj):
                            return True
                        current.draw_move(neighbor, undo=True)
                    elif dy == 1 and not current.has_bottom_wall:
                        current.draw_move(neighbor)
                        if self.__solve_r(ni, nj):
                            return True
                        current.draw_move(neighbor, undo=True)
        return False


if __name__ == "__main__":
    win = Window(800, 600)

    maze = Maze(
        x1=50,
        y1=50,
        num_rows=10,
        num_cols=10,
        cell_size_x=40,
        cell_size_y=40,
        win=win,
        seed=0
    )

    maze.solve()
    win.wait_for_close()
