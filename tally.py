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
from functools import wraps
from db_manager import *

# =============================================

__version__ = '0.2'
__license__ = 'MIT'

# =============================================

__SRC_DIR__  = os.path.dirname( __file__ )
__DB_PATH__  = os.path.join( __SRC_DIR__, 'tally.db' )
#__CSS_PATH__ = os.path.join( __SRC_DIR__, 'tally.css' )
__TEMPLATE__ = os.path.join( __SRC_DIR__, 'tally' )

if not os.path.exists( __DB_PATH__ ) :
    with get_tally_connection( __DB_PATH__ ) as conn :
        conn.cursor( TallyCursor ).create_all_tables()

# =============================================

def DBOperator( func ) :
    """ A function decorator that sets initial connection to the
        DB for further operation in the decorated functions
    """
    @wraps( func )
    def __DBOperator( *args, **kws ) :
        with get_tally_connection( __DB_PATH__ ) as conn :
            result = func( conn.cursor( TallyCursor ), *args, **kws )	
        return result
    return __DBOperator

# =============================================

class CCurrency :
    """Currency class, contains a dict 'members' which may have keys:
        "curid", "name", "symbol", "html", "unicode", "description"
    """
    def __init__( self, **members ) :
        self.members = members
        self.msg = ''
    
    def check( self ) :
        keys = self.members.keys()
        for key in ( 'name', 'symbol', 'html', 'uni', 'desc' ) :
            if key not in keys :
                return False
            elif not self.members[key] :
                return False
        return True


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
        self.cost = '%s %g' % ( tt[2], tt[3] )
        self.remark = tt[4]


class CTotalTally :
    """Total tally class, contains only 1 fields : "cost"
    """
    def __init__( self, ttt ) :
        self.cost = '%s %g' % ( ttt[0], ttt[1] )


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

# =============================================

@DBOperator
def get_default_number_of_rows_in_1_insertion( cursor ) :
    try :
        return int( cursor.get_from_default_values_table( 'rows_in_1_insertion' ) )
    except :
        return 5


@DBOperator
def get_default_currency( cursor ) :
    try :
        return int( cursor.get_from_default_values_table( 'currency' ) )
    except :
        return 1


@DBOperator
def get_currencies_list( cursor ) :
    return [ CCurrency( curid=i, html=h ) for i,h in \
        cursor.get_from_currencies_table( 'curid', 'html' ) ]


@DBOperator
def get_monthly_tally_list( cursor, date ) :
    return [ CTally(row) for row in \
        cursor.get_monthly_data_from_tally_table(date) ]


@DBOperator
def get_monthly_income_tally_list( cursor, date ) :
    return [ CTotalTally(row) for row in \
        cursor.get_monthly_income_from_tally_table(date) ]


@DBOperator
def get_monthly_expenses_tally_list( cursor, date ) :
    return [ CTotalTally(row) for row in \
        cursor.get_monthly_expenses_from_tally_table(date) ]


@DBOperator
def get_monthly_balance_tally_list( cursor, date ) :
    return [ CTotalTally(row) for row in \
        cursor.get_monthly_balance_from_tally_table(date) ]


@DBOperator
def get_all_years( cursor ) :
    MinYear = cursor.get_minimal_year()
    CurYear = dt.date.today().year
    if MinYear :
        return [ str(y) for y in range( MinYear, CurYear+1 ) ]
    else :
        return [ CurYear ]


@DBOperator
def update_default_values_table( cursor, key, value ) :
    cursor.update_default_values_table( key, value )


@DBOperator
def insert_into_currencies_table( cursor, members ) :
    return cursor.insert_into_currencies_table( **members )


@DBOperator
def delete_from_currencies_table( cursor, currency ) :
    cursor.delete_from_currencies_table( currency )


@DBOperator
def insert_into_tally_table( cursor, row ) :
    cursor.insert_into_tally_table( row=row )

# =============================================

@bot.route( '/' )
@bot.route( '/record' )
def record() :
    InputRows = get_default_number_of_rows_in_1_insertion() * \
        [ CInputRow( currency=get_default_currency() ) ]
    
    return bot.template( __TEMPLATE__,
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
        return bot.template( __TEMPLATE__,
            operation = 'RECORD',
            AllCurrencies = get_currencies_list(),
            InputRows = InputRows,
        )
    else :
        for row in [ x for x in InputRows if not x.is_empty ] :
            insert_into_tally_table( row )
        bot.redirect( '/view' )


@bot.route( '/view' )
@bot.route( '/view/<date:re:20[0-9][0-9]-(0[1-9]|1[0-2])>' )
def view( date=None ) :
    if not date :
        today = dt.date.today()
        date = '%d-%02d' % ( today.year, today.month )

    return bot.template( __TEMPLATE__,
        operation = 'VIEW',
        year = date[:4],
        month = date[-2:],
        AllYears = get_all_years(),
        TallyRows = get_monthly_tally_list( date ),
        IncomeRows = get_monthly_income_tally_list( date ),
        ExpensesRows = get_monthly_expenses_tally_list( date ),
        BalanceRows = get_monthly_balance_tally_list( date ),
    )


@bot.post( '/view' )
def post_view() :
    year = bot.request.forms.get( 'year' )
    month = bot.request.forms.get( 'month' )
    bot.redirect( '/view/%s-%s' % (year,month) )


@bot.route( '/settings' )
def settings() :
    return bot.template( __TEMPLATE__,
        operation = 'SETTINGS',
        AllCurrencies = get_currencies_list(),
        currency = get_default_currency(),
        num_of_rows = get_default_number_of_rows_in_1_insertion(),
        CurrencyToAdd = CCurrency(name='', symbol='', html='', uni='', desc=''),
    )


@bot.post( '/settings/default_currency' )
def post_settings() :
    number = int( bot.request.forms.get( 'currency' ) )
    update_default_values_table( 'currency', number )
    bot.redirect( '/settings' )


@bot.post( '/settings/num_of_rows' )
def post_settings() :
    number = str( bot.request.forms.get( 'num_of_rows' ) )
    update_default_values_table( 'rows_in_1_insertion', number )
    bot.redirect( '/settings' )


@bot.post( '/settings/add_currency' )
def post_settings() :
    currency2add = CCurrency(
        name = bot.request.forms.get( 'name' ),
        symbol = bot.request.forms.getunicode( 'symbol' ),
        html = bot.request.forms.get( 'html' ),
        uni = bot.request.forms.get( 'unicode' ),
        desc = bot.request.forms.get( 'description' ),
    )
    
    if currency2add.check() :
        if insert_into_currencies_table( currency2add.members ) :
            bot.redirect( '/settings' )
        else :
            currency2add.msg = u'不可与已有货币重复'
    else :
        currency2add.msg = u'所有货币属性不可为空'

    return bot.template( __TEMPLATE__,
        operation = 'SETTINGS',
        AllCurrencies = get_currencies_list(),
        currency = get_default_currency(),
        num_of_rows = get_default_number_of_rows_in_1_insertion(),
        CurrencyToAdd = currency2add,
    )


@bot.post( '/settings/delete_currency' )
def post_settings() :
    currency = int( bot.request.forms.get( 'currency' ) )
    delete_from_currencies_table( currency )
    bot.redirect( '/settings' )

# =============================================
if __name__ == '__main__' :
    bot.debug( True )
    bot.run( host='localhost', port=50001, reloader=True )
