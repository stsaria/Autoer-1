"""モジュールの読み込み"""
import os
import sys
import shutil
import socket
import requests
# ※ユーザーはrequestsを入れる必要があります（もしくは、同梱されたソフトウェアを使う）

def except_print(except_text, text, stop):
    """例外を表示する関数"""
    print("エラー(例外)が発生しました\n",text)
    while True:
        except_choice = input("\n例外を表示しますか？ \nはい[YES]\nいいえ[No]\n[Y/n]:").lower()
        if except_choice in ["yes", "ye", "y"]:
            print("詳細------\n",except_text)
            break
        if except_choice in ["no", "n"]:
            break
    if stop:
        sys.exit(1)

def network(url):
    """ネットワークのチェック関数（グローバル、プライベート IPも取得可能）"""
    active = False
    global_ip = None
    private_ip = None
    except_content = None
    try:
        temporal_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temporal_socket.connect(("8.8.8.8", 80))
        private_ip = temporal_socket.getsockname()[0]
        temporal_socket.close()
        global_ip = requests.get(url, timeout=(3.0, 7.5)).text
        active = True
    except Exception as excep:
        except_content= excep
    return active, global_ip, private_ip, except_content

def run_check() -> None:
    """チェックを実行する関数（起動時など）"""
    print("File", end="...")
    paths = ["data", "data/minecraft-list.txt", "data/minecraft-dir-list.txt", "minecraft"]
    attributes = ["dir", "file", "file", "dir"]
    for index in range(len(paths)):
        if not os.path.exists(paths[index]):
            if attributes[index] == "dir":
                os.mkdir(paths[index])
            if attributes[index] == "file":
                try:
                    file = open(paths[index], 'w', encoding="utf-8")
                    file.write('')
                    file.close()
                except OSError as execp:
                    except_print(execp, "", True)
    print("OK")
    print("NetWork", end="...")
    network_result = network("https://ifconfig.me")
    if not network_result[0]:
        print("Error")
        except_print(network_result[3], "ネットワークに問題があります。", True)
    print("OK")
    print("Java Path", end="...")
    if not shutil.which('java'):
        print("Error")
        print("Javaのパス（環境変数）が通っていません。")
        sys.exit(1)
    print("OK")
    print("All OK!\n")
