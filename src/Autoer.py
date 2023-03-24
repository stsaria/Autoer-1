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

        if len(sys.argv) >= 5:
            try:
                make.make_server(sys.argv[1], sys.argv[2], sys.argv[3], int(0), "", "", bool(sys.argv[4]))
                print("Make Success")
                sys.exit(0)
            except Exception as e:
                check.except_print(e, "", True)
        self.version = 1.1
        self.editon = "pre-release"
    
    def run_autoer(self):
        if self.editon == "pre-release":
            print("*このプログラムは、リリース前最終確認版です*")
        """Autoerを実行する"""
        print("Autoer-1\nVersion: "+str(self.version)+"-"+self.editon)
        while True:
            mode = input("モードを選択してください\n作成モード[Make]\n管理モード[Control]\nソフトウェアを終了[Exit]\n[M,C,E]: ").lower()
            if mode in ["make", "mak", "ma", "m"]:
                make.wizard_make_server()
            elif mode in ["control", "contro", "contr", "cont", "con", "co", "c"]:
                control.control_server()
            elif mode in ["exit", "exi", "ex", "e"]:
                sys.exit(0)

if __name__ == "__main__":
    autoer = Autoer()
    autoer.run_autoer()
