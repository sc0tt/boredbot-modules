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
  lines = db.get(trigger.nick) or 0
  bot.say("%s: You've said %s lines" % (trigger.nick, lines))
