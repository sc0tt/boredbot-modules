#-*- coding: utf-8 -*-
"""
quotes.py - Willie Quote Module
Original author: Meicceli
Licensed under the GNU Lesser General Public License Version 3 (or greater at your wish).
"""
from willie.module import commands, rate, example
from random import choice
from urllib import quote as conv
from urllib import unquote as unconv


def setup(bot):
    if bot.db and not bot.db.preferences.has_columns('quotes'):
        bot.db.preferences.add_columns(['quotes'])


@commands('aq', 'addquote')
@example(".addquote <Meicceli> embolalia can't code")
def quote_add(bot, trigger):
    """Adds a quote to a database"""

    # converts the quote to ascii format
    try:
        args = conv(trigger.group(2).encode('utf-8'))
    except AttributeError:
        bot.say("No quote given.")
        return
    orig = ''

    # checks if there are any quotes added and if so, stores them into orig
    try:
        orig = str(bot.db.preferences.get(trigger.sender, 'quotes'))
    except TypeError:
        pass

    # Checks if the quote we're adding is already added.
    if args in orig:
        bot.reply("Quote already added!")
        return

    # generates the new quote string
    # (I%20am%20a%20quote|Me%20too|I%20am%20as%20well|)
    quote = orig + args + '|'

    # adds the quote to the database
    bot.db.preferences.update(trigger.sender, {'quotes': quote})
    bot.reply("Quote added!")


@commands('q', 'quote')
def get_conv(bot, trigger):
    """Gets a random quote from the database"""

    # gets all the quotes, removes the trailing "|", and then splits the
    # quotes into quote_list
    try:
        quote_list = bot.db.preferences.get(trigger.sender, 'quotes')[:-1].split("|")
    # checks if there are any quotes
    except TypeError:
        bot.reply("No quotes added!")
        return

    # checks if all the quotes have been deleted
    if len(quote_list) == 1 and quote_list[0] == "":
        bot.reply("No quotes added!")
        return

    # if a quote number is given, this fetches the quote associated with the
    # given number.
    if trigger.group(2):
        try:
            number = int(trigger.group(2))
            output = str(number) + ": " + quote_list[number - 1]
        except ValueError:
            bot.say(u"Must be a number or a string!")
            return
    # if no quote number is given, this picks a quote randomly
    else:
        #(pseudo-)randomly chooses a quote from quote_list
        ans = choice(quote_list)
        # generates the output (7:%20This%20is%20the%20quote)
        output = str(quote_list.index(ans) + 1) + ": " + ans

    # converts the "%20" etc. back into a readable format (7: This is the
    # quote)
    bot.say(unconv(output).decode('utf-8'))


@commands('dq', 'delquote')
@rate(300)
@example('.delquote 3')
def quote_del(bot, trigger):
    """Deletes a quote from the database."""

    del_key = trigger.group(2)

    # gets all the quotes, removes the trailing "|", and then splits the
    # quotes into quote_list
    quote_list = bot.db.preferences.get(trigger.sender, 'quotes')[:-1].split("|")

    # This if-bit allows only me (meicceli) to delete all the quotes, but
    # allows others to delete one quote per 60 seconds (rate is 60)
    if del_key == "all" and trigger.nick.lower() == "markisking":
        bot.db.preferences.update(trigger.sender, {'quotes': ""})
        bot.reply("All quotes deleted!")
        return
    elif del_key.find(":") != -1 and trigger.nick.lower() == "markisking":
        uus_lista = "|".join(quote_list[:int(del_key[0]) - 1]) + "|"
        bot.db.preferences.update(trigger.sender, {'quotes': uus_lista})
        bot.reply("Deleted quotes, starting from " + str(int(del_key[0])))
        return
    elif del_key == "all" and trigger.nick.lower() != "markisking":
        bot.reply("You don't have the permission to do that! Ask Markisking")
        return
    else:
        pass

    # deletes the item by index shown in the beginning of every quote (for
    # example "5: quote" could be deleted with .delquote 5)
    del quote_list[int(del_key[0]) - 1]

    # This bit makes sure that there won't be any "||" found, which would mess
    # up the splitting in .quote (there would be empty strings in the
    # quote_list)
    modified_list = ""
    for i in quote_list:
        modified_list += i + "|"
    if modified_list.find('||') != 1:
        modified_list = modified_list.replace('||', '|')

    # updates the list with the quote removed
    bot.db.preferences.update(trigger.sender, {'quotes': modified_list})
    bot.reply("Quote deleted!")


@commands('sq', 'squote', 'searchquote')
@example('.sq 3, string1 string2')
def quote_search(bot, trigger):
    """Searches quotes. If you want you can use ", " to assign the quote number you'd like to display."""

    args = trigger.group(2)

    # if ", " found, stores the search number into search_number and the query
    # into search_term. If no ", " found, splits search terms with a space
    # (%20)
    if args.find(', ') != -1:
        args = trigger.group(2).split(", ")
        search_term = conv(args[1].encode('utf-8')).split("%20")
        search_number = int(args[0])
    else:
        search_term = conv(trigger.group(2).encode('utf-8')).split("%20")
        search_number = 1

    # gets all the quotes, removes the trailing "|", and then splits the
    # quotes into quote_list
    quote_list = bot.db.preferences.get(
        trigger.sender, 'quotes')[:-1].split("|")

    # this bit performs the search
    for i in search_term:
        findings = [s for s in quote_list if i in s]

    # if quotes are found, store the quote into output.
    try:
        output = "(" + str(findings.index(findings[search_number - 1]) + 1) + "/" + str(len(findings)) + ") - " + \
            str(quote_list.index(findings[search_number - 1]) + 1) + \
            ": " + findings[search_number - 1]
    except IndexError:
        bot.reply("Nothing found.")
        return
    bot.reply(unconv(output).decode('utf-8'))


@commands('lq')
@rate(1800)
def quote_listi(bot, trigger):
    quote_list = bot.db.preferences.get(trigger.sender, 'quotes')[:-1].split("|")
    if not trigger.group(2):
        bot.reply("There are " + str(len(quote_list)) + " quotes.")
    else:
        if len(quote_list) > 5:
            for i in bot.db.preferences.get(trigger.sender, 'quotes')[:-1].split("|"):
                bot.msg(trigger.nick, unconv(i))
            return
        else:
            for i in bot.db.preferences.get(trigger.sender, 'quotes')[:-1].split("|"):
                bot.say(unconv(i))
            return

