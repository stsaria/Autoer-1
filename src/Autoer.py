import sys
from Etc import check
from Server import make
from Server import control

# Sorry, this code isn't pretty.

class Autoer:
    """実行メインクラス"""
    def __init__(self) -> None:
        """起動に必要な準備"""
        check.run_check()
        self.version = 0.7
        self.editon = "beta"
    
    def run_autoer(self):
        """Autoerを実行する"""
        print("Autoer-1\nVersion: "+str(self.version)+"-"+self.editon)
        while True:
            mode = input("モードを選択してください\n作成モード[Make]\n管理モード[Control]\nソフトウェアを終了[Exit]\n[M,C,E]: ").lower()
            if mode in ["make", "mak", "ma", "m"]:
                make.make_server()
            elif mode in ["control", "contro", "contr", "cont", "con", "co", "c"]:
                control.control_server()
            elif mode in ["exit", "exi", "ex", "e"]:
                sys.exit(0)

if __name__ == "__main__":
    autoer = Autoer()
    autoer.run_autoer()
