#!/usr/bin/env python

# Prints a sick bash prompt

# Shortens paths for printing the cwd in a terminal withing taking up much space
# e.g. "~/ridiculously/long/current/directory" becomes "~/ridicu*/long/current/direct*"
# Also shortens current git branch

import os, re, socket

class color:
    CLEAR       = '\[\033[00m\]'
    BOLD        = '\[\033[01m\]'
    UNDERLINE   = '\[\033[04m\]'
    BLACK       = '\[\033[30m\]'
    RED         = '\[\033[31m\]'
    GREEN       = '\[\033[32m\]'
    BROWN       = '\[\033[33m\]'
    BLUE        = '\[\033[34m\]'
    PURPLE      = '\[\033[35m\]'
    CYAN        = '\[\033[36m\]'
    LIGHT_GRAY  = '\[\033[37m\]'
    DARK_GRAY   = '\[\033[90m\]'
    LIGHT_RED   = '\[\033[91m\]'
    LIGHT_GREEN = '\[\033[92m\]'
    YELLOW      = '\[\033[93m\]'
    LIGHT_BLUE  = '\[\033[94m\]'
    LIGHT_PURPLE= '\[\033[95m\]'
    LIGHT_CYAN  = '\[\033[96m\]'
    WHITE       = '\[\033[97m\]'

FREE_WIDTH = 30 # Minimum number of free columns to keep for typing commands

user = os.getlogin()
host = socket.gethostname()
cwd = re.sub("^{}".format(os.getenv('HOME')), "~", os.getenv('PWD'))
gitbranch = os.popen("git rev-parse --abbrev-ref HEAD 2> /dev/null").read().strip()
if gitbranch == "":
    gitbranchformatted = ""
else:
    gitbranchformatted = " [{}]".format(gitbranch)
virtualenv = os.popen("basename $VIRTUAL_ENV 2> /dev/null").read().strip()
if virtualenv == "":
    virtualenvformatted = ""
else:
    virtualenvformatted = " ({})".format(virtualenv)
#time = time.strftime("%H:%M:%S")

promptformat = 'color.BOLD + color.LIGHT_GREEN + user + "@" + host + color.CLEAR + ":" + color.BOLD + color.LIGHT_BLUE + cwd + color.CLEAR + color.CYAN + gitbranchformatted + color.PURPLE + virtualenvformatted + color.CLEAR + u" \u00bb "'
promptnocolor = re.sub(r'\\\[\x1b\[\d\dm\\\]', '', eval(promptformat)) # Strips the colors to get accurate len in chars
promptwidth = len(promptnocolor)
termwidth = int(os.popen("tput cols").read())

# Words that are are allowed to trim (i.e. all dirs in cwd and git branch)
trimwords = cwd.split('/')
trimwords.append(virtualenv)
trimwords.append(gitbranch)

trimdelta = (promptwidth + FREE_WIDTH) - termwidth # Number of columns to trim

while trimdelta > 0:
    i = trimwords.index(max(trimwords, key=len)) # Index of longest word
    trimwords[i] = trimwords[i][:-2] + '*' # Take off the last 2 chars and append a '*'
    trimdelta -= 1

# New shortened variables
gitbranch = trimwords.pop()
virtualenv = trimwords.pop()
cwd = '/'.join(trimwords)

if gitbranch == "":
    gitbranchformatted = ""
else:
    gitbranchformatted = " [{}]".format(gitbranch)

if virtualenv == "":
    virtualenvformatted = ""
else:
    virtualenvformatted = " ({})".format(virtualenv)

print eval(promptformat).encode('utf-8')
