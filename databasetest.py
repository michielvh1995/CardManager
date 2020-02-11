from Tools.Database.Database import DataBase, TypedDataBase
# ===================================================
# Debugging
# ===================================================
if False:
    print "init \n"
    db = DataBase()

    print "create table \n"
    print db.create_table("test", fields = ["id", "value"])

    print "tables"
    print "   " + str(db.tables["test"])

    print "insert"
    print "   " + str(db.Query("INSERT INTO test (id) VALUES (1);"))
    print

    print "select"
    print db.Query("SELECT (id) FROM test;")
    print db.Query("SELECT (id, value) FROM test;")
    print

    print "Creating a larger table"
    print db.create_table("test2", ["id", "test", "val"])
    print db.Query('INSERT INTO test2 ("test", "val", "id") VALUES ("AAA", "BBB", "0");')
    print db.Query('INSERT INTO test2 ("test", "val", "id") VALUES ("BAA", "CCC", "1");')
    print db.Query('INSERT INTO test2 ("test", "val", "id") VALUES ("CAA", "DDD", "2");')
    print db.Query('INSERT INTO test2 ("test", "val", "id") VALUES ("DAA", "CCC", "3");')
    print

    print "Invalid key"
    print db.Query("SELECT (id, value) FROM test2;")
    print

    print "Querying on multiple items"
    for i in db.Query("SELECT (id, val) FROM test2;"):
        print "  " + str(i)
    print

    print "Query with WHERE clause"
    for i in db.Query("SELECT (test, id, val) FROM test2 WHERE 'test' = AAA;"):
        print "  " + str(i)
    print

    print "Query with WHERE and AND"
    print db.Query("SELECT (id, val) FROM test2 WHERE 'test' = AAA AND 'val' = BBB")
    print


    print "Invalid SELECT query"
    print db.Query("FROM B SELECT (id, val) FROM test2 WHERE (test) = 'AAA';")
    print

# ---------------------------------------------------------------------------
# Round 2: TypedDatabase
# ---------------------------------------------------------------------------
dbT = TypedDataBase()

print "Create table query with field types:"
print dbT.Query("CREATE TABLE typeTest (id INT PRIMARY, text TEXT, other TEXT);")
print

print "Correct typing:"
print dbT.Query('INSERT INTO typeTest ("id", "text") VALUES (1, "testtext");')
print dbT.Query('INSERT INTO typeTest ("id", "text") VALUES (2, "Met spatie?");')
print dbT.Query('INSERT INTO typeTest ("id", "text") VALUES (3, "Andere text");')
print dbT.Query('INSERT INTO typeTest ("id", "text") VALUES (4, "Incluus cijfers 123");')
print

print "Incorrectly typed"
print dbT.Query('INSERT INTO typeTest ("id", "text") VALUES ("a", "testtext");')
print

print "Querying on multiple items"
for i in dbT.Query("SELECT (id, text) FROM typeTest;"):
    print "  " + str(i)
print

print "Querying with a WHERE clause"
for i in dbT.Query("SELECT (id, text) FROM typeTest WHERE id = 1;"):
    print "  " + str(i)
print

print "Export test, see file exporttest.sql"
with open("exporttest.sql", "w") as file:
    dbT.ExportAsSQL(file)
