import subprocess
import linecache
import sys
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
        if int(minecraft_server_dir_list_txt_lines_count) < int(choice_lines) - 1:
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

def make_sh():
    """shとbatファイルを生成する関数"""
    print("Please select the server where you want to create the sh-bat file.")
    with open("data/minecraft-list.txt", "r", encoding="utf-8") as file:
        lines = file.read()
    print(lines)
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
                        "ネットワークの情報確認モード[IP]\n",
                        "最大参加人数の変更モード,[max-player]\n",
                        "戻る | Exit (exit)\n[R,P,S,B,N,M,E]: ", end="")
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
        elif choice in["exit", "exi", "ex", "e"]:
            break
        else:
            print("その項目はありません。")
