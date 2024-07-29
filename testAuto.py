import unittest
from TicTacToe import TicTacToe
from random import randint

class TestAutoMove(unittest.TestCase):
	def test_auto_move(self):
		"""
		测试 auto_move 方法
		1. 创建两个 TicTacToe 实例
		2. 让它们交替执行 auto_move
		3. 对另一个执行 manual_move 进行同步
		4. 打印棋盘并断言为平局
		5. 运行 100 次,结果输出到 log 文件
		"""
		with open("test_log.txt", "w", encoding="utf-8") as log_file:
			for game_num in range(10000):
				# 创建两个 TicTacToe 实例
				ttt1 = TicTacToe()
				ttt2 = TicTacToe()

				# 初始化当前玩家
				current_player = 1  # 1 表示 ttt1, -1 表示 ttt2
				first_step = True

				# 游戏循环
				while True:
					if current_player == 1:
						# ttt1 执行自动下棋
						move = ttt1.auto_move()
					else:
						# ttt2 执行自动下棋
						if first_step:
							while True:
								move = (randint(0, 2), randint(0, 2))
								if ttt2._board[move[0]][move[1]] != 0:
									continue
								first_step = False
								ttt2.force_move(move[0], move[1], TicTacToe.computer)
								break
						else:
							move = ttt2.auto_move()

					if move:
						print(f"游戏 {game_num + 1}: 玩家 {current_player} 移动到 {move}", file=log_file)
						row, col = move
						# 在当前玩家的棋盘上落子
						if current_player == 1:
							ttt2.manual_move(row, col)
						else:
							ttt1.manual_move(row, col)
					else:
						print(f"游戏 {game_num + 1}: 无法进行有效移动", file=log_file)
						break

					# 检查是否有胜者或平局
					winner1 = ttt1.check_winner()
					winner2 = ttt2.check_winner()
					if winner1 != 0 or winner2 != 0 or ttt1.is_board_full():
						# 打印棋盘
						print(f"游戏 {game_num + 1} 结果:", file=log_file)
						ttt1.print_board(file=log_file)
						ttt2.print_board(file=log_file)

						# 断言两个棋盘状态相反
						board1 = ttt1.get_board()
						board2 = ttt2.get_board()

						log_file.flush()

						for i in range(3):
							for j in range(3):
								self.assertEqual(board1[i][j], -board2[i][j])

						# 断言必须为平局
						self.assertTrue(ttt1.is_board_full() or winner1 == 1)

					# 切换玩家
					current_player = -current_player

if __name__ == '__main__':
	unittest.main()