import asyncio
import discord
import os
import random
import math
import psycopg2
import json
import requests
from osrsbox import items_api
from random import randint
from discord.ext import commands

def numify(num):
    if type(num) == int or type(num) == float:
        return int(math.floor(num))
    elif type(num) == str:
        # Remove any commas
        cleanNum = num.replace(',', '')

        try:
            cleanNum = int(cleanNum)
            return cleanNum
        except ValueError:
            pass

        multiplier = 1

        if cleanNum[-1:] == 'k' or cleanNum[-1:] == 'K':  # Thousands
            multiplier = 1000
        elif cleanNum[-1:] == 'm' or cleanNum[-1:] == 'M':  # Millions
            multiplier = 1000 * 1000
        elif cleanNum[-1:] == 'b' or cleanNum[-1:] == 'B':  # Billions
            multiplier = 1000 * 1000 * 1000

        try:
            baseNum = float(cleanNum[0:-1])
            finalQuantity = int(math.floor(baseNum * multiplier))
            commaMoney = "{:,d}".format(finalQuantity)
            return finalQuantity
        except ValueError:
            return "couldn't multiply"


def short_numify(num, multiplier):

    def remove_last_char_for_round(string):
        shortened = string
        if shortened[-1:] == '0':
            shortened = shortened[0:-1]
            if shortened[-1:] == '.':
                shortened = shortened[0:-1]
                return shortened
            else:
                return remove_last_char_for_round(shortened)
        else:
            return shortened

    try:
        raw_number = numify(num) * multiplier

        shortened = ''
        if raw_number >= 1000 * 1000 * 1000:
            output = raw_number/(1000 * 1000 * 1000)
            shortened = "{0:.2f}".format(output)
            shortened = remove_last_char_for_round(shortened)
            return f"{shortened}B"
        elif raw_number >= 1000 * 1000:
            output = raw_number/(1000 * 1000)
            shortened = "{0:.2f}".format(output)
            shortened = remove_last_char_for_round(shortened)
            return f"{shortened}M"
        elif raw_number > 1000:
            output = raw_number/(1000)
            shortened = "{0:.2f}".format(output)
            shortened = remove_last_char_for_round(shortened)
            return f"{shortened}K"
        else:
            return raw_number
    except Exception as e:
        print("Error short-numifying:", e)
        pass


def tidy_float(s):
    """Return tidied float representation.
    Remove superfluous leading/trailing zero digits.
    Remove '.' if value is an integer.
    Return '****' if float(s) fails.
    """
    # float?
    try:
        f = float(s)
    except ValueError:
        return '****'
    # int?
    try:
        i = instr(i)
    except ValueError:
        pass
    # scientific notation?
    if 'e' in s or 'E' in s:
        t = s.lstrip('0')
        if t.startswith('.'): t = '0' + t
        return t
    # float with integral value (includes zero)?
    i = int(f)
    if i == f:
        return str(i)
    assert '.' in s
    t = s.strip('0')
    if t.startswith('.'): t = '0' + t
    if t.endswith('.'): t += '0'
    return t