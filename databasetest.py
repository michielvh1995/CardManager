from Tools.Database.Database import TypedDataBase
from Tools.Database.FileService import FileService
# ===================================================
# Debugging
# ===================================================

# ---------------------------------------------------------------------------
# Round 2: TypedDatabase
# ---------------------------------------------------------------------------
dbT = TypedDataBase(name = "test")

def InsertTest(tablename):
    print "Create table query with field types:"
    print dbT.Query("CREATE TABLE " + tablename + " (id INT PRIMARY, text TEXT, other TEXT);")
    print

    print "Correct typing:"
    print dbT.Query('INSERT INTO ' + tablename + ' ("id", "text") VALUES (1, "testtext");')
    print dbT.Query('INSERT INTO ' + tablename + ' ("id", "text") VALUES (2, "Met spatie?");')
    print dbT.Query('INSERT INTO ' + tablename + ' ("id", "text") VALUES (3, "Andere text");')
    print dbT.Query('INSERT INTO ' + tablename + ' ("id", "text") VALUES (4, "Incluus cijfers 123");')
    print

    print "Incorrectly typed"
    print dbT.Query('INSERT INTO ' + tablename + ' ("id", "text") VALUES ("a", "testtext");')
    print

def QueryTest(tablename):
    print "SELECT query"
    for i in dbT.Query("SELECT (id, text) FROM " + tablename + ";"):
        print "  " + str(i)
    print

    print "Querying with a WHERE clause"
    for i in dbT.Query("SELECT (id, text) FROM " + tablename + " WHERE id = 1;"):
        print "  " + str(i)
    print

    print "WHERE <="
    for i in dbT.Query("SELECT (id, text) FROM " + tablename + " WHERE id <= 2;"):
        print "  " + str(i)
    print

    print "Querying with a WHERE clause on a TEXT field"
    for i in dbT.Query("SELECT (id, text) FROM " + tablename + " WHERE text = testtext;"):
        print "  " + str(i)
    print

    print "With type errored WHERE clause"
    print dbT.Query("SELECT (id, text) FROM " + tablename + " WHERE id >= h;")
    print

# ---------------------------------------------------------------------------
# Round 3: Filesystems; Files, Files, Files
# ---------------------------------------------------------------------------
def MultilineQueries(tablename):
    print "Single line, with check"
    print dbT.InputSQL('INSERT INTO ' + tablename + ' ("id", "text") VALUES (1, "testtext");')
    print

    print "Incomplete query"
    print dbT.InputSQL('INSERT INTO ' + tablename + ' ("id", "text") VALUES')
    print "   part 2 of query"
    print dbT.InputSQL(' (1, "testtext");')
    print

    print "Comment character in string"
    print dbT.InputSQL("INSERT INTO ' + tablename + ' ('text', 'other', 'id')")
    print dbT.InputSQL(" VALUES ('Nu met nasty -- characters', 'None', '5');")
    print

    # Reset the lasts
    dbT.lastcommand = ""
    print "End query character in string"
    print dbT.InputSQL("INSERT INTO " + tablename + " ('text', 'other', 'id')")
    print dbT.InputSQL(" VALUES ('Nu met nasty ; characters', 'None', '5');")
    print dbT.Query("SELECT (id, text) FROM " + tablename + " WHERE id = 5;")
    print

    # Reset the lasts
    dbT.lastcommand = ""

def ToSQLFile():
    print "Export test, see file exporttest.sql"
    with open("exporttest.sql", "w") as file:
        print dbT.ExportAsSQL(file)
    print

def FromSQLFile():
    print "Import from exporttest.sql file"
    with open("exporttest.sql", "r") as file:
        print dbT.ImportSQL(file)
    print

def FileStore():
    print "Run FileService.OverwriteAll():"
    fs = FileService("filetest.db")
    fs.OverwriteAll(dbT)
    print
    print "retrieving"
    print

    fs.UpdateTable(dbT.tables["typeTest"])

    return fs.Read()

# ---------------------------------------------------------------------------
# Constraints
# ---------------------------------------------------------------------------
def PrimaryTable(tablename):
    print "Create table query with field types:"
    print dbT.Query("CREATE TABLE " + tablename + " (id INT PRIMARY, text TEXT, other TEXT);")
    print

    print "Correct typing:"
    print dbT.Query('INSERT INTO ' + tablename + ' ("id", "text") VALUES (1, "testtext");')
    print dbT.Query('INSERT INTO ' + tablename + ' ("id", "text") VALUES (2, "Met spatie?");')
    print dbT.Query('INSERT INTO ' + tablename + ' ("id", "text") VALUES (3, "Andere text");')
    print dbT.Query('INSERT INTO ' + tablename + ' ("id", "text") VALUES (4, "Incluus cijfers 123");')
    print

    print "Incorrectly typed"
    print dbT.Query('INSERT INTO ' + tablename + ' ("id", "text") VALUES ("a", "testtext");')
    print

    print dbT.tables[tablename].rows



# ---------------------------------------------------------------------------
# Function calls
# ---------------------------------------------------------------------------


PrimaryTable("typeTest")
#InsertTest("jank")
#MultilineQueries("typeTest")
#db = FileStore()

#FromFile()
#ToFile()
