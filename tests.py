# tests.py
import unittest
from main import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._Maze__cells), num_cols)
        self.assertEqual(len(m1._Maze__cells[0]), num_rows)

    def test_different_maze_size(self):
        m2 = Maze(0, 0, 5, 8, 20, 20)
        self.assertEqual(len(m2._Maze__cells), 8)
        self.assertEqual(len(m2._Maze__cells[0]), 5)

    def test_single_cell(self):
        m3 = Maze(0, 0, 1, 1, 40, 40)
        self.assertEqual(len(m3._Maze__cells), 1)
        self.assertEqual(len(m3._Maze__cells[0]), 1)

    def test_break_entrance_and_exit(self):
        maze = Maze(0, 0, 5, 5, 10, 10)

        entrance = maze._Maze__cells[0][0]
        exit_cell = maze._Maze__cells[4][4]

        self.assertFalse(entrance.has_top_wall)
        self.assertFalse(exit_cell.has_bottom_wall)

if __name__ == "__main__":
    unittest.main()
