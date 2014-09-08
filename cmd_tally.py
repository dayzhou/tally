#! /usr/bin/env python3
# coding=utf-8

import sys, os
import cmd
import sqlite3


########################################## Create Tables

def create_default_values_table( cur ) :
    cur.execute( 'DROP TABLE IF EXISTS default_values' )
    cur.execute( 'CREATE TABLE default_values( \
        key TEXT UNIQUE, \
        value TEXT )' \
    )
    cur.execute( "INSERT INTO default_values VALUES('currency','1')" )


def create_tally_table( cur ) :
    cur.execute( 'DROP TABLE IF EXISTS tally' )
    cur.execute( "CREATE TABLE tally( \
        talid INTEGER PRIMARY KEY, \
        ware TEXT, \
        cost REAL, \
        currency INT, \
        remark TEXT, \
        date DATE DEFAULT ( date('now','localtime') ) )" \
    )


def create_currencies_table( cur ) :
    currencies = (
        ( 1,  'CNY', u'CNY¥', 'CNY&#165;', r'CNY\xA5', 'China Yuan' ),
        ( 2,  'GBP', u'£',    '&#163;',    r'\xA3',    'Great Britain Pound' ),
        ( 3,  'USD', u'$',    'U.S.&#36;', r'U.S.$',   'U.S. Dollar' ),
        ( 4,  'ECU', u'€',    '&#8364;',   r'\u20AC',  'European Currency Unit' ),
        ( 5,  'HKD', u'HK$',  'HK&#36;',   r'HK$',     'Hong Kong Dollar' ),
        ( 6,  'NTD', u'NT$',  'NT&#36;',   r'NT$',     'New Taiwan Dollar' ),
        ( 7,  'JPY', u'JPY¥', 'JPY&#165;', r'JPY\xA5', 'Japanese Yen' ),
        ( 8,  'KOW', u'₩',    '&#8361;',   r'\u20A9',  'Korea Won' ),
        ( 9,  'CAD', u'Can$', 'Can&#36;',  r'Can$',    'Canada Dollar' ),
        ( 10, 'AUD', u'A$',   'A&#36;',    r'A$',      'Australia Dollar' ),
    )
    cur.execute( 'DROP TABLE IF EXISTS currencies' )
    cur.execute( 'CREATE TABLE currencies( \
        curid INTEGER PRIMARY KEY, \
        name TEXT NOT NULL UNIQUE, \
        symbol TEXT NOT NULL UNIQUE, \
        html TEXT NOT NULL UNIQUE, \
        unicode TEXT NOT NULL UNIQUE, \
        description TEXT NOT NULL UNIQUE)' \
    )
    cur.executemany( 'INSERT INTO currencies VALUES(?,?,?,?,?,?)', currencies )

########################################## Table row classes

class Currency :
    """The currency class, collecting information about one kind of currency
    """
    def __init__( self, cursor, curid=0, name='' ) :
        if curid :
            cursor.execute( 'SELECT * FROM currencies WHERE curid=?', (curid,) )
            currency = cursor.fetchall()
        elif name :
            cursor.execute( 'SELECT * FROM currencies WHERE name=?', (name,) )
            currency = cursor.fetchall()

        if currency :
            self.curid, self.name, self.symbol, self.html, \
                self.unicode, self.description = currency[0]
            self.existence = True
        else :
            self.existence = False

def insert_into_currencies_table( cur, name, symbol, html, uni, desc ) :
    cur.execute( 'INSERT INTO currencies(name, symbol, html, uni, desc) \
        VALUES(?,?,?,?,?)', (name,symbol,html,uni,desc) \
    )


def insert_into_default_values_table( cur, key, value ) :
    cur.execute( 'INSERT INTO default_values VALUES(?,?)', (key,value) )


def insert_into_tally_table( cur, ware, cost, currency, remark='', date='' ) :
    if date :
        cur.execute( 'INSERT INTO tally(ware,cost,currency,remark,date) \
            VALUES(?,?,?,?,?)', (ware,cost,currency,remark,date) \
        )
    else :
        cur.execute( 'INSERT INTO tally(ware,cost,currency,remark) \
            VALUES(?,?,?,?)', (ware,cost,currency,remark) \
        )

##########################################

class _TallyCmd ( cmd.Cmd ) :
    """Command line tools"""

    def __init__ ( self, cursor, **karg ) :
        cmd.Cmd.__init__ ( self )
        self.prompt = '  <Tally> '
        self.cursor = cursor

    def do_CreateTable( self, args ) :
        if args == 'currencies' :
            create_currencies_table( self.cursor )
            print( 'Table "currencies" created' )
        elif args == 'tally' :
            create_tally_table( self.cursor )
            print( 'Table "tally" created' )
        elif args == 'default_values' :
            create_default_values_table( self.cursor )
            print( 'Table "default_values" created' )

    def do_prompt( self, args ) :
        """ Change interactive prompt :
        the quotation marks " and ' as the first or last character are omitted,
        e.g., try to type (and see what you will get):
        prompt "'Tally> '
        """
        if args :
            if args[0] in ('"', "'") :
                args = args[1:]
            if args and args[-1] in ('"', "'") :
                args = args[:-1]
            self.prompt = args

    def do_shell( self, args ):
        """Run a shell command by preposing an exclamation mark:
        ! ls
        """
        self.last_output = os.popen( args ).read()
        print( '\n'+self.last_output )

    def do_exit ( self, args ) :
        """Quit session
        """
        return True

    def do_EOF( self, args ) :
        """Quit by pressing <CTRL>+D
        """
        return True

##########################################

if __name__ == '__main__' :
    with sqlite3.connect( 'tally.db' ) as conn :
        _TallyCmd( conn.cursor() ).cmdloop()
