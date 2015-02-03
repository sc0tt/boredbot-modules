"""
h1x0.py - Easily make an m.h1x0.com/ mirror link for chat
"""
import willie
import random
@willie.module.commands('h', 'h1x0')
def h(bot, trigger):
    """Easily make an m.h1x0.com/ mirror link for chat"""
    pattern = "http://m.h1x0.net/"
    toMirror = trigger.group(2)
    bot.say(pattern + toMirror);
