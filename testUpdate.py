import unittest
from random import randint

from TicTacToe import TicTacToe


class TestTicTacToe(unittest.TestCase):
    def setUp(self):
        self.ttt = TicTacToe()  # 假设TicTacToe类已经定义

    def test_normal_moves(self):
        """测试正常下棋"""
        # 测试1：第一步落子
        new_board = [[0, 0, 0], [0, -1, 0], [0, 0, 0]]
        is_valid, actions = self.ttt.try_update_board(new_board)
        print(is_valid, actions)
        self.assertTrue(is_valid)
        self.assertIsNone(actions)

        # 测试2：连续正常落子
        self.ttt._board = [[0, 0, 0], [0, -1, 0], [1, 0, 0]]
        new_board = [[0, -1, 0], [0, -1, 0], [1, 0, 0]]
        is_valid, actions = self.ttt.try_update_board(new_board)
        print(is_valid, actions)
        self.assertTrue(is_valid)
        self.assertIsNone(actions)

        # 测试3：棋盘即将下满时的正常落子
        self.ttt._board = [[-1, 1, -1], [1, -1, 1], [1, 0, -1]]
        new_board = [[-1, 1, -1], [1, -1, 1], [1, -1, -1]]
        is_valid, actions = self.ttt.try_update_board(new_board)
        print(is_valid, actions)
        self.assertTrue(is_valid)
        self.assertIsNone(actions)

    def test_move_pieces(self):
        """测试移动已经落下的棋子"""
        # 测试1：移动一个棋子
        self.ttt._board = [[0, 0, 0], [0, -1, 0], [0, 0, 0]]
        new_board = [[0, -1, 0], [0, 0, 0], [0, 0, 0]]
        is_valid, actions = self.ttt.try_update_board(new_board)
        print(is_valid, actions)
        self.assertFalse(is_valid)
        self.assertEqual(actions, [(0, 1, 1, 1)])

        # 测试2：移动多个棋子
        self.ttt._board = [[1, 0, -1], [0, -1, 0], [0, 0, 1]]
        new_board = [[0, 1, 0], [-1, -1, 0], [1, 0, 0]]
        is_valid, actions = self.ttt.try_update_board(new_board)
        print(is_valid, actions)
        self.assertFalse(is_valid)
        self.assertEqual(set(actions), {(0, 1, 0, 0), (1, 0, 0, 2), (2, 0, 2, 2)})

    def test_multiple_moves(self):
        """测试一次落下多个棋子"""
        # 测试1：落下两个棋子
        self.ttt._board = [[0, 0, 0], [0, -1, 0], [0, 0, 0]]
        new_board = [[0, -1, 0], [0, -1, 0], [-1, 0, 0]]
        is_valid, actions = self.ttt.try_update_board(new_board)
        print(is_valid, actions)
        self.assertFalse(is_valid)
        self.assertEqual(set(actions), {(0, 1, -1, -1), (2, 0, -1, -1)})

        # 测试2：落下三个棋子
        self.ttt._board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        new_board = [[-1, 0, -1], [0, -1, 0], [0, 0, 0]]
        is_valid, actions = self.ttt.try_update_board(new_board)
        print(is_valid, actions)
        self.assertFalse(is_valid)
        self.assertEqual(set(actions), {(0, 0, -1, -1), (0, 2, -1, -1), (1, 1, -1, -1)})

    def test_replace_pieces(self):
        """测试替换棋子"""
        # 测试1：替换一个棋子
        self.ttt._board = [[0, 0, 0], [0, -1, 0], [0, 0, 1]]
        new_board = [[0, 0, 0], [0, -1, 0], [0, 0, -1]]
        is_valid, actions = self.ttt.try_update_board(new_board)
        print(is_valid, actions)
        self.assertFalse(is_valid)
        self.assertEqual(actions, [(2, 2, -1, -1), (-1, 1, 2, 2)])

        # 测试2：替换多个棋子
        self.ttt._board = [[1, 0, -1], [0, -1, 0], [1, 0, 0]]
        new_board = [[-1, 0, 1], [0, -1, 0], [-1, 0, 0]]
        is_valid, actions = self.ttt.try_update_board(new_board)
        print(is_valid, actions)
        self.assertFalse(is_valid)
        self.assertEqual(
            set(actions),
            {
                (0, 0, -1, -1),
                (0, 2, -1, 1),
                (2, 0, -1, -1),
                (-1, 1, 0, 0),
                (-1, -1, 0, 2),
                (-1, 1, 2, 0),
            },
        )

    def test_remove_pieces(self):
        """测试移除棋子"""
        # 测试1：移除一个棋子
        self.ttt._board = [[0, 0, 0], [0, -1, 0], [0, 0, 1]]
        new_board = [[0, 0, 0], [0, -1, 0], [0, 0, 0]]
        is_valid, actions = self.ttt.try_update_board(new_board)
        print(is_valid, actions)
        self.assertFalse(is_valid)
        self.assertEqual(actions, [(-1, 1, 2, 2)])

        # 测试2：移除多个棋子
        self.ttt._board = [[1, 0, -1], [0, -1, 0], [1, 0, 0]]
        new_board = [[0, 0, 0], [0, -1, 0], [0, 0, 0]]
        is_valid, actions = self.ttt.try_update_board(new_board)
        print(is_valid, actions)
        self.assertFalse(is_valid)
        self.assertEqual(set(actions), {(-1, 1, 0, 0), (-1, -1, 0, 2), (-1, 1, 2, 0)})

    def test_illegal_moves(self):
        """测试非法落子"""
        # 测试1：电脑落子（非法情况）
        self.ttt._board = [[0, 0, 0], [0, -1, 0], [0, 0, 0]]
        new_board = [[1, 0, 0], [0, -1, 0], [0, 0, 0]]
        is_valid, actions = self.ttt.try_update_board(new_board)
        print(is_valid, actions)
        self.assertFalse(is_valid)
        self.assertEqual(actions, [(0, 0, -1, 1)])

        # 测试2：在已有棋子的位置上落子
        self.ttt._board = [[1, 0, 0], [0, -1, 0], [0, 0, 0]]
        new_board = [[-1, 0, 0], [0, -1, 0], [0, 0, 0]]
        is_valid, actions = self.ttt.try_update_board(new_board)
        print(is_valid, actions)
        self.assertFalse(is_valid)
        self.assertEqual(actions, [(0, 0, -1, -1), (-1, 1, 0, 0)])

    def test_swap_pieces(self):
        """测试交换棋子位置"""
        # 测试1：交换两个棋子的位置
        self.ttt._board = [[0, -1, 0], [0, 0, 0], [1, 0, 0]]
        new_board = [[0, 1, 0], [0, 0, 0], [-1, 0, 0]]
        is_valid, actions = self.ttt.try_update_board(new_board)
        print(is_valid, actions)
        self.assertFalse(is_valid)
        self.assertEqual(
            set(actions), {(0, 1, -1, 1), (2, 0, -1, -1), (-1, -1, 0, 1), (-1, 1, 2, 0)}
        )

        # 测试2：交换多个棋子的位置
        self.ttt._board = [[1, -1, 0], [0, 0, 0], [-1, 0, 1]]
        new_board = [[-1, 1, 0], [0, 0, 0], [1, 0, -1]]
        is_valid, actions = self.ttt.try_update_board(new_board)
        print(is_valid, actions)
        self.assertFalse(is_valid)
        self.assertEqual(
            set(actions),
            {
                (0, 0, -1, -1),
                (0, 1, -1, 1),
                (2, 0, -1, 1),
                (2, 2, -1, -1),
                (-1, 1, 0, 0),
                (-1, -1, 0, 1),
                (-1, -1, 2, 0),
                (-1, 1, 2, 2),
            },
        )

    def test_no_moves(self):
        # 空棋盘不落子
        self.ttt.reset_board()
        new_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        is_valid, actions = self.ttt.try_update_board(new_board)
        print(is_valid, actions)
        self.assertFalse(is_valid)
        self.assertEqual(actions, [])

        # 第二手不落子 0
        x = randint(0, 2)
        y = randint(0, 2)
        player = 1 if randint(0, 1) == 0 else -1
        self.ttt.reset_board()
        self.ttt._board[x][y] = player
        new_board = self.ttt._board[:]
        is_valid, actions = self.ttt.try_update_board(new_board)
        print(is_valid, actions)
        self.assertFalse(is_valid)
        self.assertEqual(actions, [])

        # 后期不落子
        self.ttt._board = [[1, -1, 0], [0, 0, 0], [-1, 0, 1]]
        new_board = [[1, -1, 0], [0, 0, 0], [-1, 0, 1]]
        is_valid, actions = self.ttt.try_update_board(new_board)
        print(is_valid, actions)
        self.assertFalse(is_valid)
        self.assertEqual(actions, [])

        # 无效的棋盘不落子
        self.ttt._board = [[1, -1, 1], [-1, 1, -1], [1, -1, 1]]
        new_board = [[1, -1, 1], [-1, 1, -1], [1, -1, 1]]
        is_valid, actions = self.ttt.try_update_board(new_board)
        print(is_valid, actions)
        self.assertFalse(is_valid)
        self.assertEqual(actions, [])


if __name__ == "__main__":
    unittest.main()
