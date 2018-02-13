# Tetris for Slack

チャットボットハッカソンのサンプルです．
Slackでテトリスを遊ぶことができます．

# Get start

1. https://api.slack.com/bot-users のcreating a new bot userをクリックして新しくBotを作成する
2. 適当なチャンネルに1.で作成したBotをInviteする
3. imgフォルダにあるpngファイルをすべてファイル名をemoji名としてslackに登録する
4. Botを取得する

```sh
$ git clone https://github.com/cloud-hackathon/slack-tetris.git
$ cd slack-tetris
```

5. 取得したslack-tetrisディレクトリのmanifest.ymlに環境変数を追加する

```yaml
---
  ...
  env:
    SLACK_API_TOKEN: <1.のOAuth & Permissionsに書いてあるBot User OAuth Access Token>
    SLACK_VERIFICATION_TOKEN: <1.のBasic Informationに書いてあるVerification Token>
    BOT_NAME: <Bot名>
```

6. Cloud FoundryにBotをPushする

```sh
$ cf login -a URL -u USER -p PASS
$ cf push <アプリ名>
```

7. Cloud FoundryアプリのURLを取得する

```sh
$ cf app <アプリ名> | grep urls
urls: tetris-cliquish-dualism.lab3.tamac.me # コピーする
```

8. SlackのEvent SubscriptionsにURLを登録しSubscribe to Bot EventsにMessageイベント3つを追加する

9. テトリスで遊ぶ

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

* https://api.slack.com/apps
* http://euphorie.sakura.ne.jp/junk/page_python_teto.html
* http://slackapi.github.io/python-slackclient/index.html
* https://github.com/slackapi/python-slack-events-api
* https://www.cloudfoundry.org/
* https://www.flaticon.com/
