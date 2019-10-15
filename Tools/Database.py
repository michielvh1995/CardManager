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

        # TODO: change the field and value items to lists
        out =["INSERT",None,None,None,None]

        for i in range(1,4):
            out[i] = self.re_insert.search(sql).group(i)


        return out



# ------------------------------------------------------------

class Table:
    def __init__(self, fields, where=None):
        self.fields = fields
        self.header = {}
        self.rows = []

        for i, f in enumerate(fields):
            self.header[f] = i


    def Insert(self, fields, values, ret = None):
        """
            Insert a new row to the table
        """
        row = [None]*len(self.fields)

        for i, f in enumerate(fields):
            row[self.header[f]] = values[i]

        self.rows.append(row)

        if ret:
            return "asd"

class DataBase:
    def __init__(self, passwd = None):
        self.sqlinterpreter = SQLInterpreter()

        # TODO: create table creation logic
        self.tables = []
        self.tblnames = {}


        self.tables.append(Table(["id"]))
        self.tblnames["test"] = 0

        if passwd:
            # Encryption logic
            self.enc = True

    def Query(self, query):
        """ Execute a query """
        # Interpret SQL
        act, tb, fields, values, ret = self.sqlinterpreter.Match(query)

        if act == "INSERT":
            ret = self.insert(tb, [fields], [values], ret)


        return ret

    def insert(self, tbl, fields, values, ret):
        """
            Insert a row into a table
        """
        print "DB.insert"
        return self.tables[self.tblnames[tbl]].Insert(fields, values, ret)

    def create_table(self, name, fields, where = None, ret = None):
        """

        """
        print "create table"
        self.tables.append(Table(fields, where))
        self.tblnames[name] = len(self.tables)

        return ret





db = DataBase()

db.Query("INSERT INTO test (id) VALUES (1);")
print db.tables[0].rows

db.create_table("test2", ["id", "test", "val"])
db.Query('INSERT INTO test2 ("test", "val", "id") VALUES ("AAA", "BBB", "0")')
