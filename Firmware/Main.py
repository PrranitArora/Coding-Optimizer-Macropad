import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Macros, Tap

keyboard = KMKKeyboard()

macros = Macros()
keyboard.modules.append(macros)

# Pins for each button
PINS = [board.D5, board.D8, board.D9, board.D10, board.D11, board.D12]

keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)



# one counter per button
states = [0, 0, 0, 0, 0, 0]

# words for each button, in order
words = [
    ["hello", "world", "!"],     # button 0 cycle
    ["alpha", "beta", "gamma"],  # button 1 cycle
    ["one", "two", "three"],     # button 2 cycle
    ["cat", "dog"],              # button 3 cycle
    ["fixed"],                   # button 4 (always same)
    ["yes", "no"],               # button 5 cycle
]

def get_macro(idx):
    global states

    # get the word list for this button
    lst = words[idx]

    # current index
    i = states[idx]

    # pick word
    word = lst[i]

    # advance index
    i = (i + 1) % len(lst)
    states[idx] = i

    # return macro object
    return KC.MACRO(Tap(word))



def before_press(key):
    index = keyboard.matrix.active_keys.index(key)

    # dynamically update the pressed key’s macro
    keyboard.keymap[0][index] = get_macro(index)


keyboard.before_press = before_press

# temporary macros for each button
button0 = KC.MACRO(Tap(""))
button1 = KC.MACRO(Tap(""))
button2 = KC.MACRO(Tap(""))
button3 = KC.MACRO(Tap(""))
button4 = KC.MACRO(Tap(""))
button5 = KC.MACRO(Tap(""))


keyboard.keymap = [
    [button0, button1, button2, button3, button4, button5]
]


if __name__ == '__main__':
    keyboard.go()
