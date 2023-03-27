# Autoer-1

<img alt="GitHub tag (latest SemVer pre-release)" src="https://img.shields.io/github/v/tag/stsaria/Autoer-1?include_prereleases" style="display: flex;">　<img alt="GitHub all releases" src="https://img.shields.io/github/downloads/stsaria/Autoer-1/total" style="display: flex;">　<img alt="GitHub license" src="https://img.shields.io/github/license/stsaria/Autoer-1" style="display: flex;">　<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/stsaria/Autoer-1" style="display: flex;">


## 1.概要
・Pythonで記述された マインクラフトサーバーの作成支援ソフトウェアです。<br>
・LinuxとWindowsに対応しています。（Macでの動作は保証できません。）<br>
・Gui (Graphical User Interface)版はありません。 Cui (Character User Interface) などのコンソールベースのプログラムです。

## 2.制限
・このプログラムを違法に使用しないでください。<br>
・ライセンスはCreative Commons Zero v1.0 Universal です。(ただし、Version v0.6-beta以前のコード (v0.5-alphaなど.) は BSD-2 が適合となります。)

## 3.対応OS(オペレーションシステム)
・オペレーションシステム：Windows10<br>
　Linux(確認できたOS:Ubuntu/Debian)

## 4.Pancakeの必要要件

・Javaの環境(マインクラフトのバージョンに合うJavaの環境が、必要になります。<br>　詳しくは<a href="support-java-version.md">こちらでご覧ください</a>)<br>
・実行ファイル（exeファイルなど）を実行できる環境（管理者権限が必要になる場合があります。）<br>
・ネット環境（最悪テザリングでもOK）

## 5.使い方

・1: 設定したいマインクラフトサーバーのポートを開いてください。(例:25565/tcp)
・2: 公開しているPancakeの実行ファイルをダウンロードしてください。（配布場所: https://github.com/stsaria/Autoer-1/releases）
・3: ダウンロードしたファイルを実行してください。
・4: 案内に沿ってサーバーを作成・起動してください。

## 6.プログラム実行時に引数を与える方法
※ まだ、このモードはテスト版として搭載しています。<br>
※ 問題がある場合は、このリポジトリのIssueに報告をしてください。<br>
### ・起動時のチェックをスキップする場合
```
[hoge@cp1 ~]$ ./Autoer -notcheck
（ただし、この引数は他の引き数にかぶらなければ、どこにおいても問題なし）
```
### ・作成する場合
#### コマンド
```
[hoge@cp1 ~]$ ./Autoer -make [server_name] [server_version] [server_port] [eula(True, False)]
```
※ ただし、このモードで作成する場合は forgeやpapermc,spigotmc などには対応していません。
### ・作成する場合（ファイルで複数作成）
#### ファイル
// text.txt
```
[server_name] [server_version] [server_port] [eula(True, False)]
```
（改行で区切れば、**1コマンド**で複数作成することができます。）
#### コマンド
```
[hoge@cp1 ~]$ ./Autoer -make -file [file_name]
```
このように引数を与えさせます。<br>
※ ただし、このモードで作成する場合は forgeやpapermc,spigotmc などには対応していません。
### ・実行する場合
#### コマンド
```
[hoge@cp1 ~]$ ./Autoer -control [server_name(例: minecraft-2023-03-25-02-09-50-927255 例2(サーバー番号): 1)] [server_xms] [server_xmx] [java_argument(任意)]
```

## 7.プロキシモードとは

※ プロキシモードの自動起動などの設定モードは搭載していません<br>
※ まだ、このモードはテスト版として搭載しています。<br>
※ 問題がある場合は、このリポジトリのIssueに報告をしてください。<br>

・プロキシモードでポートやホストを入力して、続行するとプロキシサーバーを立てることができます。<br>
・終了する場合は、強制終了で終了させられます。（なので、Ctrl+Cなどでは終了できない可能性があります。）
