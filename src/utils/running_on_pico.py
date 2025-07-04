import sys


def running_on_pico():
    if sys.implementation.name == "micropython":
        try:
            import os

            return "Raspberry Pi" in os.uname().machine
        except:
            return True
    return False
