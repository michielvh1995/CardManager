from Tools.Database import DataBase
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

print "Querying on multiple items"
print db.Query("SELECT (id, val) FROM test2;")
print db.Query("SELECT (id, value) FROM test2;")
