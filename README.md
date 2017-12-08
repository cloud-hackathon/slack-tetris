# Tetris for Slack

チャットボットハッカソンのサンプルです．
Slackでテトリスを遊ぶことができます．

# Get start

1. https://api.slack.com/bot-users のcreating a new bot userをクリックして新しくBotを作成する
2. 適当なチャンネルに1.で作成したBotをInviteする
3. imgフォルダにあるpngファイルをすべてファイル名をemoji名としてslackに登録する
4. Botを動かすマシンに環境変数をセットする

```sh
$ export SLACK_API_TOKEN=<1.で取得したTOKEN>
$ export BOT_NAME=<1.で設定したBot Name>
```

5. botを起動する

```sh
$ git clone https://github.com/cloud-hackathon/slack-tetris.git
$ cd slack-tetris
$ pip install -r requirements.txt
$ python bot.py
```

6. テトリスで遊ぶ

# Commands

Slackで以下の用に投稿するとBotを操作できます．

bot名 command

入力可能なコマンドは以下の通りです．
未定義のコマンドを入力するとヘルプが表示されます．

```skack
start: テトリスを開始
down|d: ブロックを1マス下に移動
bottom|b: ブロックを一番したまで移動
left|l [n]: ブロックをnマス左に移動，1<=n<=9, default n=1
right|r [n]: ブロックをnマス右に移動，1<=n<=9, default n=1
turn|t: プロックを回転
stop: テトリスを終了
```

# Reference

* http://euphorie.sakura.ne.jp/junk/page_python_teto.html
* http://slackapi.github.io/python-slackclient/index.html
* https://www.flaticon.com/
