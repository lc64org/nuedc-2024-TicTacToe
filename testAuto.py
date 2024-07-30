import threading
import unittest
from datetime import datetime
from random import randint

from TicTacToe import TicTacToe

# 全局变量,用于生成唯一的线程编号
thread_counter = 0
thread_counter_lock = threading.Lock()

def get_thread_number():
    global thread_counter
    with thread_counter_lock:
        thread_counter += 1
        return thread_counter

class TestAutoMove(unittest.TestCase):
    def __init__(self, methodName='runTest', thread_number=None):
        super().__init__(methodName)
        self.thread_number = thread_number

    def test_auto_move(self):
        """
        测试 auto_move 方法
        1. 创建两个 TicTacToe 实例
        2. 让它们交替执行 auto_move
        3. 对另一个执行 manual_move 进行同步
        4. 打印棋盘并断言为平局
        5. 运行 100 次,结果输出到 log 文件
        """
        filename = f"auto_test_{self.thread_number}_{str(datetime.now())[:19]}.log".replace(" ", "_").replace(":", "-")
        with open(
            filename,
            "w",
            encoding="utf-8",
        ) as log_file:
            for game_num in range(100000):
                # 创建 TicTacToe 实例
                ttt = TicTacToe()

                # 初始化当前玩家
                current_player = 1
                is_auto = False

                # 游戏循环
                while True:
                    if current_player == 1:
                        # 执行自动下棋
                        move = ttt.auto_move()
                        is_auto = True
                    else:
                        # 执行自动或随机下棋
                        if randint(0, 2) == 0: # 1/3 的概率自动下棋
                            # 自动下棋
                            move = ttt.find_best_move(ttt.human)
                            # 如果找到合适的空位
                            if move:
                                row, col = move
                                # 在该位置落电脑的子（值为1）
                                ttt._board[row][col] = ttt.human
                                is_auto = True
                        else:
                            # 随机下棋
                            while True:
                                if ttt.is_board_full():
                                    move = None
                                    break
                                move = (randint(0, 2), randint(0, 2))
                                if ttt._board[move[0]][move[1]] != 0:
                                    continue
                                ttt.force_move(move[0], move[1], TicTacToe.human)
                                is_auto = False
                                break
                    if move:
                        print(
                            f"游戏 {game_num + 1}: 玩家 {current_player} {"自动" if is_auto else "随机"} 移动到 {move}",
                            file=log_file,
                        )
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


def run_tests_in_thread(thread_number):
    suite = unittest.TestSuite()
    suite.addTest(TestAutoMove('test_auto_move', thread_number=thread_number))
    unittest.TextTestRunner().run(suite)

if __name__ == "__main__":
    threads = []
    for _ in range(10):
        thread_number = get_thread_number()
        t = threading.Thread(target=run_tests_in_thread, args=(thread_number,))
        threads.append(t)
        t.start()

    # 等待所有线程完成
    for t in threads:
        t.join()
