import requests
import json
import willie
import random

@willie.module.commands('ud', 'urb')
def urbandict(phenny, input):
    """.urb <word> - Search Urban Dictionary for a definition."""
    word = input.group(2)
    if not word:
        return
    response = requests.get("http://api.urbandictionary.com/v0/define", params={"term": word})
    data = response.json()
    if data['result_type'] == 'no_results':
        phenny.say("No results found for {0}".format(word))
        return
    result = data['list'][0]

    response = "{0}: {1} - {2}".format(word, result['definition'].strip()[:256], result["permalink"])
    phenny.say(response)

@willie.module.commands('udrand', 'urbrand')
def udrand(bot, trigger):
  data = requests.get("http://api.urbandictionary.com/v0/random").json()
  result = random.choice(data["list"])
  response = "{0}: {1} - {2}".format(result['word'], result['definition'].strip()[:256], result["permalink"])
  bot.say(response)
