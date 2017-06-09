# coding=utf-8
from time import sleep
import psutil


def text_formatter(txt):
    try:
        line = ""
        final = ""
        max_width = 0
        lines = 0
        if "[_]" not in txt:
            addon = "\n"
        else:
            addon = ""
        for word in txt.split():
            line += " " + word
            if len(line) > max_width:
                max_width = len(line)
            if len(line) > 20:
                final += line + addon
                line = ""
                lines += 1

        final += line

        while "[_]" in final:
            final = final.replace("[_]", "\n")

        return final, lines, max_width
    except Exception as err:
        return "Errore", 1, 5


def fade_in(obj):
    op = 0
    while op < 1:
        obj.setWindowOpacity(op)
        sleep(0.005)
        op += 0.005


def fade_out(obj):
    op = 1
    while op > 0:
        obj.setWindowOpacity(op)
        sleep(0.001)
        op -= 0.002


def get_cores():
    return int(psutil.cpu_count())


def get_freq():
    return int(int(psutil.cpu_freq()[0]))


def get_max_freq():
    return int(int(psutil.cpu_freq()[2]))


def get_usage():
    return int(psutil.cpu_percent())


def get_ram():
    return int(psutil.virtual_memory()[2])


def get_battery():
    if psutil.sensors_battery():
        return int(psutil.sensors_battery()[0])
    else:
        return None


def has_battery():
    if psutil.sensors_battery():
        return True
    else:
        return False
