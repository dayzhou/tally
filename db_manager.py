#! /usr/bin/env python3
# coding=utf-8

import sys, os
import cmd
import sqlite3

########################################## My Connection and Cursor class

class TallyCursor( sqlite3.Cursor ) :
    """Cursor object specially for tally database tables
    """
    def create_default_values_table( self ) :
        KeysValues = (
            ('currency', '1'),
            ('rows_in_1_insertion', '1'),
        )
        self.execute( 'DROP TABLE IF EXISTS default_values' )
        self.execute( 'CREATE TABLE default_values( \
            key TEXT UNIQUE, \
            value TEXT )' \
        )
        self.executemany( "INSERT INTO default_values VALUES(?,?)", KeysValues )

    def create_tally_table( self ) :
        self.execute( 'DROP TABLE IF EXISTS tally' )
        self.execute( "CREATE TABLE tally( \
            talid INTEGER PRIMARY KEY, \
            date DATE DEFAULT ( strftime('%Y-%m-%d','now','localtime') ), \
            ware TEXT, \
            currency INT, \
            cost REAL, \
            remark TEXT DEFAULT NULL )" \
        )

    def create_currencies_table( self ) :
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
        self.execute( 'DROP TABLE IF EXISTS currencies' )
        self.execute( 'CREATE TABLE currencies( \
            curid INTEGER PRIMARY KEY, \
            name TEXT NOT NULL UNIQUE, \
            symbol TEXT NOT NULL UNIQUE, \
            html TEXT NOT NULL UNIQUE, \
            unicode TEXT NOT NULL UNIQUE, \
            description TEXT NOT NULL UNIQUE)' \
        )
        self.executemany( 'INSERT INTO currencies VALUES(?,?,?,?,?,?)', currencies )

    def create_all_tables( self ) :
        self.create_default_values_table()
        self.create_currencies_table()
        self.create_tally_table()

    def insert_into_currencies_table( self, name, symbol, html, uni, desc ) :
        try :
            self.execute( 'INSERT INTO currencies(name, symbol, html, unicode, description) \
                VALUES(?,?,?,?,?)', (name,symbol,html,uni,desc) \
            )
            return True
        except sqlite3.IntegrityError :
            return False

    def insert_into_default_values_table( self, key, value ) :
        self.execute( 'INSERT INTO default_values VALUES(?,?)', (key,value) )

    def insert_into_tally_table( self, row=None, date='', ware='', currency=1, cost=0, remark='' ) :
        if row :
            date = row.date
            ware = row.ware
            currency = row.currency
            cost = row.cost
            remark = row.remark
        
        if date :
            self.execute( 'INSERT INTO tally(date,ware,currency,cost,remark) \
                VALUES(?,?,?,?,?)', (date,ware,currency,cost,remark) \
            )
        else :
            self.execute( 'INSERT INTO tally(ware,currency,cost,remark) \
                VALUES(?,?,?,?)', (ware,currency,cost,remark) \
            )

    def get_from_default_values_table( self, key ) :
        self.execute( 'SELECT value FROM default_values WHERE key=?', (key,) )
        value = self.fetchone()
        if value :
            return value[0]
        else :
            return None

    def get_from_currencies_table( self, *what ) :
        self.execute( 'SELECT %s FROM currencies' % ','.join( what ) )
        return self.fetchall()

    def get_monthly_data_from_tally_table( self, date ) :
        self.execute( 'SELECT date,ware,html,cost,remark \
            FROM tally JOIN currencies ON tally.currency=currencies.curid \
            WHERE date LIKE "%s%%" \
            ORDER BY date DESC' % date
        )
        return self.fetchall()

    def get_monthly_income_from_tally_table( self, date ) :
        self.execute( 'SELECT html,sum(cost) \
            FROM tally JOIN currencies ON tally.currency=currencies.curid \
            WHERE date LIKE "%s%%" AND cost<0 \
            GROUP BY currency' % date
        )
        return self.fetchall()

    def get_monthly_expenses_from_tally_table( self, date ) :
        self.execute( 'SELECT html,sum(cost) \
            FROM tally JOIN currencies ON tally.currency=currencies.curid \
            WHERE date LIKE "%s%%" AND cost>0 \
            GROUP BY currency' % date
        )
        return self.fetchall()

    def get_monthly_balance_from_tally_table( self, date ) :
        self.execute( 'SELECT html,sum(cost) \
            FROM tally JOIN currencies ON tally.currency=currencies.curid \
            WHERE date LIKE "%s%%" \
            GROUP BY currency' % date
        )
        return self.fetchall()

    def get_minimal_year( self ) :
        self.execute( 'SELECT min(date) FROM tally' )
        date = self.fetchone()[0]
        if date :
            return int( date[:4] )
        else :
            return None
    
    def update_default_values_table( self, key, value ) :
        self.execute( 'UPDATE default_values SET value=? WHERE key=?', (value,key) )

    def delete_from_currencies_table( self, curid ) :
        self.execute( 'DELETE FROM currencies WHERE curid=?', (curid,) )


def get_tally_connection( DBFile ) :
    return sqlite3.connect( DBFile )

########################################## Table row classes

class Currency :
    """The currency class, collecting information about one kind of currency
    """
    def __init__( self, curid=0, name='' ) :
        if curid :
            _cursor.execute( 'SELECT * FROM currencies WHERE curid=?', (curid,) )
            currency = _cursor.fetchall()
        elif name :
            _cursor.execute( 'SELECT * FROM currencies WHERE name=?', (name,) )
            currency = _cursor.fetchall()

        if currency :
            self.curid, self.name, self.symbol, self.html, \
                self.unicode, self.description = currency[0]
            self.existence = True
        else :
            self.existence = False

##########################################

class _TallyCmd ( cmd.Cmd ) :
    """Command line tools"""

    def __init__ ( self, cursor ) :
        cmd.Cmd.__init__ ( self )
        self.prompt = '  <Tally> '
        self.cursor = cursor
    
    def _exit( self ) :
        self.cursor.close()
        return True
    
    def do_call( self, args ) :
        """Call any function you want and return the result of that function
        """
        if args :
            func = args.split( ' ' )[0]
            arguments = ','.join( args.split( ' ' )[1:] )
            print( eval( func+'('+arguments+')' ) )

    def do_CreateTable( self, args ) :
        """Create some specific table you want.
        * CreateTable currencies
            create "currencies" table
        * CreateTable tally
            create "tally" table
        * CreateTable default_values
            create "default_values" table
        * CreateTable all
            create all above 3 tables
        """
        if args == 'currencies' :
            self.cursor.create_currencies_table()
            print( 'Table "currencies" is created.' )
        elif args == 'tally' :
            self.cursor.create_tally_table()
            print( 'Table "tally" is created.' )
        elif args == 'default_values' :
            self.cursor.create_default_values_table()
            print( 'Table "default_values" is created.' )
        elif args == 'all' :
            self.cursor.create_all_tables()
            print( 'All 3 tables "default_values",' \
                '"tally" and "currencies" are created.' )

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
        """Run a shell command by preposing an exclamation mark.
        e.g., run the "ls" command:
        ! ls
        """
        self.last_output = os.popen( args ).read()
        print( '\n'+self.last_output )

    def do_exit ( self, args ) :
        """Quit session
        """
        return self._exit()

    def do_EOF( self, args ) :
        """Quit by pressing <CTRL>+D
        """
        return self._exit()

##########################################

if __name__ == '__main__' :
    with get_tally_connection( 'tally.db' ) as _conn :
        _TallyCmd( _conn.cursor( TallyCursor ) ).cmdloop()
