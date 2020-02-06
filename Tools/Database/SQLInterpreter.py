import re
import DBErrors as err

insert_str = "^INSERT INTO (.*) \((.*)\) VALUES \((.*)\);"
select_str = "^SELECT \((.*)\) FROM (.*)[ ;]"

where_str = " ?(WHERE|AND|OR) \'(.*)\' = (.*)[ ;]"

#test = " (.*) = (.*)?( WHERE| AND| OR) (.*) = (.*)[ ;]"
test = "SELECT\s+(.*)\s+FROM\s+(.*)"
test = "WHERE\s+(.*)=(.*)\s+?(AND|OR)\s+(.*)"


# Database response:
# [str, table. fields, (other)]
class SQLResponse:
    def __init__(self, type, table = None, fields = None, rest = None, where = False ):
        self.internal = [type, table, fields]
        if rest:
            for i in rest:
                self.internal.append(i)

        self.tbl = table
        self.rest = rest
        self.fields = fields

        # Flags for queries:
        self.WHERE = where

    def __getitem__(self, key):
        return self.internal[key]

    def __len__(self):
        return len(self.internal)

    def __str__(self):
        return str(self.internal)

SQLNone = SQLResponse("NONE")

class SQLInterpreter:
    def __init__(self):
        self.re_insert = re.compile(insert_str)
        self.re_select = re.compile(select_str)

        self.re_where = re.compile(where_str)

        # Cleaning the (sub)strings
        self.re_clean = re.compile(r"[\s+\"\']")

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

        return err.COMMANDNOTFOUNDERROR(SQL)


        # The update query path:
        # The remove query path:
        # The select query path:

    def try_select(self, sql):
        """ Try to see whether or not the query is a selection query and break it up in parts
        """
        ret = SQLNone

        # Check whether or not it is a selection operation
        res = self.re_select.search(sql)

        # If it is not a SELECT query
        if not res:
            return ret

        # Check for a WHERE
        print
        print
        print

        wh = self.re_where.search(sql)
        print wh.groups()
        rest = [wh is not None]
        print
        print

        # If a WHERE clause exists
        if wh:
            # Remove the WHERE from the initial query:
            sql = self.re_where.sub(";", sql)

            # Properly extract the SELECT
            res = self.re_select.search(sql)

            # And set the rest list
            self.cleanWhere(rest, wh)


        # Now extract the table and fields from the query
        ret = SQLResponse("SELECT",
            table = self.re_clean.sub("", res.group(2)),
            fields = self.re_clean.sub("", res.group(1)).split(","),
            rest = rest,
            where = rest[0])

        return ret


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

    def cleanWhere(self, tar, resrch):
        """ TODO: This function cleans the WHERE statement to a useful list of (key, value) pairs

        """
        t1 = resrch.group(2)
        t2 = resrch.group(3)
        tar.append(
            (self.re_clean.sub("",t1),self.re_clean.sub("",t2))
        )
        print tar
