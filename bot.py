import logging
import os
import time
from slackclient import SlackClient
from tetris import Tetris, HEIGHT, WIDTH


# get slack client
sc = SlackClient(os.environ.get("SLACK_API_TOKEN"))

# get tetris
tetris = Tetris()

# load bot info
BOT_NAME = os.environ.get("BOT_NAME")
bot_id = ""
resp = sc.api_call("users.list")
if resp.get('ok'):
  for user in resp.get('members'):
    if 'name' in user and user.get('name') == BOT_NAME:
      bot_id = user.get('id')
BOT_ID = bot_id

# make logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# log to file
fh = logging.FileHandler("bot.log")
logger.addHandler(fh)

# log to stdout
sh = logging.StreamHandler()
logger.addHandler(sh)

# set logging format
formatter = logging.Formatter(
  "%(asctime)s : %(name)s : %(lineno)d : %(levelname)s : %(message)s")
fh.setFormatter(formatter)
sh.setFormatter(formatter)

# define omits
omits = {
  "d": "down",
  "b": "bottom",
  "l": "left",
  "r": "right",
  "t": "turn",
}

# define support messages
texts = {
  "start": "game start!",
  "down": "down",
  "bottom": "bottom",
  "left": "left",
  "right": "right",
  "turn": "turn",
  "stop": "stop",
  "help": (
    "usage\n"
    "```start: start new game\n"
    "down|d: move a block down\n"
    "bottom|b: move a block to bototm\n"
    "left|l [n] (1~9, default 1): move a block to left [n] times\n"
    "right|r [n] (1~9, default 1): move a block to right [n] times\n"
    "turn|t: turn a block\n"
    "stop: stop the game```"
  ),
  "playing": "already playing!",
  "not_playing": "go ahead with start command!",
  "cannot_move": "cannot move a block!",
  "over": "game over!",
}

# define block emojis
emojis = {
  -1: ":tetris_gray:",
  0: ":tetris_white:",
  1: ":tetris_green:",
  2: ":tetris_orange:",
  3: ":tetris_pink:",
  4: ":tetris_purple:",
  5: ":tetris_yellow:",
  6: ":tetris_blue:",
  7: ":tetris_red:",
}


def start():
  tetris.playing = True
  tetris.clear()


def down():
  success = tetris.down()
  if not success:
    tetris.player = None
    tetris.playing = False
  return success


def bottom():
  success = tetris.bottom()
  if not success:
    tetris.player = None
    tetris.playing = False
  return success


def left():
  return tetris.move(-1)


def right():
  return tetris.move(1)


def turn():
  return tetris.turn()


def stop():
  tetris.player = None
  tetris.playing = False
  return True


def get_playground():
  playground = ""
  for y in range(HEIGHT - 1):
    for x in range(WIDTH - 2):
      # left lane
      if x == 0:
        playground += emojis[-1]

      # background or block
      b = tetris.block(x + 1, y)
      if b >= 1:
        playground += emojis[b]
      else:
        playground += emojis[0]

      # right lane
      if x == 9:
        playground += emojis[-1]
        playground += "\n"
  return playground


def post_message(channel, command):
  text = texts.get(command, "message not defined")
  with_playground = ["start", "down", "bottom", "left", "right", "turn"]
  if command in with_playground:
    text += "\n"
    text += get_playground()
  sc.api_call(
    "chat.postMessage",
    channel=channel,
    text=text,
    thread_ts=tetris.player,
    as_user=True
  )


def handle_message(message):
  command = message["text"].split()[1]
  if command in omits.keys():
    command = omits.get(command)
  if command in ["left", "right"] and len(message["text"].split()) > 2:
    try:
      repeat = int(message["text"].split()[2])
    except:
      repeat = None
  else:
    repeat = None
  channel = message["channel"]
  if not tetris.player:
    tetris.player = message["ts"]

  try:
    if command == "start":
      if tetris.playing:
        post_message(channel, "playing")
      else:
        eval(command)()
        post_message(channel, command)
    else:
      if tetris.playing:
        if repeat and repeat < WIDTH - 2:
          for i in range(repeat):
            eval(command)()
          post_message(channel, command)
        else:
          if eval(command)():
            post_message(channel, command)
          else:
            post_message(channel, "cannot_move")
      else:
        post_message(channel, "not_playing")
  except Exception as e:
    logger.warn(e)
    post_message(channel, texts.get("help"))


def get_mentioned_message(message_list):
  mentions = [BOT_NAME, "<@%s>"%BOT_ID]
  if len(message_list) > 0:
    for message in message_list:
      if message.get("text") and message["text"].split()[0] in mentions:
        return message
  return {}


if __name__ == "__main__":
  # start to call real time messaging api
  if sc.rtm_connect():
    while True:
      message = get_mentioned_message(sc.rtm_read())
      if message:
        handle_message(message)
  else:
    logger.warn("Connection Failed")
