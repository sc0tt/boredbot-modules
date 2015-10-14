import requests
import willie

# TODO: Make these config options c:
announce_chan = "#boardgamers"
streamers = [
  "sc00ty",
  "pacifist117",
  "markiskingm",
  "supersocks",
  "agentxleavening"
]

currently_streaming = {}

@willie.module.interval(10)
def monitor_streamers(bot):
  streaming_names = []
  streaming = requests.get('https://api.twitch.tv/kraken/streams', params={"channel": ",".join(streamers)}).json()
  results = []
  for streamer in streaming["streams"]:
    streamer_name = streamer["channel"]["name"]
    streamer_game = streamer["channel"]["game"]
    streamer_url = streamer["channel"]["url"]
    streamer_viewers = streamer["viewers"]
    
    if streamer_name not in currently_streaming:
      currently_streaming[streamer_name] = streamer_game
      results.append("%s just went live playing %s! (%s - %s viewer%s)" % (streamer_name, 
                                                                          streamer_game, 
                                                                          streamer_url, 
                                                                          streamer_viewers, 
                                                                          "s" if streamer_viewers != 1 else ""))
    elif streamer_game != currently_streaming[streamer_name]:
      currently_streaming[streamer_name] = streamer_game
      results.append("%s just started playing %s! (%s - %s viewer%s)" % (streamer_name, 
                                                                        streamer_game, 
                                                                        streamer_url, 
                                                                        streamer_viewers, 
                                                                        "s" if streamer_viewers != 1 else ""))

    streaming_names.append(streamer_name)

  if results:
    bot.msg(announce_chan, ", ".join(results))  

  # Remove people who stopped streaming
  for streamer in currently_streaming.keys():
    if streamer not in streaming_names:
      del currently_streaming[streamer]



@willie.module.commands('twitchtv','tv','twitch', 'teevee')
@willie.module.example('.tv  or .tv twitchusername')
def streamer_status(bot, trigger):
  streamer_name = trigger.group(2)
  query = streamers if streamer_name is None else streamer_name.split(" ")

  streaming = requests.get('https://api.twitch.tv/kraken/streams', params={"channel": ",".join(query)}).json()
  results = []
  for streamer in streaming["streams"]:
    streamer_name = streamer["channel"]["name"]
    streamer_game = streamer["channel"]["game"]
    streamer_url = streamer["channel"]["url"]
    streamer_viewers = streamer["viewers"]
    
    results.append("%s is playing %s (%s - %s viewer%s)" % (streamer_name, 
                                                           streamer_game, 
                                                           streamer_url, 
                                                           streamer_viewers, 
                                                           "s" if streamer_viewers != 1 else "" ))
  if results:
    bot.say(", ".join(results))
  else:
    bot.say("Nobody is currently streaming.")


