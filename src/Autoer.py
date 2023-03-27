import linecache
import json
import sys
import os

"""自作プログラムの読み込み"""
from Etc import check
from Server import make
from Server import control

# Sorry, this code isn't pretty.
# this code -> ptrsie#0952
# email -> solothunder.autoer@gmail.com

def strtobool(str: str):
    if str.lower() in ["true", "tru", "tr", "t"]:
        return 1
    elif str.lower() in ["false", "fals", "fal", "fa", "f"]:
        return 0

class Autoer:
    """実行メインクラス"""
    def is_version_new_autoer(self, use_version):
        """実行されたAutoerのバージョンが一番新しいか確認する関数"""
        version = ""
        make.download_text("https://api.github.com/repos/stsaria/Autoer-1/tags", "data/autoer.json")
        for i in range(open("data/autoer.json").readline().count('name')):
            if json.load(open('data/autoer.json', 'r'))[i]['name'] in ["pre"]:
                continue
            version = json.load(open('data/autoer.json', 'r'))[i]['name'].replace('v', '').replace('.', '').replace('-', '').replace('release', '').replace('beta', '').replace('pre', '').replace('alpha', '')[:2]
            if int(str(use_version).replace('.', '')) < int(version):
                return False
            else:
                return True
    def __init__(self) -> None:
        """起動に必要な準備"""
        ischeck = True
        if 2 <= len(sys.argv):
            try:
                if "-notcheck" in sys.argv:
                    ischeck = False
                if sys.argv[1] == "-make":
                    if sys.argv[2] == "-file":
                        if not os.path.isfile(sys.argv[3]):
                            print("そのファイルは存在しません")
                            sys.exit(4)
                        lines = open(sys.argv[3], encoding="utf-8", mode="r").readlines()
                        for i in range(len(lines)):
                            argv = lines[i].split(' ')
                            print(str(i)+"番目のサーバー名は |||↓\n"+make.make_server(argv[0], argv[1], argv[2], int(0), "", "", bool(strtobool(argv[3].capitalize().replace('\n', '')))))
                    else:
                        print("作成したサーバー名は |||↓\n"+make.make_server(sys.argv[2], sys.argv[3], sys.argv[4], int(0), "", "", bool(strtobool(sys.argv[5].capitalize()))))
                    print("Make Success")
                    sys.exit(0)
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
                    # xmx,xms isnum?
                    if not sys.argv[3].isdigit() or not sys.argv[4].isdigit():
                        print("メモリの指定方法が想定外です。")
                        sys.exit(5)
                    if len(sys.argv) == 6:
                        java_argv = sys.argv[5]
                    start_jar = linecache.getline("data/"+path.replace('/', '-')+".txt", 2).replace('\n', '')
                    control.exec_java(path, start_jar, sys.argv[3], sys.argv[4], java_argument=java_argv)
                    sys.exit(0)
                else:
                    pass
            except Exception as e:
                check.except_print(e, "", True)
        if ischeck:
            check.run_check()
        self.version = 1.3
        self.editon = "release"
        if not self.is_version_new_autoer(str(self.version)):
            print("I:すでにこのバージョンよりも新しい、バージョンが出ています。\nくわしくは: https://github.com/stsaria/Autoer-1/releases\n")
    
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
    try:
        autoer = Autoer()
        autoer.run_autoer()
    except Exception as e:
        check.except_print(e, "", True)
