#!/usr/bin/env python3

##
# @file db_connector.py
# @issue 1.0
# @last 20210617
# @user cavt
#
# @brief Connector for the POWER db. Input data in JSON.
# This script will take data in JSON format and upload it to the POWER DB

# @version v1.0 | 20210617 | cavt | 
# Initial version
# @version v1.1 | 20210915 | cavt |
# Just add return code when DB operation fails
#
# Imports
#
#import MySQLdb
import json
import pymysql
import sys
from datetime import date
import logging as log

# Configure logging file
#log.basicConfig(filename='/var/log/volt/volt.log', encoding='utf-8', level=log.DEBUG, format='%(asctime)-15s %(levelname)-8s %(message)s')

#
# Private functions
#


#
# Public functions
#
def store_data(j_file, server, user, passwd, db):
    """
    This function will take a JSON file and will upload it to the
    POWER DB
    
    :param j_file: JSON input file
    :param server: IP of the DB server
    :param user: User for the access to the DB
    :param passwd: Password
    :param db: Name of the db
    :return: Error code
    """

    # Connection to DB
    try:
        
        # Stablish connection with the DB
        db = pymysql.connect(server, user, passwd, db)
        
        # Initialize the cursor
        dbcursor = db.cursor()
    
    except:
        log.error("[%s] DB_ERROR: Fail in the connection to the Database" % st_tic)
        log.debug("DB_ERROR: Fail in the connection to the Database")
        return(-1)

    
    # Unserialize the JSON
    data = json.loads(j_file)

    aa_Data = []
    
    # Prepare data
    for row in range(0, len(data['data'])):
        aa_Data.append([data['data'][row]['date'], data['data'][row]['timefrom'], data['data'][row]['timeto'], data['data'][row]['type'], data['data'][row]['consumption'], data['data'][row]['price'], data['bill'], data['cups']])

    # Prepare SQL entry
    sql_insert = "INSERT INTO data (`date`, `timefrom`, `timeto`, `type_id`, `consumption`, `price`, `bill`, `cups`) VALUES (STR_TO_DATE(%s, '%%d/%%m/%%Y'), %s, %s, %s, %s, %s, %s, %s)"

#    log.debug('----------------- sql_insert ---------------')
#    log.debug(sql_insert)
#    log.debug('--------------------------------------------')
#    log.debug('------------------ aa_Data -----------------')
#    log.debug(aa_Data)
#    log.debug('--------------------------------------------')

    try:

        # several entries at once (run the query)
        dbcursor.executemany(sql_insert, aa_Data)

        # Commit the operation
        db.commit()

    except:
        log.debug('Exception!!!')
        e = sys.exc_info()[0]
        log.debug("<p>Error: %s</p>:" % e)
        db.rollback()
        return(-2)
    
    # Close Database
    db.close()    

    # Everything was ok
    log.debug('Everything was OK with the DB')
    return(0)


    




