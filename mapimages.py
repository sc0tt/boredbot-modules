import willie
import redis

db = redis.Redis(db=1)

@willie.module.commands('m')
def mapimages(bot, trigger):
  word = trigger.group(2)

  if word:
    word = word.split()
    key = word[0]

    image = db.get(key.lower())

    if image:
      bot.say(image)
    else:
      if len(word) == 1:
        bot.say("Not Found")
      else:
        word = " ".join(word[1:])
        bot.say("%s = %s" % (key, word))
        db.set(key.lower(), word)
  else:
    bot.say("-- .m <key> <value>")