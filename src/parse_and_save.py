#!/usr/bin/env python3

##
# @file parse_and_save.py
# @issue 1.0
# @last 20210618
# @user cavt
#
# @brief This function will handle the the parse of a file
# and afterwards the save into the database
#
# @args
# filename: filename (including extension of the file to parse)

# @version v1.0 | 20210618 | cavt | 
# Initial version
# @version v1.1 | 20210916 | cavt | 
# Update with return codes and logging messages

from db_connector import store_data
from parse_naturgy_bill_f import parse_naturgy_bill
import argparse
import logging as log

# Configure logging file
log.basicConfig(filename='/var/log/volt/volt.log', encoding='utf-8', level=log.DEBUG, format='%(asctime)s [%(levelname)s] <%(filename)s:%(lineno)d>:  %(message)s')

# Parse arguments
arg_parser = argparse.ArgumentParser(description='Parse Naturgy Consumption Excel File.')
arg_parser.add_argument('filename', type=str, help='Excel filename to parse (including extension)')
arg_parser.add_argument('--server', type=str, help='IP of the DB Server (default: localhost)', default='localhost')
arg_parser.add_argument('--user', type=str, help='Username for the DB')
arg_parser.add_argument('--pwd', type=str, help='Password for the DB')
arg_parser.add_argument('--db', type=str, help='Name of the DB', default='power')

args = arg_parser.parse_args()

# Get file from arguments
file = args.filename

log.debug('"' + file + '": Processing...')


if ((not file.endswith('.xls')) and (not file.endswith('xlsx'))):
    print('Invalid file format (.xls/.xlsx required)')
    log.error('Invalid file format (.xls/.xlsx required), Filename: ' + file)
    exit(-1)
    
    
# Parse the file
[retCode, data_s] = parse_naturgy_bill(file)

if (retCode != 0):
    log.debug('Failed Parse, retCode = ' + str(retCode))
    exit(-2)
    
# Store data into the DB
if (retCode == 0):
    
    log.debug('Parsed complete! Saving data into Database...')
    log.debug('Args: ')
    log.debug('server: ' + args.server)
    log.debug('user: ' + args.user)
    log.debug('pwd: ' + args.pwd)
    log.debug('db: ' + args.db)
    retCode = store_data(data_s, args.server, args.user, args.pwd, args.db)

    if (retCode != 0):
        log.debug('Failed Saving data into DB, retCode = ' + str(retCode))
        exit(-3)
        
    else:
        log.debug('Operation completed for ' + file)
        exit(0)
    
          

