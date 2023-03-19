from urllib.request import Request, urlopen
import linecache
import datetime
import urllib
import shutil
import socket
import json
import re
import os

import Server.control as control
import Etc.check as check
import Etc.etc as etc

def get_minecraft_version(version):
    file = open('data/version.json', 'r')
    json_object = json.load(file)
    minecraft_editions = ["stable", "snapshot"]
    successs = []
    for minecraft_edition in minecraft_editions:
        try:
            minecraft_server_url = json_object[minecraft_edition][version]["server"]
            successs.append(True)
        except KeyError:
            successs.append(False)
            continue
    if not successs[0] and not successs[1]:
        return False, "not"
    return True, minecraft_server_url

def download(url, save_name):
    urllib.request.urlretrieve(url, save_name)

def download_text(url, file_name):
    # そのままだとurllib.error.HTTPError: HTTP Error 403: Forbiddenでコケるからユーザーエージェントを偽装
    headers = {'User-Agent': 'Mozilla/5.0'}
    request = Request(url, headers=headers)
    html = urlopen(request).read()
    html = html.decode('utf-8')
    # ファイル書き込み(server.properties)
    file = open(file_name, mode='w')
    file.write(str(html))
    file.close()

# 特定の文字列の行を書き換える関数
def replace_func(fname, replace_set):
    target, replace = replace_set
    
    with open(fname, 'r') as f1:
        tmp_list =[]
        for row in f1:
            if row.find(target) != -1:
                tmp_list.append(replace)
            else:
                tmp_list.append(row)

    with open(fname, 'w') as f2:
        for i in range(len(tmp_list)):
            f2.write(tmp_list[i])

# ↑を呼び出す関数
def file_identification_rewriting(file_name, before, after):
    replace_setA = (before, after) # (検索する文字列, 置換後の文字列)
    # call func
    replace_func(file_name, replace_setA)

# サーバー情報入力関数 
def input_server_info():
    while True:
        server_name = input("新規サーバー名を入力してください: ")
        if server_name == "":
            continue
        break
    while True:
        server_port = input("設定したいポートを入力してください: ")
        if not server_port.isdigit():
            print("数字ではありません。")
            continue
        if int(server_port) < 1 or int(server_port) > 100000:
            print("予想外のポートです。")
            continue
        # 入力したポートが使用されているかのチェック
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if sock.connect_ex(("127.0.0.1",int(server_port))) == 0:
            print("注意：このポートは既に使用されています。",
                    "\nそのまま使用すると、不都合が生じる可能性があります。",
                    "\nこのポートでよろしいですか？\nはい[yes]\nいいえ[no] [Y/n]: ", end="")
            choice = etc.input_yes_no("")
            if not choice:
                continue
        break
    while True:
        choice = input("もしあなたがマインクラフトサーバーでModやプラグイン \n(Mod: forge | プラグイン: spigotmc,papermc) を使いたい場合は`yes`を入力てください。 \nそうでない場合 (公式のサーバーをダウンロードする) は `no`を選択してください。\n※ただし、自分のJarファイルを使うモードでのトラブルに関しては答えることはできません。※\n[Y,N]: ").lower()
        if choice in ["yes", "ye", "y"]:
            version = None
            while True:
                choice = input("Forgeを利用する場合は 'yes'を入力してください。\nSpigotmcやPapermcなどを利用する場合は `no`.\n[Y,N]: ").lower()
                if choice in ["yes", "ye", "y"]:
                    local_jar_mode = 2
                    while True:
                        jar_start_file = None
                        jar_installer_file = input("Forgeのファイル名を入力してください。 (e.g. C:/Users/user/Download/forge-installer.jar): ")
                        try:
                            if not os.path.isfile(jar_installer_file):
                                print("ファイルがありません。")
                                continue
                            if not jar_installer_file.endswith(".jar"):
                                print("そのファイルはJarファイルではありません。")
                                continue
                        except Exception as e:
                            check.except_print(e, "", False)
                            continue
                        break
                
                elif choice in ["no", "n"]:
                    local_jar_mode = 1
                    while True:
                        jar_installer_file = None
                        jar_start_file = input("自分が持っているJarファイル名を入力してください。 (e.g. C:/Users/user/Download/spigotmc.jar): ")
                        try:
                            if not os.path.isfile(jar_start_file):
                                print("ファイルがありません。")
                                continue
                            if not jar_start_file.endswith(".jar"):
                                print("そのファイルはJarファイルではありません。")
                                continue
                        except Exception as e:
                            check.except_print(e, "", False)
                            continue
                        break
                break
            break
        
        elif choice in ["no", "n"]:
            jar_installer_file = None
            jar_start_file = None
            local_jar_mode = 0
            while True:
                version = input("サーバーのバージョンを入力してください: ")
                if not get_minecraft_version(version)[0]:
                    continue
                if not check.minecraft_to_support_list(version):
                    if not etc.input_yes_no("いま、あなたが入力したバージョンに合うJavaが見つかりません。\nそのまま続行すると、不都合が生じる可能性があります。\n続行しますか？\nはい[yes]\nいいえ[no] [Y/n]: "):
                        continue
                break
            break
    while True:
        choice = input("\nもし、もう一つ作成したい場合には `plural` と入力してください。\n今すぐ作成する場合には `add` と入力してください。 \n[P,A]: ")
        if choice in ["add", "ad", "a"]:
            return True, server_name, version, server_port, local_jar_mode, jar_installer_file, jar_start_file
        elif choice in ["plural", "plura", "plur", "plu", "pl", "p"]:
            return False, server_name, version, server_port, local_jar_mode, jar_installer_file, jar_start_file

def make_server():
    print("Make Mode")
    server_count = 1
    while True:
        print(str(server_count)+"回目")
        server_add, server_name, server_version, server_port, local_jar_mode, jar_installer_file, jar_start_file = input_server_info()
        if not os.path.exists("tmp"):
            os.mkdir("tmp")
        with open("tmp/"+str(server_count)+".tmp", 'w', encoding="utf-8") as f:
            print(server_name+"\n"+str(server_version)+"\n"+server_port+"\n"+str(local_jar_mode)+"\n"+str(jar_start_file)+"\n"+str(jar_installer_file), file=f)
        if server_add:
            break
        server_count = server_count + 1
    eula = etc.input_yes_no("\nEULA/ソフトウェア利用許諾契約に同意しますか？ \nマインクラフトのEulaに関しては\nhttps://www.minecraft.net/ja-jp/eula\nをご覧ください\n 同意する場合は `yes` , 同意しない場合は `no` と入力してください。\n[Y/n]: ")
    
    for i in range(server_count):
        i = i + 1
        print("作成中 ("+str(i)+"回目)")
        
        dt_now = datetime.datetime.now(datetime.timezone.utc)
        dt_now_utc = datetime.datetime.now(datetime.timezone.utc)
        minecraft_dir = "minecraft/minecraft-"+dt_now.strftime('%Y-%m-%d-%H-%M-%S-%f')
        os.mkdir(minecraft_dir)
        
        server_name = linecache.getline("tmp/"+str(i)+".tmp", 1).replace('\n', '')
        server_version = linecache.getline("tmp/"+str(i)+".tmp", 2).replace('\n', '')
        server_port = linecache.getline("tmp/"+str(i)+".tmp", 3).replace('\n', '')
        local_jar_mode = int(linecache.getline("tmp/"+str(i)+".tmp", 4))
        jar_local_file = linecache.getline("tmp/"+str(i)+".tmp", 5).replace('\n', '')
        jar_installer_file = linecache.getline("tmp/"+str(i)+".tmp", 6).replace('\n', '')
        
        if not local_jar_mode == 0:
            
            if local_jar_mode == 1:
                server_version = os.path.splitext(os.path.basename(jar_local_file))[0]
                shutil.copy(jar_local_file, minecraft_dir)
                jar_start_file = "server.jar"
            
            if local_jar_mode == 2:
                shutil.copy(jar_installer_file, minecraft_dir)
                jar_installer_file = os.path.basename(jar_installer_file)
                jar_start_file = jar_installer_file.replace('-installer', '')
                server_version = os.path.splitext(os.path.basename(jar_start_file))[0]
                control.exec_java(minecraft_dir, jar_installer_file, "1", "1", "--installServer")
        else:
            try:
                print("Version "+server_version+" をダウンロードしています。")
                # マイクラjarファイルダウンロード
                download(get_minecraft_version(server_version)[1], minecraft_dir+"/server.jar")
                jar_start_file = "server.jar"
            # ダウンロード時の例外処理
            except Exception as e:
                check.except_print(e, "", True)
        
        
        # eula.txt create&write
        f = open(minecraft_dir+"/eula.txt", 'w')
        f.write("#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).\n#"+dt_now_utc.strftime('%a')+" "+dt_now_utc.strftime('%b')+" "+dt_now_utc.strftime('%d')+" "+dt_now_utc.strftime('%H:%M:%S')+" "+str(dt_now_utc.tzinfo)+" "+dt_now_utc.strftime('%Y')+"\neula="+str(eula))
        f.close()
        
        # server properties donwload
        download_text("https://server.properties/", minecraft_dir+"/server.properties")
        # server properties edit port
        file_identification_rewriting(minecraft_dir+"/server.properties", "server-port=", "server-port="+server_port+"\n")
        # server properties edit motd(server name)
        file_identification_rewriting(minecraft_dir+"/server.properties", "motd=", "motd="+server_name+"\n")
        
        server_list_lines_count = sum([1 for _ in open('data/minecraft-list.txt', encoding="utf-8")])
        with open('data/minecraft-list.txt', 'a', encoding="utf-8") as f:
            print("["+str(server_list_lines_count + 1)+"] Server name: "+server_name+" | Creation time: "+dt_now.strftime('%Y/%m/%d %H:%M:%S')[:-3]+" | Server Version: "+server_version+" | Minecraft Server Directory: "+minecraft_dir+"/", file=f)
        with open('data/minecraft-dir-list.txt', 'a', encoding="utf-8") as f:
            print(minecraft_dir, file=f)
        
        # サーバーディレクトリに管理用txtファイルを作成
        with open("data/"+minecraft_dir.replace('/', '-')+".txt", 'w', encoding="UTF-8") as f:
            print(server_version+"\n"+jar_start_file, file=f)

    # Remove directory temp
    shutil.rmtree("tmp")
    print("\nサーバーの作成が完了しました！\n")