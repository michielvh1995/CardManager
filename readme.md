# A simple database manager with a graphical tool

## Database:
The database in use will be a simple in-house database engine

## The UI
The UI will be provided by the tkinter package

##

----
## How the DB works:
idk yet

Encrypted skiplist & hashtable

![Class graph]()


# Changelog:
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
  * Refactoring the SQL interpretation out of the main class

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
