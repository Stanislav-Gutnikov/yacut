import string
from random import choice


def get_unique_short_id():
    str_ = string.ascii_letters
    for i in range(1, 10):
        str_ += str(i)
    new_str = ''
    while len(new_str) <= 5:
        new_str += choice(str_)
    return new_str
