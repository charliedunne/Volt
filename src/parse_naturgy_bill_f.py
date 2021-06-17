#!/usr/bin/python3

##
# @file parse_naturgy_bill_f.py
# @issue 1.0
# @last 20210617
# @user cavt
#
# @brief Function to parse the XLS from naturgy bill and generate
# an output in json format
#
# @version v1.0 | 20210617 | cavt |
# Initial version
#
# Imports
#

import xlrd
import argparse
import json

# Configuration stuff
CFG = {}
CFG['loc_bill'] = [4, 5]
CFG['loc_period'] = [5, 5]
CFG['loc_cups'] = [7, 5]
CFG['start_off'] = 13
CFG['date'] = 0
CFG['timefrom'] = 1
CFG['timeto'] = 2
CFG['type'] = 3
CFG['consumption'] = 4
CFG['price'] = 5

##
# Find the last row with data
def find_last_row(sh):
    """
    This function will find the last row where there is data from the
    book sheet handle provided

    :param sh: Handle to the Book Sheet to search into
    :return: Row index with the last valid data
    """
    
    for row in range(CFG['start_off'], sh.nrows):
        if (sh.cell_value(rowx=row, colx=0) == ''):
            return row-1

def parse_naturgy_bill(file):
    """
    This function will parse an excel file that is provided along with the
    bill with the consumption details by Naturgy Energy S.A to their customers.

    :param file: Filename of the .xls file to parse
    :return: List with two elements.
    The first one will be a return code with the following values:
    · 0 -> Operation Success
    · -1 -> Invalid file (.xls is required)
    · -2 -> Invalid format (The main sheet must be called 'Curva Horaria')
    · -3 -> Invalid format (Headers for data are not in the expected row)
    · -4 -> Invalid format (Last row has not been properly found)
    · -5 -> Invalid data (Period from the bill does not match the data)
    The second element of the list will contain the JSON with the data if the
    return code is 0 (SUCCESS) or 0 otherwise.
    """

    if not file.endswith('.xls'):
        return(-1, 0)

    # Open the excel file
    book = xlrd.open_workbook(file)

    # Get the main sheet
    sh = book.sheet_by_index(0)

    # Validate the book
    if (sh.name != 'Curva Horaria'):
        return(-2, 0)
        
    if (sh.cell_value(rowx=CFG['start_off']-1, colx=CFG['date']) != 'Fecha'):
        return(-3, 0)

    last_row = find_last_row(sh)

    if (sh.cell_value(rowx=last_row+2, colx=0) != 'Consumo agrupado:'):
        return(-4, 0)

    if (sh.cell_value(rowx=last_row+4, colx=0) != 'Periodo'):
        return(-4, 0)

    # Get general information
    bill = sh.cell_value(rowx=CFG['loc_bill'][0], colx=CFG['loc_bill'][1])
    period = sh.cell_value(rowx=CFG['loc_period'][0], colx=CFG['loc_period'][1])
    cups = sh.cell_value(rowx=CFG['loc_cups'][0], colx=CFG['loc_cups'][1])

    # Validate the range
    date_from = sh.cell_value(rowx=last_row+5, colx=0)
    date_to = sh.cell_value(rowx=last_row+5, colx=1)
    period_from = period.split('a')[0].strip()
    period_to = period.split('a')[1].strip()

    if (date_from != period_from):
        return(-5, 0)

    if (date_to != period_to):
        return(-5, 0)

    # Build the json
    out = {}
    out['bill'] = bill
    out['period_start'] = period_from
    out['period_end'] = period_to
    out['cups'] = cups
    out['data'] = []
    
    # Output the JSON
    for row in range(CFG['start_off'], last_row+1):
        out['data'].append(
            {'date':sh.cell_value(rowx=row, colx=CFG['date']),
             'timefrom':sh.cell_value(rowx=row, colx=CFG['timefrom']),
             'timeto':sh.cell_value(rowx=row, colx=CFG['timeto']),
             'type':sh.cell_value(rowx=row, colx=CFG['type']),
             'consumption':sh.cell_value(rowx=row, colx=CFG['consumption']),
             'price':sh.cell_value(rowx=row, colx=CFG['price'])})
    
    # Output the JSON with the data
    return(0, json.dumps(out))
