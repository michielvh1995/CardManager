import re
import DBErrors as err
import DBResponse as rs

insert_str = "INSERT INTO\s+(.*)\s+\((.*)\)\s+VALUES\s+\((.*)\);"

where_str = " ?(WHERE|AND|OR) [\'\(](.*)[\'\)] = (.*)[ ;]"

#test = " (.*) = (.*)?( WHERE| AND| OR) (.*) = (.*)[ ;]"
test = "SELECT\s+(.*)\s+FROM\s+(.*)"
test = "WHERE\s+(.*)=(.*)\s+?(AND|OR)\s+(.*)"

createTable = "^CREATE TABLE (.*)\s+\((.*)\);"


# Cleaning regex:
clean_name = "[\"\\\'\(\s+]"
clean_field = "[\"\']"
clean_comment = "[^\"]*(\"[^\"]*\"[^\"]*)*(--.*)"           # BUG: fires off even numbers of "" as well

# New SELECT
select = "SELECT\s+\((.*)\)\s+FROM\s+([a-zA-Z]+)(.*);"
where = "\s+WHERE\s+(.*)\s+(>=|<=|=|<|>)\s+(..*)"

# Checks
complete = "[^\"^\']*([\"\'][^\"^\']*\"[^\"^\']*)*(.*);"    # BUG: fires off even numbers of "" as well




class SQLInterpreter:
    def __init__(self):
        self.re_table = re.compile(createTable)
        self.re_insert = re.compile(insert_str)

        self.re_where = re.compile(where_str)

        # Cleaning the (sub)strings
        self.re_clean = re.compile(r"[\s+\"\']")

        self.clean_name  = re.compile(clean_name)
        self.clean_field = re.compile(clean_field)


        self.re_complete = re.compile(complete)

        # TODO: TEST
        self.re_selectNew = re.compile(select)
        self.re_whereNew = re.compile(where)

    # TODO: REFACTOR THIS FUNCTION AND ALL ITS CHILDREN
    def TryDecodeSQL(self, sql):
        """ Try all possible types of queries and return the correct type

        """
        # Clean the SQL query from comments and such
        sql = self.CleanSQL(sql)

        # CREATE DATABASE:


        # CREATE TABLE:
        out = self.try_CreateTable(sql)
        if out["type"] == "CREATE TABLE" or out["type"] == "ERROR":
            return out

        # INSERT
        out = self.try_insert(sql)
        if out["type"] == "INSERT" or out["type"] == "ERROR":
            return out


        # SELECT
        out = self.try_select(sql)
        if (out["type"] == "SELECT"):
            return out

        # The update query path:
        # The remove query path:
        # The select query path:
        return err.COMMANDNOTFOUNDERROR(sql)



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

            # Register the constraints and turn it into a dict
            fdict = {}
            for f in fields:
                fdict[f[0]] = f[1:]

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


        # See whether or not it is a SELECT query
        res =  self.re_selectNew.search(sql)

        if not res:
            return ret
        # Check for a WHERE clause
        wh = self.re_whereNew.search(res.group(3))

        conditions = []
        if wh:
            conditions.append(wh.groups())

        ret = rs.SQLResponse(
            type   = "SELECT",                                      # Type
            table  = self.re_clean.sub("", res.group(2)),           # What table
            fields = self.re_clean.sub("", res.group(1)).split(",") # Fieldnames
        )
        ret["conditions"] = conditions

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

            # TODO: Is this correct?
            for i in range(len(values)):
                if values[i][0] == " ":
                    values[i] = values[i][1:]

            # Combine cleaned fields into pairs
            kvpairs = zip(fields,values)

            # Put everything into a SQLResponse
            out = rs.SQLResponse(
                type   = "INSERT",       # INSERT
                table  = res.group(1),   # Table
                fields = kvpairs         # [(Field,Value)]
            )

        return out

    def IsComplete(self, sql):
        """ TODO: Description
        """

        # Clean the SQL query from comments and such
        sqln = self.CleanSQL(sql)

        m = self.re_complete.match(sql)

        if m:
            return rs.SQLComplete(sqln)

        ret = rs.SQLIncomplete(sqln)
        return ret


    # ------------------------------------------------------------------
    # Cleaning
    # ------------------------------------------------------------------
    def CleanSQL(self, sql):
        """ Clean a SQL statement of all kinds of impurities
        """
        sql = self.cleanComments(sql)

        return sql

    def cleanComments(self, sql):
        """ Look for any sequence "--" with an even amount of \' and \" in front of it
        input:
            sql     :   string      : The SQL query to be cleaned
        """
        m = re.match(clean_comment, sql)

        sqln = sql

        # Continuously remove comment sections
        while m:
            sqln = sqln[:sql.find(m.group(2))]  # Subset the string
            m = re.match(clean_comment, sqln)   # Get the new match object of the result string
        return sqln


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
