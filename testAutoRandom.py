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
			for game_num in range(500000):
				# 创建 TicTacToe 实例
				ttt = TicTacToe()

				# 初始化当前玩家
				current_player = 1

				# 游戏循环
				while True:
					if current_player == 1:
						# 执行自动下棋
						move = ttt.auto_move()
					else:
						# 执行随机下棋
						while True:
							if ttt.is_board_full():
								move = None
								break
							move = (randint(0, 2), randint(0, 2))
							if ttt._board[move[0]][move[1]] != 0:
								continue
							ttt.force_move(move[0], move[1], TicTacToe.human)
							break

					if move:
						print(f"游戏 {game_num + 1}: 玩家 {current_player} 移动到 {move}", file=log_file)
					else:
						print(f"游戏 {game_num + 1}: 无法进行有效移动", file=log_file)
						break

					# 检查是否有胜者或平局
					winner = ttt.check_winner()
					if winner != 0 or ttt.is_board_full():
						# 打印棋盘
						print(f"游戏 {game_num + 1} 结果：%s" % winner, file=log_file)
						ttt.print_board(file=log_file)

						log_file.flush()

						# 断言必须为平局
						self.assertTrue(ttt.is_board_full() or winner == 1)

						current_player = -current_player
						break

					# 切换玩家
					current_player = -current_player

if __name__ == '__main__':
	unittest.main()