import subprocess
import linecache
import platform
import shutil
import time
import sys
import os
from Server import make
from Etc import etc
from Etc import check

def exec_java(dir_name, jar_name, xms, xmx, java_argument):
    """javaを実行するための関数"""
    # もし入力内容が0かnotだったら1(1GB)に
    cmd = "java -Xmx"+xmx+"G -Xms"+xms+"G -jar ./"+jar_name+" "+java_argument
    subprocess.call(cmd, shell=True, cwd=r""+dir_name+"/")

def select_server():
    """サーバーを選択する関数"""
    minecraft_server_list_txt_lines_count = sum(
        [1 for _ in open('data/minecraft-list.txt', encoding="utf-8")])
    minecraft_server_dir_list_txt_lines_count = sum(
        [1 for _ in open('data/minecraft-dir-list.txt', encoding="utf-8")])
    if not minecraft_server_dir_list_txt_lines_count == minecraft_server_list_txt_lines_count:
        print("txtファイルの行数が合わないため、続行できません。")
        sys.exit(1)
    while True:
        with open("data/minecraft-list.txt", "r", encoding="utf-8") as file:
            lines = file.read()
        print(lines)
        choice_lines = input("サーバーの番号を入力してください: ")
        if not choice_lines or not choice_lines.isdigit():
            continue
        if int(minecraft_server_dir_list_txt_lines_count) < int(choice_lines):
            continue
        break
    return choice_lines

def start_server():
    """サーバーを実行するための `準備` 関数"""
    print("サーバー起動モード")
    print("起動するサーバーを選んでください\n")
    choice_server = select_server()
    while True:
        choice_xms = input("Xms(サーバー最小割当メモリ)を入力してください(G) ※数字のみ: ")
        choice_xmx = input("Xmx(サーバー最大割当メモリ)を入力してください(G) ※数字のみ: ")
        mem_input = [str(choice_xms), str(choice_xmx)]
        for i in mem_input:
            if not i.isdigit():
                continue
            if int(i) < 1:
                continue
        break
    path = linecache.getline('data/minecraft-dir-list.txt', int(choice_server)).replace('\n', '')
    start_jar = linecache.getline("data/"+path.replace('/', '-')+".txt", 2).replace('\n', '')

    exec_java(path, start_jar, mem_input[0], mem_input[1], "nogui")

def change_port():
    """サーバーのポートを再設定する関数"""
    print("サーバーポート変更モード")
    print("ポートを変更する、サーバーを選択してください。")
    choice_server = select_server()
    path = linecache.getline('data/minecraft-dir-list.txt', int(choice_server)).replace('\n', '')
    while True:
        input_port = input("再設定するポートを入力してください: ")
        if not input_port or not str.isnumeric(input_port):
            continue
        else:
            break
    make.file_identification_rewriting(path+"/server.properties",
                                        "server-port=", "server-port="+input_port+"\n")
    print("サーバーのポートを変更しました。")

def change_max_player():
    """最大参加人数を変更する関数"""
    print("サーバー最大参加人数の変更モード")
    print("最大参加人数を変更したいサーバーを選択してください。")
    choice_server = select_server()
    path = linecache.getline('data/minecraft-dir-list.txt', int(choice_server)).replace('\n', '')
    while True:
        input_max_player = input("再設定する最大参加人数を入力してください: ")
        if not input_max_player.isdigit():
            continue
        break
    
    make.file_identification_rewriting(path+"/server.properties", "max-players=", "max-players="+input_max_player+"\n")
    print("サーバーの最大参加人数を変更しました。")

def add_startup():
    """スタートアップ(LinuxではSystemdなど)にMinecraftを実行するbat-shファイルを登録する関数"""
    print("OS起動時 自動起動 設定モード")
    check.is_admin()
    print("設定したいサーバーを選択してください。")
    user_use_platfrom = platform.system()
    choice_server = select_server()
    path = linecache.getline('data/minecraft-dir-list.txt', int(choice_server)).replace('\n', '')
    start_jar = linecache.getline("data/"+path.replace('/', '-')+".txt", 2).replace('\n', '')
    absolute_path = os.path.abspath(path)
    while True:
        choice_xms = input("Xms(サーバー最小割当メモリ)を入力してください(G) ※数字のみ: ")
        choice_xmx = input("Xmx(サーバー最大割当メモリ)を入力してください(G) ※数字のみ: ")
        mem_input = [str(choice_xms), str(choice_xmx)]
        for i in mem_input:
            if not i.isdigit():
                continue
            if int(i) < 1:
                continue
        break
    if user_use_platfrom == "Windows":
        try:
            file = open("C:/ProgramData/Microsoft/Windows/Start Menu/Programs/StartUp/minecraft-"+path.replace('/', '').replace('minecraft', '')+".bat", mode='w')
            file.write("java -Xms{xms}G -Xmx{xmx}G -jar {abspath}/{jar_file} nogui \n\
                        pause".format(xms = choice_xms, xmx = choice_xmx, abspath = absolute_path, jar_file = start_jar))
            file.close()
        except Exception as excep:
            check.except_print(excep, "", True)
    else:
        if not shutil.which('systemctl'):
            print("コマンド:Systemctlが見つかりません")
            sys.exit(4)
        try:
            file = open("/etc/systemd/system/minecraft"+path.replace('/', '').replace('minecraft', '')+".service", mode='w')
            file.write("[Unit] \
            \nDescription=Minecraft Server: %i \
            \nAfter=network.target \
            \n[Service] \
            \nWorkingDirectory={woking_dir} \
            \nRestart=always \
            \nExecStart=/usr/bin/java -Xms{xms}G -Xmx{xmx}G -jar {jar_file} nogui \
            \n[Install] \
            \nWantedBy=multi-user.target".format(woking_dir = absolute_path, xms = choice_xms, xmx = choice_xmx, jar_file = start_jar))
            file.close()
            subprocess.run("sudo systemctl daemon-reload", shell=True)
            time.sleep(0.8)
            subprocess.run("sudo systemctl enable minecraft"+path.replace('/', '').replace('minecraft', ''), shell=True)
        except Exception as excep:
            check.except_print(excep, "", True)
    print("完了しました！")

def make_sh():
    """shとbatファイルを生成する関数"""
    choice_lines = select_server()
    path = linecache.getline('data/minecraft-dir-list.txt', int(choice_lines)).replace('\n', '')
    while True:
        choice_xms = input("Xms(サーバー最小割当メモリ)を入力してください(G) ※数字のみ: ")
        choice_xmx = input("Xmx(サーバー最大割当メモリ)を入力してください(G) ※数字のみ: ")
        mem_input = [str(choice_xms), str(choice_xmx)]
        for i in mem_input:
            if not i.isdigit():
                continue
            if int(i) < 1:
                continue
        break
    start_jar = linecache.getline("data/"+path.replace('/', '-')+".txt", 2).replace('\n', '')
    file_name = ["start.sh", "start.bat"]
    for i in file_name:
        with open(path+"/"+i, 'w', encoding="utf-8") as file:
            print("echo Start!\n",
                    "java -Xms"+mem_input[0]+"G",
                    " -Xmx"+mem_input[1]+"G",
                    " -jar "+start_jar+" --nogui", file=file,  sep='')
    print("sh-batファイルを作成しました。")

def network_info():
    """ネットワークのIPなどを確認できる関数"""
    print("\n注意: IPを公開するのは、危険度が高いです。\n",
            "IPアドレスは重要な情報です。(電話番号のようなものです。) \n",
            "もし、あなたが配信やIPアドレスを見せたくない状況の場合には表示しないことをおすすめします。",
            "\n`yes` か `no`を選択してください。\n[Y/N]: ")
    network_info_select = etc.input_yes_no("")
    if not network_info_select:
        return False
    active, global_ip, private_ip = check.network("https://ifconfig.me")
    if not active:
        global_ip = "取得できません。"
    print("プライベートIP (同じネットワークで参加するために必要です。)"+private_ip)
    print("グローバルIP (外のネットワークから参加するために必要です。)"+global_ip)
    input()
def control_server():
    while True:
        print("\nモードを選択してください。\n",
                "サーバー起動モード[run]\n",
                "サーバーポート変更モード[port]\n",
                "shとbatファイル作成[sh],[bat]\n",
                "ネットワークの情報確認モード[network]\n",
                "最大参加人数の変更モード,[max-player]\n",
                "スタートアップ(Windows)、Systemd(*Linux)での自動起動の設定モード[add-startup]\n",
                "戻る | Exit (exit)\n",
                "[R,P,S,B,N,M,A,E]: ", end="")
        choice = input().lower()
        if choice in ["run", "ru", "r"]:
            start_server()
        elif choice in["port", "por", "po", "p"]:
            change_port()
        elif choice in["sh", "s"]:
            make_sh()
        elif choice in["bat", "ba", "b"]:
            make_sh()
        elif choice in["network", "networ", "netwo", "netw", "net", "ne", "n"]:
            network_info()
        elif choice in["max-player", "max-playe", "max-play", "max-pla", "max-pl", "max-p", "max-", "max", "ma", "m"]:
            change_max_player()
        elif choice in["add-startup", "add-startu", "add-start", "add-star", "add-sta", "add-st", "add-s", "add-", "add", "ad", "a"]:
            add_startup()
        elif choice in["exit", "exi", "ex", "e"]:
            break
        else:
            print("その項目はありません。")
