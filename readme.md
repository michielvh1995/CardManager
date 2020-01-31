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
Version 0.1.1:
* Added SELECT queries
* Added an ERROR class
* Bug fixes:
  - Now removes \" and \' from fieldnames


# TODO:
* Rewrite database logic in C/C++

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
  * WHERE clauses
  * MAX/MIN values
  * Sorting: ORDER/GROUP BY

### Tier 3:
  * Graphical interface
  * Blob datatype
  * Encryption

### Tier 4:
  * Foreign constraints.
  * JOINs
