import willie
import redis

db = redis.Redis(db=3)

@willie.module.commands('kadd')
def mapimages(bot, trigger):
  img = trigger.group(2)

  if img:
    db.set(img, None)
    bot.say("Added.")
  else:
    bot.say("-- .k <url>")

@willie.module.commands('k')
def rand_image(bot, trigger):
  img = trigger.group(2)
  if img:
    if db.get(img) is None:
      db.set(img, True)
      bot.say("Added.")
    else:
      bot.say("Already exists.")
  else:
    k = db.randomkey()
    bot.say("k %s" % (k))
