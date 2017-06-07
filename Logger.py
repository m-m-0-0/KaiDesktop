# coding=utf-8

# MIT License

# Copyright (c) 2017 Kaikyu

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# 888    d8P  d8b 888                                                .d8888b.                888
# 888   d8P   Y8P 888                                               d88P  Y88b               888
# 888  d8P        888                                               888    888               888
# 888d88K     888 888888 .d8888b  888  888 88888b.   .d88b.         888         .d88b.   .d88888  .d88b.
# 8888888b    888 888    88K      888  888 888 "88b d8P  Y8b        888        d88""88b d88" 888 d8P  Y8b
# 888  Y88b   888 888    "Y8888b. 888  888 888  888 88888888  8888  888    888 888  888 888  888 88888888
# 888   Y88b  888 Y88b.       X88 Y88  888 888  888 Y8b.            Y88b  d88P Y88..88P Y88b 888 Y8b.
# 888    Y88b 888  "Y888  88888P'  "Y88888 888  888  "Y8888          "Y8888P"   "Y88P"   "Y88888  "Y8888

from time import strftime
import inspect

try:
    from termcolor import colored
except:
    print("Installing termcolor...")
    import os
    os.system("python3 -m pip install termcolor")
    from termcolor import colored


WHITE = "white"
RED = "red"
BLUE = "blue"
GREEN = "green"
YELLOW = "yellow"
GREY = "white"
MAGENTA = "magenta"


file = False


def colored2(text, *args):
    return text


def setType(t):
    global file
    if t == 1:
        file = True
    elif t == 0:
        file = False
    else:
        print("Hmm...")


def init():
    global colored
    try:
        old = open("Log.txt").read()
    except:
        old = ""

    with open("OldLog.txt", "w") as fl:
        fl.write(old)
        fl.close()
    with open("log.txt", "w") as fl:
        fl.write("Logger inizializzato.\n")
        fl.close()
    colored = colored2
    pass


def lt():
    return colored(strftime("%H:%M:%S"), GREY)


def printf(text):
    if file:
        with open("log.txt", "a") as fl:
            fl.write(text + "\n")
            fl.close()
    else:
        print(text)


def call_elab(caller_foo):
    if caller_foo == "<module>":
        caller_foo = "module"
    t_len = 17
    caller_foo += (t_len - len(caller_foo)) * " "
    return caller_foo


# Log "error"
def e(text):
    text = str(text)
    tipo = colored("Error", RED)
    caller = colored(call_elab(inspect.stack()[1][3]), RED)
    text = colored("Errore: ", RED) + text
    line = colored("riga: " + str(inspect.getframeinfo(inspect.stack()[1][0]).lineno), RED)
    printf("[ %s  ] Da %s - %s - %s %s" % (tipo, caller, lt(),  text, line))


# Log "debug"
def d(text):
    tipo = colored("Debug", GREEN)
    caller = colored(call_elab(inspect.stack()[1][3]), GREEN)
    printf("[ %s  ] Da %s - %s - %s" % (tipo, caller, lt(), text))


# Log "info"
def i(text):
    tipo = colored("Info", BLUE)
    caller = colored(call_elab(inspect.stack()[1][3]), BLUE)
    printf("[ %s   ] Da %s - %s - %s" % (tipo, caller, lt(), text))


# Log "action"
def a(text):
    tipo = colored("Action", MAGENTA)
    caller = colored(call_elab(inspect.stack()[1][3]), MAGENTA)
    printf("[ %s ] Da %s - %s - %s" % (tipo, caller, lt(), text))


def w(text):
    tipo = colored("Warn", YELLOW)
    caller = colored(call_elab(inspect.stack()[1][3]), YELLOW)
    printf("[ %s   ] Da %s - %s - %s" % (tipo, caller, lt(), text))
