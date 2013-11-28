###
### This code depends on the MySQLdb python library available at
### http://sourceforge.net/projects/mysql-python/
### Unfortunately, this can potentially be irritating to install because you may
### first have to install a c-compiler (usually gcc on the command line).
### However, these are usually pretty straightforward to install.
###

import os
import MySQLdb
import cgitb

IS_SETUP = False;
CONNECTION = None;
INSTANCE = False;

cgitb.enable() # More informative error messages.

def setup(instance):
    """
    Creates a new global variable, CONNECTION, which is a live connection to a
    MySQL database, over which queries can be made.

    @param {String} 'instance' Determines which database is going to be used.
    """
    global INSTANCE
    INSTANCE = instance;
    if instance == "shakespeare":
        database = "wordseer_a"
        username = "wordseer_a"
        password = "wordseer_a"
    elif instance == "acm" :
        database = "wordseer_h"
        username = "wordseer_h"
        password = "wordseer_h"
    ## If you want to use a new instance, put another elif clause here.

    global CONNECTION;
    if not IS_SETUP:
        CONNECTION = MySQLdb.connect(user=username, passwd=password, db=database)

def getCursor():
    """
    Returns a cursor over which SQL queries can be made.
    The default cursor returns a dictionary for each result row, keyed by the
    column name.
    """
    global INSTANCE
    setup(INSTANCE);
    global CONNECTION;
    return CONNECTION.cursor(MySQLdb.cursors.DictCursor)

def commit():
    """
    Do this before ending execution, to make sure that all in-memory changes get
    flushed to the database.
    """
    global CONNECTION;
    CONNECTION.commit();
