import re

class ERROR:
    def __init__(self):
        self.e = "ERROR"

    def __str__(self):
        return self.e

class KEYNOTFOUNDERROR(ERROR):
    def __init__(self, key, table = None):
        self.e = "KEY ERROR: key " + str(key) + " not found in table" + ((" in table " + table) if table else "!")
        self.internal = ["ERROR", table, key]

    def __getitem__(self, key):
        return self.internal[key]

# Database response:
# [str, table. fields, (other)]
class SQLInterpreter:
    def __init__(self):
        self.re_insert = re.compile("INSERT INTO (.*) \((.*)\) VALUES \((.*)\);")
        self.re_select = re.compile("SELECT \((.*)\) FROM (.*)( WHERE)?(.*)?;")

        # Cleaning the (sub)strings
        self.re_clean = re.compile(r"[\s+\"\']")

    def Match(self, SQL):
        wrk = self.try_insert(SQL)

        if wrk:
            return wrk

        return ("NONE",None,None,None,None)

    def TryDecodeSQL(self, SQL):
        """ Try all possible types of queries and return the correct type

        """

        # The insert query path:

        out = self.try_insert(SQL)
        if(out[0] == "INSERT"):
            out[2] = self.re_clean.sub("", out[2]).split(",")
            out[3] = self.re_clean.sub("",out[3]).split(",")
            # ["command", table, fields, values, return]
            return out

        out = self.try_select(SQL)
        if (out[0] == "SELECT"):

            return out

        return ["NONE"]


        # The update query path:
        # The remove query path:
        # The select query path:

    def try_select(self, sql):
        """ Try to see whether or not the query is a selection query and break it up in parts
        """
        res = self.re_select.search(sql)

        if res:
            ret = [
                "SELECT",         # Type
                self.re_clean.sub("", res.group(2)),            # Table
                self.re_clean.sub("", res.group(1)).split(",") # Fields
                # WHERE-or-not
                # WHERE query
            ]

            return ret
        return ["NONE"]


    def try_insert(self, sql):
        """ Try to insert items into the database
        input:
            sql:    string              the SQL query
        """

        out = ["NONE",None,None,None,None]
        if self.re_insert.search(sql):
            out[0] = "INSERT"
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

    def Select(self, names):
        """ Check if all names are in the fields and return the values of the rows per field
        """
        out = []

        for row in self.rows:
            r = []
            for n in names:
                if row.has_key(n):
                    r.append(row[n])
                else:
                    return KEYNOTFOUNDERROR(n)
            out.append(r)
        return out


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
        return "Created table: \"" + str(name)+"\""
    #

    def Query(self, query):
        """ Execute a query """
        # Interpret SQL
        # Currently hardcoded to just accept insertion queries
        ret = ""
        res = self.sqlinterpreter.TryDecodeSQL(query)

        print res
        if res[0] == "INSERT":
            ret = self.insert(res[1], res[2], res[3], res[4])

        elif res[0] == "SELECT":
            if len(res) > 3:
                ret = self.select(res[1], res[2], res[4])
            else:
                ret = self.select(res[1], res[2])

        elif res[0] == "ERROR":
            return res

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

    def select(self, tbl, fields, where = None):
        """ Return all values of certain fields from a table.
        WHERE clauses can be used to filter the fields on.
        """

        if tbl in self.tablenames:
            return self.tables[tbl].Select(fields)

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
