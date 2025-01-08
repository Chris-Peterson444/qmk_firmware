#! /usr/bin/env python3
"""reset_ploopy

Put ploopy nano in bootloader mode by ensuring the following LEDs are on at the
same time:
    - Scroll Lock
    - Num Lock
    - Caps Lock
"""

import subprocess
import sys
import time

from pynput.keyboard import Controller, Key


# Toggle Caps Lock
def press_caps(keyboard):
    keyboard.press(Key.caps_lock)
    keyboard.release(Key.caps_lock)


def press_num(keyboard):
    keyboard.press(Key.num_lock)
    keyboard.release(Key.num_lock)


# For whatever reason pynput doesn't work for scroll lock, so we need to use
# xset directly. Unfortunately xset doesn't work for caps or num lock!
def scroll_on():
    subprocess.run("xset led named 'Scroll Lock'", shell=True)


def scroll_off():
    subprocess.run("xset -led named 'Scroll Lock'", shell=True)


def get_xset_values() -> str:
    return subprocess.run(
        "xset q | grep 'Caps Lock'",
        shell=True,
        capture_output=True,
        encoding="utf-8",
    ).stdout


def main() -> int:
    print(__doc__)
    keyboard = Controller()

    print(f"Got original:\n{get_xset_values()}")

    press_caps(keyboard)
    press_num(keyboard)
    scroll_on()

    print(f"Set to:\n\n{get_xset_values()}")

    print("waiting a second...")
    time.sleep(1)

    print("reverting")
    press_caps(keyboard)
    press_num(keyboard)
    scroll_off()

    print(f"Finally:\n\n{get_xset_values()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
