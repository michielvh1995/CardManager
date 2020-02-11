import re
import DBErrors as err
import DBResponse as rs

insert_str = "^INSERT INTO (.*) \((.*)\) VALUES \((.*)\);"
select_str = "^SELECT \((.*)\) FROM (.*)[ ;]"

where_str = " ?(WHERE|AND|OR) [\'\(](.*)[\'\)] = (.*)[ ;]"

#test = " (.*) = (.*)?( WHERE| AND| OR) (.*) = (.*)[ ;]"
test = "SELECT\s+(.*)\s+FROM\s+(.*)"
test = "WHERE\s+(.*)=(.*)\s+?(AND|OR)\s+(.*)"

createTable = "^CREATE TABLE (.*)\s+\((.*)\);"


# Cleaning regex:
clean_name = "[\"\\\'\(\s+]"
clean_field = "\""



class SQLInterpreter:
    def __init__(self):
        self.re_table = re.compile(createTable)

        self.re_insert = re.compile(insert_str)
        self.re_select = re.compile(select_str)

        self.re_where = re.compile(where_str)

        # Cleaning the (sub)strings
        self.re_clean = re.compile(r"[\s+\"\']")

        self.clean_name  = re.compile(clean_name)
        self.clean_field = re.compile(clean_field)

    # TODO: REFACTOR THIS FUNCTION AND ALL ITS CHILDREN
    def TryDecodeSQL(self, sql):
        """ Try all possible types of queries and return the correct type

        """
        SQL = sql
        # CREATE DATABASE:


        # CREATE TABLE:
        out = self.try_CreateTable(sql)
        if out["type"] == "CREATE TABLE" or out["type"] == "ERROR":
            return out

        # INSERT
        out = self.try_insert(SQL)
        if out["type"] == "INSERT" or out["type"] == "ERROR":
            return out


        # SELECT






        # The insert query path:

        out = self.try_select(SQL)
        if (out["type"] == "SELECT"):
            return out

        return err.COMMANDNOTFOUNDERROR(SQL)


        # The update query path:
        # The remove query path:
        # The select query path:

    def try_CreateTable(self, sql):
        """ Try to determine whether or not the statement is a CREATE TABLE statement
        """
        ret = rs.SQLNone
        regex_result = self.re_table.search(sql)

        if regex_result:
            # TODO: Improve upon this splitting
            # TODO: Create the constraints array/dictionary
            fields = regex_result.group(2).split(",")   # Break fields up in field constraint tuples
            fields = [f.split() for f in fields]

            fdict = {}
            for f in fields:
                fdict[f[0]] = f[1]

            ret = rs.SQLResponse(
                type = "CREATE TABLE",
                table = regex_result.group(1),  # Table name is the first group in the match
                fields = fdict                  # The dictionary of field TYPE pairs
            )

        return ret


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

        out = rs.SQLNone
        res = self.re_insert.search(sql)    # table, [field], [value]
        if res:
            # Split the fields & values into keyvalue pairs
            fields = [self.clean_name .sub("", f) for f in res.group(2).split(",")]
            values = [self.clean_field.sub("", f) for f in res.group(3).split(",")]

            # Combine cleaned fields into pairs
            kvpairs = zip(fields,values)

            # Put everything into a SQLResponse
            out = rs.SQLResponse(
                type   = "INSERT",       # INSERT
                table  = res.group(1),   # Table
                fields = kvpairs         # [(Field,Value)]
            )

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
