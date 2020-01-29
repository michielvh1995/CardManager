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



# TODO:
* Rewrite database logic in C/C++

## Python TODO:
### Tier 1:
  * Allow for return values for queries
  * Allow for searching for a value for a field
  * Allow for subsetting on rows
  * Save databases/tables on the harddrive
  * Load databases from a file
  * Look into list-reordering prevention (or if this is even a thing)

### Tier 2:
  * Data types!
  * Append database files without having to load the entire DB (might/will be broken with encryption)
  * Make it into a deamon
  * Refactoring the SQL interpretation out of the main class

### Tier 3:
  * Graphical interface
  * Blob datatype
  * Encryption
