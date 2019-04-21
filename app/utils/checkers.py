# -*- coding: utf-8 -*-


def is_integer(num):
    if isinstance(num, int):
        return True
    elif isinstance(num, str):
        try:
            num = int(num)
            return True
        except ValueError:
            return False
    else:
        return False
