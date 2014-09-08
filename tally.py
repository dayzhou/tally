#!/usr/bin/env python3
# coding=utf-8
r"""

Author : Da Zhou
Email  : day.zhou.free@gmail.com

Copyright (c) 2014, Da Zhou.
License: MIT
"""

import sys, os
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
@bot.route( '/python' )
def python_version() :
    return sys.version

# =============================================
@bot.route( '/' )
@bot.route( '/record' )
def record() :
    return bot.template( 'tally',
        operation = 'RECORD'
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
    bot.debug( True )
    bot.run( host='localhost', port=50001, reloader=True )
