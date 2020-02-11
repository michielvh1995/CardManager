# A simple database manager with a graphical tool

## Database:
The database in use will be a simple in-house database engine

## The UI
The UI will be provided by the tkinter package

##

----
## How the DB works:
idk yet

Encrypted skiplist & hashtable?

![Class graph]()


# Changelog:
Version 0.1.6.c:
* Now has full support for 3 data types: INT/FLOAT/TEXT
* Further refactoring
  - Less dependencies for SQLInterpreter
  - SQLInterpreter now has a proper structure and responses
* WHERE clauses are broken

Version 0.1.6b:
* Now Supports CREATE TABLE queries

Version 0.1.6a:
* Databases can now be exported as SQL files

Version 0.1.5:
* Moved Table to seprate file
* Implemented TypedTable: a Table that supports type constraints
* Implemented TypedDataBase: the database now supports type constraints
* TODO: actually convert SQL (string) to types (i.e. date/int)
* TODO: rewrite the SQLInterpreter

Version 0.1.4:
* Changed how SQLresponses work
* Changed how DBErrors work
* Most of the code now uses the new format
* Fixed bugs that the database was not properly imported

Version 0.1.3:
* Updated how WHERE works. Still only supports filtering on 1 field

Version 0.1.2:
* Added support for WHERE clauses
  - Currently at most 1 field can be filtered on
* Generalized SQL responses

Version 0.1.1:
* Added SELECT queries
* Added an ERROR class
* Bug fixes:
  - Now removes \" and \' from fieldnames


# TODO:
* Rewrite database logic in C/C++
* Refactor the SQLResponse to make better use of WHERE

## Python TODO (NEW!):
### Tier 1:
  * Refactor SQLInterpreter to handle types better
  * Convert string to types (see previous point)
  * Allow WHERE to query on inequals (>, <, etc.)
  * Loading and storing of a database
  * Have strings keep their spaces and allow for escaped characters (\' => ')
  * Filestoring:
    - Import database from SQL file

### Tier 2:
  * Store the database as a file on the PC that allows for data "streaming"


## Python TODO:
### Tier 1:
  * Allow for return values for queries
  * Save databases/tables on the harddrive
  * Load databases from a file
  * Look into list-reordering prevention (or if this is even a thing)

### Tier 2:
  * Data types!
  * Append database files without having to load the entire DB (might/will be broken with encryption)
  * Make it into a deamon

### Tier 2.5:
  * Data constraints
  * MAX/MIN values
  * Sorting: ORDER/GROUP BY

### Tier 3:
  * Graphical interface
  * Blob datatype
  * Encryption

### Tier 4:
  * Foreign constraints.
  * JOINs
