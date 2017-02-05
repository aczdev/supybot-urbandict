###
# UrbanDict ~ plugin for searching definitions at UrbanDictionary.com
# Copyright (c) 2016, Adam Cz.
# All rights reserved.
#
#(TODO): fix colouring
#
###

import requests
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('UrbanDict')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x

# Predefined IRC colours
RED = '\x0304'
GREEN = '\x0309'
ORANGE = '\x0307'
MAGENTA = '\x0313'
RA = '\x0F'

UD = 'http://api.urbandictionary.com/v0/define?term='

class UrbanDict(callbacks.Plugin):
    """Plugin gathers definitions of a keyword from UrbanDictionary.com"""
    def votebar(self, up, down):
        try:
            mean = float(up)/(up+down)
        except ZeroDivisionError:
            mean = 0

        count = int(round(mean*10))
        bar = ''
        bar = bar.ljust(count, '+')
        bar = bar.ljust(10, '-')
        bar = GREEN + bar[:count] + RED + bar[count:]
        return bar

    def ud(self, irc, msg, args, text):
        """<term>

        This option displays three best definitions of looked term from
        UrbanDictionary.com website.
        """
        try:
            req = requests.get(UD + text)
            js = req.json()

            defs = js['list']

            head =  ORANGE + 'UrbanDictionary.com' + GREEN + ' Phrase: ' + RA + text
            irc.reply(head)

            if len(defs) >= 3:
                amount = 3
            elif len(defs) == 0:
                irc.reply(RED + 'Sorry, but the term could not be found! :(' + RA)
                return None
            else:
                amount = len(defs)

            for i in range(amount):
                up = defs[i]['thumbs_up']
                down = defs[i]['thumbs_down']
                define = defs[i]['definition']
                link = defs[i]['permalink']
                example = defs[i]['example']

                stripped = lambda s: "".join(i for i in s if 31 < ord(i) < 127)
                example = stripped(example)
                if len(example) > 180:
                    example = example[:180] + '(...)'
                elif len(example) == 0:
                    example = RED + 'none' + RA

                counter = MAGENTA + '[' + RA + str(i+1) + '/' + RA + str(amount) + MAGENTA + '] ' + RA

                info =  GREEN + 'Link: ' + RA + link + ' | ' + \
                        GREEN + 'Votes: ' + GREEN + str(up) + ' ' + self.votebar(up, down) + ' ' + \
                        str(down) + RA + ' | ' + GREEN + 'Definition: ' + RA

                info2 = GREEN + 'Example: ' + ORANGE + example

                irc.reply(counter + info)
                irc.reply(define)
                irc.reply(info2)

        except requests.exceptions.HTTPError:
            irc.error('HTTP error!')
    ud = wrap(ud, ['text'])

Class = UrbanDict
