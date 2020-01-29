import re

class SQLInterpreter:
    def __init__(self):
        self.re_insert = re.compile("INSERT INTO (.*) \((.*)\) VALUES \((.*)\);")

    def Match(self, SQL):
        wrk = self.try_insert(SQL)

        if wrk:
            return wrk

        return ("NONE",None,None,None,None)


    def try_insert(self, sql):
        """ Try to insert items into the database
        input:
            sql:    string              the SQL query
        output:
                    (boolean, error):   whether or not the query was successfully executed
        """
        print "# DEBUG: "
        print sql
        print
        print self.re_insert.match(sql)


        # TODO: change the field and value items to lists
        out =["INSERT",None,None,None,None]

        for i in range(1,4):
            out[i] = self.re_insert.search(sql).group(i)


        return out



# ------------------------------------------------------------

class Table:
    def __init__(self, fieldnames, where=None):
        self.fields = fieldnames    #
        self.header = []        # The field names
        self.rows = []          # [{name: field}]

        for f in self.fields:
            self.header.append(f)

    def Insert(self, names, values, ret = None):
        """ Insert a new row to the table
        """
        row = {}
        for i, f in enumerate(names):
            row[f] = values[i]

        self.rows.append(row)

        if ret:
            return "asd"

class Card:
    def __init__(self):
        self.id = None

class DataBase:
    def __init__(self, passwd = None):
        # Necessary?
        self.sqlinterpreter = SQLInterpreter()      # Cleaning SQL and performing actions (?)
        self.tablenames = []                        # List of the table names
        self.tables = {}                            # { name : Table }

    def create_table(self, name, fields, where = None, ret = None):
        """ Create and add a new table to the database
        """
        tbl = Table(fields)
        self.tables[name] = tbl
        self.tablenames.append(name)
    #

    def Query(self, query):
        """ Execute a query """
        # Interpret SQL
        # Currently hardcoded to just accapt insertion queries
        act, tb, fields, values, ret = self.sqlinterpreter.Match(query)
        fields = fields.split(",")
        values = values.split(",")

        print fields
        if act == "INSERT":
            ret = self.insert(tb, fields, values, ret)


        return ret

    def insert(self, tbl, fields, values, ret):
        """ Insert a row into a table
        """
        if tbl in self.tablenames:
            self.tables[tbl].Insert(fields, values)

            # Query return values and return them

            return "TRUE"
        else:
            return "ERROR"
    #
    # def create_table(self, name, fields, where = None, ret = None):
    #     """
    #
    #     """
    #     print "create table"
    #     self.tables.append(Table(fields, where))
    #     self.tblnames[name] = len(self.tables)
    #
    #     return ret


# ===================================================
# Debugging
# ===================================================
print "init \n"
db = DataBase()

print "create table \n"
db.create_table("test", fields = ["id", "value"])

print "tables"
print db.tables["test"]

print "query"
print db.Query("INSERT INTO test (id) VALUES (1);")
print

print ("queried")
print db.tables["test"].rows
print

db.create_table("test2", ["id", "test", "val"])
print db.Query('INSERT INTO test2 ("test", "val", "id") VALUES ("AAA", "BBB", "0");')


print db.tables["test2"].rows
