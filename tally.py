#!/usr/bin/env python3
# coding=utf-8
r"""
This is an online running tally application.

Author : Da Zhou
Email  : day.zhou.free@gmail.com

Copyright (c) 2014, Da Zhou.
License: MIT
"""

import sys
import os
import re
import datetime as dt
import bottle as bot
from db_manager import *

# =============================================
__version__ = '0.1'
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
    """Input row class, contains 6 fields:
        "date"     : date on which money are spent
        "ware"     : the ware the money is spent for
        "currency" : currency (money)
        "cost"     : money the ware costs
        "remark"   : notes for memo
        "msg"      : message for invalid input
    """
    def __init__( self, date='', ware='', currency=1, cost='', remark='' ) :
        today = dt.date.today()
        self.date = date or '%d-%02d-%02d' % (today.year,today.month,today.day)
        self.ware = ware
        self.currency = currency
        self.cost = cost
        self.remark = remark
        self.msg = {'date':'', 'ware':'', 'cost':'', 'remark':''}
        self.is_empty = False
    
    def check_and_format( self ) :
        if not self.ware :
            self.is_empty = True
            return True

        evalidate = True
        
        if len( self.ware ) > 30 :
            self.msg['ware'] = u'商品名称不应超过30字符'
            evalidate = False

        if len( self.remark ) > 50 :
            self.msg['remark'] = u'备忘内容不应超过50字符'
            evalidate = False
        
        try :
            self.cost = float( self.cost )
        except ValueError :
            self.msg['cost'] = u'金额必须是一个数'
            evalidate = False

        try :
            ymd = [ int(x) for x in self.date.split('-') ]
            if dt.date( *ymd ) > dt.date.today() :
                self.msg['date'] = u'不能填写未来的日期'
                evalidate = False
            else :
                self.date = str( dt.date( *ymd ) )
        except ValueError :
            self.msg['date'] = u'错误的日期格式'
            evalidate = False
        
        return evalidate


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
    CurYear = dt.date.today().year
    if MinYear :
        return [ str(y) for y in range( MinYear, CurYear+1 ) ]
    else :
        return [ CurYear ]

# =============================================
@bot.route( '/' )
@bot.route( '/record' )
def record() :
    InputRows = get_default_number_of_rows_in_1_insertion() * \
        [ CInputRow( currency=get_default_currency() ) ]
    
    return bot.template( 'tally',
        operation = 'RECORD',
        AllCurrencies = get_currencies_list(),
        InputRows = InputRows,
    )


@bot.post( '/record' )
def post_record() :
    InputRows = [
        CInputRow(
            date = '-'.join(
                [ bot.request.forms.get( '%s%d' % (x,i) )
                    for x in ('year','month','day') ]
            ),
            ware = bot.request.forms.get( 'ware%d' % i ),
            currency = int( bot.request.forms.get( 'currency%d' % i ) ),
            cost = bot.request.forms.get( 'cost%d' % i ),
            remark = bot.request.forms.get( 'remark%d' % i ),
        )
        for i in range( get_default_number_of_rows_in_1_insertion() )
    ]
    
    if False in [ row.check_and_format() for row in InputRows ] :
        return bot.template( 'tally',
            operation = 'RECORD',
            AllCurrencies = get_currencies_list(),
            InputRows = InputRows,
        )
    else :
        for row in [ x for x in InputRows if not x.is_empty ] :
            cursor.insert_into_tally_table( row=row )
        bot.redirect( '/view' )


@bot.route( '/view' )
@bot.route( '/view/<date:re:20[0-9][0-9]-(0[1-9]|1[0-2])>' )
def view( date=None ) :
    if not date :
        today = dt.date.today()
        date = '%d-%02d' % ( today.year, today.month )

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


@bot.route( '/settings' )
def settings() :
    return bot.template( 'tally',
        operation = 'SETTINGS',
        AllCurrencies = get_currencies_list(),
        currency = get_default_currency(),
        num_of_rows = get_default_number_of_rows_in_1_insertion(),
    )


@bot.post( '/settings/default_currrency' )
def post_settings() :
    pass

@bot.post( '/settings/num_of_rows' )
def post_settings() :
    number = bot.request.forms.get( 'num_of_rows' )
    cursor.update_default_values_table( 'rows_in_1_insertion', str(number) )
    bot.redirect( '/record' )

@bot.post( '/settings/add_currrency' )
def post_settings() :
    pass

# =============================================
if __name__ == '__main__' :
    DBExistence = os.path.exists( __DB_PATH__ )
    with get_tally_connection() as conn :
        cursor = conn.cursor( TallyCursor )
        if not DBExistence :
            cursor.create_all_tables()
        bot.debug( True )
        bot.run( host='localhost', port=50001, reloader=True )
