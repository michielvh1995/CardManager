from Tools.Database.Database import DataBase, TypedDataBase
# ===================================================
# Debugging
# ===================================================
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

print "Creating a TABLE with field types"
print dbT.create_table("typeTest", {"id" : "TEXT", "text": "TEXT"})
print

print "Correct typing:"
print dbT.Query('INSERT INTO typeTest ("id", "text") VALUES (1, "testtext");')
print dbT.Query('INSERT INTO typeTest ("id", "text") VALUES (2, "Met spatie?");')
print dbT.Query('INSERT INTO typeTest ("id", "text") VALUES (3, "Andere text");')
print

print "Incorrectly typed"
print dbT.Query('INSERT INTO typeTest ("id", "text") VALUES ("a", "testtext");')
print

print "Querying on typed database, note how spaces do not work yet:"
print dbT.Query("SELECT (id, text) FROM typeTest;")
print
