#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import getitem


def deep_getitem(obj, path):
    try:
        return reduce(getitem, path.split(","), obj)
    except (KeyError, TypeError):
        return None


def get(obj, key, default=0):
    v = obj.get(key, None)
    if not v:
        return default
    if isinstance(v, basestring):
        if is_trash(v):
            return default
        else:
            return v
    else:
        if is_int(v):
            return int(v)
        elif is_float(v):
            return float(v)


def is_int(v):
    try:
        v = int(v)
    except ValueError:
        return False
    except TypeError:
        return False
    return True


def is_float(v):
    if "." in v:
        try:
            float(v)
        except ValueError:
            return False
        return True
    return False


def is_trash(v):
    if v == "n/a":
        return True
    if "-" in v:
        return v.count("-") == len(v)
    else:
        return False