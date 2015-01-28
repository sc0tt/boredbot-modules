import redis
import willie

db = redis.Redis(db=2)

@willie.module.rule(r'.*$')
def lines(bot, trigger):
  if db.get(trigger.nick) is None:
    db.set(trigger.nick, 0)
  db.incr(trigger.nick)

@willie.module.commands('lines')
def getlines(bot, trigger):
  user = trigger.group(2) or trigger.nick
  lines = db.get(user) or 0
  bot.say("%s has said %s lines" % (user, lines))
