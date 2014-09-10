## Tally: Record Your Incomes and Expenses

- - -

Tally is a _**web-based**_ program for recording everyday incomes and expenses. The underlying web engine is _[Bottle](http://bottlepy.org)_ which is a _Python_ web framework.

- - -

### Installation

1. Download the zip file and unzip it

2. Open a terminal in the unzipped directory

3. Type command:  
    > $python3 tally.py
   
    It will create a _sqlite_ database file "_tally.db_" at **first run**

4. Open a web browser, type in the url:
    > http://localhost:50001/

5. You will see the web pages

- - -

### About files

* _README.md_
    * The file you are reading

* _tally.py_
    * The **main** program that acts as the backend of the application
    * All database operations that are engine relevant are defined in the file "_db_manager.py_" so that "_tally.py_" only uses the abstract database connection cursor to manipulate the database which is **engine irrelevant**
    * That also means it needs to import classes and functions from "_db_manager_"

* _db_manager.py_
    * A **command line tool** for manipulating the database "_tally.db_"  
    * Also as a library imported by "_tally.py_"
    * Hack it yourself

* _tally.tpl_
    * The **template** file using the default "_bottle.py_" template engine

* _tally.css_
    * The CSS file imported as a subtemplate by "_tally.tpl_"

* _CHANGELOG.md_
    * Change history file and also a **todo** list

* _LICENSE_
    * The _MIT_ License details

- - -

### License

The code is available according to the MIT License (see LICENSE).