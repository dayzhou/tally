#!/usr/bin/env python3
# coding=utf-8
r"""

Author : Da Zhou
Email  : day.zhou.free@gmail.com

Copyright (c) 2014, Da Zhou.
License: MIT
"""

import sys, os
import sqlite3
import bottle as bot
from cmd_tally import *

# =============================================
__version__ = '0.0'
__license__ = 'MIT'

# =============================================
__SRC_DIR__  = os.path.dirname( __file__ )
__DB_PATH__  = os.path.join( __SRC_DIR__, 'tally.db' )
#__CSS_PATH__ = os.path.join( __SRC_DIR__, 'tally.css' )
#__TPL_PATH__ = os.path.join( __SRC_DIR__, 'tally.tpl' )

# =============================================
class CCurrency :
    """Currency Class, contains valuesof 3 fields:
        "name"        : name of the currency
        "html"        : the html code of the currency symbol
        "is_selected" : 'selected' if it is the default currency,
                        '' otherwise
    """
    def __init__( self, ct, dc ) :
        self.curid = ct[0]
        self.html = ct[1]
        self.is_selected = {True:'selected', False:''}[ct[0]==dc]


def get_default_number_of_rows_in_1_insertion() :
    try :
        return int( get_from_default_values_table( cursor, 'rows_in_one_insertion' ) )
    except :
        return 5


def get_default_currency() :
    try :
        return int( get_from_default_values_table( cursor, 'currency' ) )
    except :
        return 1


def get_currencies_list() :
    DefCurr = get_default_currency()
    CurrenciesTupple = get_from_currencies_table( cursor, 'curid', 'html' )
    CurrenciesList = []
    for currency in CurrenciesTupple :
        CurrenciesList.append( CCurrency(currency,DefCurr) )
    return CurrenciesList

# =============================================


# =============================================
@bot.route( '/' )
@bot.route( '/record' )
def record() :
    return bot.template( 'tally',
        operation = 'RECORD',
        num_of_rows = get_default_number_of_rows_in_1_insertion(),
        currencies = get_currencies_list(),
    )


@bot.route( '/view' )
def view() :
    return bot.template( 'tally',
        operation = 'VIEW'
    )


@bot.post( '/insert' )
def insert() :
    return


@bot.post( '/select' )
def select() :
    return

# =============================================
if __name__ == '__main__' :
    conn = sqlite3.connect( __DB_PATH__ )
    cursor = conn.cursor()
    bot.debug( True )
    bot.run( host='localhost', port=50001, reloader=True )
