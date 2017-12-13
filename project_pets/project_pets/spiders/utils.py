"""
Module containing utility methods for parsing data extracted from crawlers
"""
import re


def parse_price(work_str):
    """ Receives a string and removes everything except the numbers
        to transform it to a integer """
    return int(re.sub('[A-z$,.]', '', work_str).strip())

def parse_name(work_str):
    """ Removes unwanted characters from scraped names for data
        uniformity """
    substitutions = [
        ('"', ''),
        ("'", ''),
        ('.', ' '),
        ('-', ' ')
    ]

    for search, replacement in substitutions:
        work_str = work_str.replace(search, replacement)

    return work_str
