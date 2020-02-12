from Tools.Database.Database import TypedDataBase
# ===================================================
# Debugging
# ===================================================

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

#print "Querying on multiple items"
#for i in dbT.Query("SELECT (id, text) FROM typeTest;"):
#    print "  " + str(i)
#print
print "SELECT query"
for i in dbT.Query("SELECT (id, text) FROM typeTest;"):
    print "  " + str(i)
print

print "Querying with a WHERE clause"
for i in dbT.Query("SELECT (id, text) FROM typeTest WHERE id = 1;"):
    print "  " + str(i)
print

print "WHERE <="
for i in dbT.Query("SELECT (id, text) FROM typeTest WHERE id <= 2;"):
    print "  " + str(i)
print

print "Querying with a WHERE clause on a TEXT field"
for i in dbT.Query("SELECT (id, text) FROM typeTest WHERE text = testtext;"):
    print "  " + str(i)
print


print "With type errored WHERE clause"
print dbT.Query("SELECT (id, text) FROM typeTest WHERE id >= h;")
print


print "Export test, see file exporttest.sql"
with open("exporttest.sql", "w") as file:
    dbT.ExportAsSQL(file)
