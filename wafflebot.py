import datetime
import redis
import markovify
import willie

# Change this if you want, it will increase the DB size eventually.
timeout = 60 * 60 * 24 * 30 # 60s * 60m * 24h * 30d = 1 month
ignore = ["http"]

MAX_OVERLAP_RATIO = 0.5
MAX_OVERLAP_TOTAL = 10

db = redis.Redis(db=0)

class WaffleBotText(markovify.Text):
  def test_sentence_input(self, sentence):
    return True

  def _prepare_text(self, text):
    text = text.strip()

    if not text.endswith((".", "?", "!")):
      text += "."

    return text

  def sentence_split(self, text):
    lines = text.splitlines()
    text = " ".join([self._prepare_text(line) for line in lines if line.strip()])

    return markovify.split_into_sentences(text)


@willie.module.rule(r'.*$')
def wafflebot(bot, trigger):
  for ignored_item in ignore:
    if ignored_item.lower() in trigger.lower():
      continue

  # have at least 5 words
  if len(str(trigger).split(" ")) < 5:
    return

  today = datetime.datetime.now()
  key = "%s%s:%s" % (today.month, today.day, trigger.nick.lower())
  db.sadd(key, str(trigger))
  db.expire(key, timeout)


@willie.module.commands('talk', 'wb')
def wafflebot_talk(bot, trigger):
  nick = trigger.group(2)
  if nick:
    pattern = "*:%s" % nick.lower()
    min_lines = 200
  else:
    pattern = "*"
    min_lines = 100

  results = []
  for k in db.keys(pattern):
    results.extend(db.smembers(k))

  if len(results) < min_lines:
    bot.say("Sorry %s, there is not enough data." % trigger.nick)
  else:
    model = WaffleBotText("\n".join([r.decode('utf8') for r in results]))
    resp = model.make_short_sentence(500,
      max_overlap_total=MAX_OVERLAP_TOTAL, 
      max_overlap_ratio=MAX_OVERLAP_RATIO)
    bot.say(resp)

