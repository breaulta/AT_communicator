#!/usr/bin/python
# -*- coding: utf-8 -*-
#Don't write a pesky .pyc file.
import sys
sys.dont_write_bytecode = True

from module import Transmitter
from module import SMS
from little_free_locker import Locker
from little_free_locker import Lockers


tx = Transmitter()
tx.send_text('5039895540', 'The clock is ticking for Lonzo Ball. The Pelicans guard is now in his fourth season, and it’s still unclear what role makes sense for him in the NBA. His defense and basketball IQ will keep him in the league for a long time, but his streaky jumper and inability to threaten defenses make it hard to fit him in to most starting lineups. He’s really struggling on offense this season, averaging 11.9 points and 4.4 assists per game on just 38.7 percent shooting. New Orleans will have to make a decision on Lonzo this offseason when he enters restricted free agency. This is a prove-it season for the 23-year-old. And he’s not proving much right now.')
