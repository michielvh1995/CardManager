import DBErrors as err
import SQLInterpreter


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

    def Select(self, fields, where = None):
        """ Check if all names are in the fields and return the values of the rows per field
        """
        out = []
        print
        print "where: "  + str(where)

        for row in self.rows:
            r = []
            use = True
            if where:
                for pair in where[0]:
                    if row.has_key(pair[0]):
                        if not row[pair[0]] == pair[1]:
                            use = False
                    else:
                        return err.KEYNOTFOUNDERROR(pair[0])

            print
            print use



            # Match the WHERE

            # Select fields per row
            if use:
                for n in fields:
                    if row.has_key(n):
                        r.append(row[n])
                    else:
                        return err.KEYNOTFOUNDERROR(n)
                out.append(r)
        return out


class Card:
    def __init__(self):
        self.id = None

class DataBase:
    def __init__(self, passwd = None):
        # Necessary?
        self.sqlinterpreter = SQLInterpreter.SQLInterpreter()      # Cleaning SQL and performing actions (?)
        self.tablenames = []                        # List of the table names
        self.tables = {}                            # { name : Table }

    def create_table(self, name, fields, where = None, ret = None):
        """ Create and add a new table to the database
        """
        tbl = Table(fields)
        self.tables[name] = tbl
        self.tablenames.append(name)
        return "Created table: \"" + str(name)+"\""
    #

    def Query(self, query):
        """ Execute a query """
        # Interpret SQL
        # Currently hardcoded to just accept insertion queries
        ret = ""
        res = self.sqlinterpreter.TryDecodeSQL(query)

        if res[0] == "ERROR":
            return res

        elif res[0] == "INSERT":
            ret = self.insert(res[1], res[2], res[3], res[4])

        elif res[0] == "SELECT":
            ret = self.select(res)

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

    def select(self, sqlresponse):
        """ Return all values of certain fields from a table.
        WHERE clauses can be used to filter the fields on.
        input:
            sqlresponse : SQLResponse : the objectified SQL query
        """

        if sqlresponse[1] in self.tablenames:
            wh = None
            if sqlresponse.WHERE:
                wh = [sqlresponse[4], sqlresponse[5]]
            return self.tables[sqlresponse[1]].Select(fields = sqlresponse[2], where=wh)

        return "FALSE"
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

db = DataBase()
print db.create_table("test2", ["id", "test", "val"])
print db.Query('INSERT INTO test2 ("test", "val", "id") VALUES ("AAA", "BBB", "0");')
print db.Query('INSERT INTO test2 ("test", "val", "id") VALUES ("AAB", "BBB", "1");')

print "Querying"
#print db.Query("SELECT (id, val) FROM test2;")
print db.Query("SELECT (id, val) FROM test2 WHERE 'test' = AAA;")
