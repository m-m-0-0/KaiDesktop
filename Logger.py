# coding=utf-8

# Copyright (c) 2017 Kaikyu

# 888    d8P  d8b 888                                                .d8888b.                888
# 888   d8P   Y8P 888                                               d88P  Y88b               888
# 888  d8P        888                                               888    888               888
# 888d88K     888 888888 .d8888b  888  888 88888b.   .d88b.         888         .d88b.   .d88888  .d88b.
# 8888888b    888 888    88K      888  888 888 "88b d8P  Y8b        888        d88""88b d88" 888 d8P  Y8b
# 888  Y88b   888 888    "Y8888b. 888  888 888  888 88888888  8888  888    888 888  888 888  888 88888888
# 888   Y88b  888 Y88b.       X88 Y88  888 888  888 Y8b.            Y88b  d88P Y88..88P Y88b 888 Y8b.
# 888    Y88b 888  "Y888  88888P'  "Y88888 888  888  "Y8888          "Y8888P"   "Y88P"   "Y88888  "Y8888

# Thanks to Konstantin Lepa for Termcolor (https://pypi.python.org/pypi/termcolor)

from time import strftime
import inspect
import os

COLORS = dict(
        list(zip([
            'grey',
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            'white',
            ],
            list(range(30, 38))
            ))
        )
RESET = '\033[0m'

WHITE = "white"
RED = "red"
BLUE = "blue"
GREEN = "green"
YELLOW = "yellow"
GREY = "white"
MAGENTA = "magenta"


file = False


def colored(text, color=None):
    if os.getenv('ANSI_COLORS_DISABLED') is None:
        fmt_str = '\033[%dm%s'
        if color is not None:
            text = fmt_str % (COLORS[color], text)

        text += RESET
    return text


def colored2(text, *args):
    return text


def init(mode=0):
    global colored
    global file

    if mode == 0:
        file = True  # Se file è True il logger scriverà su file
        colored = colored2  # evitiamo che il testo venga colorato perchè andrà su file
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
    else:
        file = False


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
