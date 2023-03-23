import sys

"""自作プログラムの読み込み"""
from Etc import check
from Server import make
from Server import control

# Sorry, this code isn't pretty.
# this code -> ptrsie#0952
# email -> solothunder.autoer@gmail.com

class Autoer:
    """実行メインクラス"""
    def __init__(self) -> None:
        """起動に必要な準備"""
        check.run_check()
        self.version = 1.0
        self.editon = "release"
    
    def run_autoer(self):
        if self.editon == "pre-release":
            print("*このプログラムは、リリース前最終確認版です*")
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
