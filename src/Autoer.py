import linecache
import shutil
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
                else:
                    check.run_check(False)
                if "-spigot-build" in sys.argv:
                    result = False
                    version = str(sys.argv[sys.argv.index('-spigot-build')+1])
                    make.download("https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar", "Spigot-BuildTools.jar")
                    if not check.minecraft_to_support_list(version):
                        print("あなたのJavaのバージョンは、インストールする'Minecraft'のバージョンに対応していません。")
                        sys.exit(6)
                    control.exec_java("./", "Spigot-BuildTools.jar", "1", "1", java_argument="-rev "+version)
                    remove_files = ["Spigot", "CraftBukkit", "work", "Bukkit", "BuildData", "apache-maven-3.6.0"]
                    for remove_file in remove_files:
                        shutil.rmtree("./"+remove_file)
                    if os.path.isfile("./BuildTools.log.txt"):
                        file_readlines = open("/BuildTools.log.txt", 'r').readlines()
                        for i in file_readlines[-5:]:
                            if "success" in i.lower():
                                result = True
                            break
                    os.remove("BuildTools.log.txt")
                    print("作成したJarファイルは、spigot-"+version+".jar です\n※注意: ただし、サーバーを今すぐ起動できるまでは準備されていません\n")
                    if result:
                        print("\n正常に完了しました。！\n")
                    else:
                        print("正常に完了できませんでした。\nもう一度実行することをおすすめします。\n終了する場合はctrl+c")
                        input()
                if sys.argv[1] == "-make":
                    if sys.argv[2] == "-file":
                        if not os.path.isfile(sys.argv[3]):
                            print("そのファイルは存在しません")
                            sys.exit(4)
                        lines = open(sys.argv[3], encoding="utf-8", mode="r").readlines()
                        for i in range(len(lines)):
                            installer_jar = ""
                            spigot_jar = ""
                            argv = lines[i].split(' ')
                            if "-spigot" in argv:
                                local_jar_mode = 1
                                spigot_jar = argv[1]
                            elif "-mod" in argv:
                                local_jar_mode = 2
                                installer_jar = argv[1]
                            else:
                                local_jar_mode = 0
                            result = make.make_server(argv[0], argv[1], argv[2], local_jar_mode, spigot_jar, installer_jar, bool(strtobool(argv[3].capitalize().replace('\n', ''))))
                            print(str(i)+"番目のサーバー名は |||↓\n"+result[0])
                    else:
                        installer_jar = ""
                        spigot_jar = ""
                        if "-spigot" in sys.argv:
                            local_jar_mode = 1
                            spigot_jar = sys.argv[3]
                        elif "-mod" in sys.argv:
                            local_jar_mode = 2
                            installer_jar = sys.argv[3]
                        else:
                            local_jar_mode = 0
                        result = make.make_server(sys.argv[2], sys.argv[3], sys.argv[4], local_jar_mode, spigot_jar, installer_jar, bool(strtobool(sys.argv[5].capitalize())))
                        print("作成したサーバー名は |||↓\n"+result[0])
                    if result[1]:
                        print("作成が正常に完了しました")
                    else:
                        print("作成が正常に完了しませんでした\nもう一度作成する必要があります。")
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
                    if not os.path.exists(path+"/"+start_jar):
                        if os.path.exists(path+"/"+start_jar.replace(".jar", "")+"-universal.jar"):
                            start_jar = start_jar.replace(".jar", "")+"-universal.jar"
                        else:
                            print("起動できません。\nJarファイルが存在しません。")
                            sys.exit(6)
                    control.exec_java(path, start_jar, sys.argv[3], sys.argv[4], java_argument=java_argv)
                    sys.exit(0)
                else:
                    pass
            except Exception as e:
                check.except_print(e, "", True)
        if ischeck:
            check.run_check()
        self.version = 1.4
        self.editon = "release"
        if not self.is_version_new_autoer(str(self.version)):
            print("I:すでにこのバージョンよりも新しい、バージョンが出ています。\n詳しくは: https://github.com/stsaria/Autoer-1/releases\n")
    def run_autoer(self):
        if "pre" in self.editon:
            print("*このプログラムは、リリース前最終確認版です*")
        """Autoerを実行する"""
        print("\nAutoer-1\nVersion: "+str(self.version)+"-"+self.editon)
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
