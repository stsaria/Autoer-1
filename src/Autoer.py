import linecache
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
        if 5 <= len(sys.argv) <= 6:
            try:
                if sys.argv[1] == "-make":
                    make.make_server(sys.argv[2], sys.argv[3], sys.argv[4], int(0), "", "", bool(sys.argv[5]))
                    print("Make Success")
                elif sys.argv[1] == "-run":
                    java_argv = "nogui"
                    # Minecraft Server select code
                    if sys.argv[2].isdigit():
                        path = linecache.getline('data/minecraft-dir-list.txt', int(sys.argv[2])).replace('\n', '')
                    else:
                        f = open('data/minecraft-dir-list.txt')
                        minecraft_dir_list =  f.readlines()
                        minecraft_dir_list_strip = [line.strip() for line in minecraft_dir_list]
                        path = [line for line in minecraft_dir_list_strip if sys.argv[2] in line][0]
                    # xmx,xms check
                    if not sys.argv[3].isdigit() or not sys.argv[4].isdigit():
                        print("メモリの指定方法が想定外です。")
                        sys.exit(5)
                    if len(sys.argv) == 6:
                        java_argv = sys.argv[5]
                    start_jar = linecache.getline("data/"+path.replace('/', '-')+".txt", 2).replace('\n', '')
                    control.exec_java(path, start_jar, sys.argv[3], sys.argv[4], java_argument=java_argv)
                sys.exit(0)
            except Exception as e:
                check.except_print(e, "", True)
        self.version = 1.2
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
