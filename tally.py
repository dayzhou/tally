#!/usr/bin/env python3
# coding=utf-8
r"""

Author : Da Zhou
Email  : day.zhou.free@gmail.com

Copyright (c) 2014, Da Zhou.
License: MIT
"""

import sys
import os
#import sqlite3
from datetime import datetime
import bottle as bot
from db_manager import *

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
    """Currency class, contains valuesof 2 fields:
        "curid"       : currency id
        "html"        : the html code of the currency symbol
    """
    def __init__( self, ct ) :
        self.curid = ct[0]
        self.html = ct[1]


class CTally :
    """Tally class, contains valuesof 4 fields:
        "date"   : date
        "ware"   : the ware the money is spent for
        "cost"   : money the ware costs
        "remark" : notes for memo
    """
    def __init__( self, tt ) :
        self.date = tt[0]
        self.ware = tt[1]
        self.cost = '%s %d' % ( tt[2], tt[3] )
        self.remark = tt[4]


class CTotalTally :
    """Total tally class, contains only 1 fields : "cost"
    """
    def __init__( self, ttt ) :
        self.cost = '%s %d' % ( ttt[0], ttt[1] )


class CInputRow :
    """Input row class, contains 5 fields:
        "date"     : date on which money are spent
        "ware"     : the ware the money is spent for
        "currency" : currency (money)
        "cost"     : money the ware costs
        "remark"   : notes for memo
    """
    def __init__( self, date='', ware='', currency=1, cost=0, remark='' ) :
        self.date = date
        self.ware = ware
        self.currency = currency
        self.cost = cost
        self.remark = remark


def get_default_number_of_rows_in_1_insertion() :
    try :
        return int( cursor.get_from_default_values_table( 'rows_in_1_insertion' ) )
    except :
        return 5


def get_default_currency() :
    try :
        return int( cursor.get_from_default_values_table( 'currency' ) )
    except :
        return 1


def get_currencies_list() :
    return [ CCurrency(curr) for curr in \
        cursor.get_from_currencies_table( 'curid', 'html' ) ]


def get_tally_list( date ) :
    return [ CTally(row) for row in cursor.get_from_tally_table(date) ]


def get_total_tally_list( date ) :
    return [ CTotalTally(row) for row in \
        cursor.group_get_from_tally_table(date) ]


def get_all_years() :
    MinYear = cursor.get_minimal_year()
    CurYear = datetime.now().year
    if MinYear :
        return [ str(y) for y in range( MinYear, CurYear+1 ) ]
    else :
        return [ CurYear ]

# =============================================
@bot.route( '/' )
@bot.route( '/record' )
def record() :
    return bot.template( 'tally',
        operation = 'RECORD',
        num_of_rows = get_default_number_of_rows_in_1_insertion(),
        currency = get_default_currency(),
        AllCurrencies = get_currencies_list(),
    )


@bot.post( '/record' )
def post_record() :
    InputRows = [
        CInputRow(
            ware = bot.request.forms.get( 'ware%d' % i ),
            currency = bot.request.forms.get( 'currency%d' % i ),
            cost = bot.request.forms.get( 'cost%d' % i ),
            remark = bot.request.forms.get( 'remark%d' % i )
        ) for i in range( get_default_number_of_rows_in_1_insertion() )
    ]
    for row in InputRows :
        cursor.insert_into_tally_table( row=row )
    bot.redirect( '/view' )


@bot.route( '/view' )
@bot.route( '/view/<date:re:20[0-9][0-9]-(0[1-9]|1[0-2])>' )
def view( date=None ) :
    if not date :
        now = datetime.now()
        date = '%d-%02d' % ( now.year, now.month )

    return bot.template( 'tally',
        operation = 'VIEW',
        year = date[:4],
        month = date[-2:],
        AllYears = get_all_years(),
        TallyRows = get_tally_list( date ),
        TotalTallyRows = get_total_tally_list( date ),
    )


@bot.post( '/view' )
def post_view() :
    year = bot.request.forms.get( 'year' )
    month = bot.request.forms.get( 'month' )
    bot.redirect( '/view/%s-%s' % (year,month) )

# =============================================
if __name__ == '__main__' :
    DBExistence = os.path.exists( __DB_PATH__ )
    with get_tally_connection() as conn :
        cursor = conn.cursor( TallyCursor )
        if not DBExistence :
            cursor.create_all_tables()
        bot.debug( True )
        bot.run( host='localhost', port=50001, reloader=True )