"""モジュールの読み込み"""
import os
import sys
import shutil
import socket
import requests
import platform
import ctypes

from Etc import etc
# ※ユーザーはrequestsを入れる必要があります（もしくは、同梱されたソフトウェアを使う）

def check_platform():
    user_use_platform = platform.system()
    if not user_use_platform in ["Windows", "Linux"]:
        print("WindowsまたはLinux以外のOSを使用しています。\n続行できません。")
        input()
        sys.exit(1)

def except_print(except_text, text, stop):
    """例外を表示する関数"""
    print("エラー(例外)が発生しました\n",text)
    while True:
        except_choice = etc.input_yes_no("\n例外を表示しますか？ \nはい[YES]\nいいえ[No]\n[Y/n]: ")
        if except_choice:
            print("詳細------\n",except_text)
        break
    if stop:
        if except_choice:
            input()
        sys.exit(1)

def is_admin():
    """アドミン（管理者権限）で実行しているか確認する関数"""
    user_use_platfrom = platform.system()
    if user_use_platfrom == "Windows":
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    else:
        is_admin = os.geteuid() == 0 and os.getuid() == 0
    
    if not is_admin:
        print("管理者権限で実行してください。")
        sys.exit(3)

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
    check_platform()
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
