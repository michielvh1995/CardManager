import re
import DBErrors as err
import SQLResponse as rs

insert_str = "^INSERT INTO (.*) \((.*)\) VALUES \((.*)\);"
select_str = "^SELECT \((.*)\) FROM (.*)[ ;]"

where_str = " ?(WHERE|AND|OR) [\'\(](.*)[\'\)] = (.*)[ ;]"

#test = " (.*) = (.*)?( WHERE| AND| OR) (.*) = (.*)[ ;]"
test = "SELECT\s+(.*)\s+FROM\s+(.*)"
test = "WHERE\s+(.*)=(.*)\s+?(AND|OR)\s+(.*)"


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

            outp = rs.SQLResponse("INSERT",
                table  = out[1],
                fields = self.re_clean.sub("", out[2]).split(",")
                )
            outp["values"] = self.re_clean.sub("",out[3]).split(",")
            return outp

        out = self.try_select(SQL)
        if (out["type"] == "SELECT"):
            return out

        return err.COMMANDNOTFOUNDERROR(SQL)


        # The update query path:
        # The remove query path:
        # The select query path:

    def try_select(self, sql):
        """ Try to see whether or not the query is a selection query and break it up in parts
        """
        ret = rs.SQLNone

        # Check whether or not it is a selection operation
        res = self.re_select.search(sql)

        # If it is not a SELECT query
        if not res:
            return ret

        # Check for a WHERE
        print
        print "wh.groups():"
        wh = self.re_where.search(sql)
        where = None

        # If a WHERE clause exists
        if wh:
            # Remove the WHERE from the initial query:
            sql = self.re_where.sub(";", sql)

            # Properly extract the SELECT
            res = self.re_select.search(sql)

            # And set the rest list
            where = self.cleanWhere(wh)

        # Now extract the table and fields from the query
        ret = rs.SQLResponse("SELECT",
            table = self.re_clean.sub("", res.group(2)),
            fields = self.re_clean.sub("", res.group(1)).split(",")
            )

        ret["where"] = where

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

    def cleanWhere(self, resrch):
        """ TODO: This function cleans the WHERE statement to a useful list of (key, value) pairs

        """
        tar = []
        t1 = resrch.group(2)
        t2 = resrch.group(3)
        tar.append(
            (self.re_clean.sub("",t1),self.re_clean.sub("",t2))
        )

        return tar
