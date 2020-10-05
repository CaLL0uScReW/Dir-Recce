

import string
import random


def rstring(len_):
    a = ""
    for i in range(0, len_):
        a += "".join(random.choice(string.letters))
    return a
