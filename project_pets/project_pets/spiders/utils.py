"""
Module containing utility methods for parsing data extracted from crawlers
"""
import re


def parse_price(work_str):
    """ Receives a string and removes everything except the numbers
        to transform it to a integer """
    return int(re.sub('[A-z$,.]', '', work_str).strip())