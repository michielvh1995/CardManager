import DBErrors as err          # TODO: UNUSED remove
import DBResponse
import SQLInterpreter

from Table import TypedTable

class TypedDataBase:
    # TODO: when creating tables is done using SQL we need to do the following:
    # When creating tables the return value of create table (from the Table class) becomes a DBresponse
    # Thus error checking needs to be done in the DataBase class as well
    # For now we assume that creating tables is always done correctly
    def __init__(self, name = None, passwd = None):
        self.sqlinterpreter = SQLInterpreter.SQLInterpreter()      # Cleaning SQL and performing actions (?)
        self.tablenames = []                        # List of the table names
        self.tables = {}                            # { name : Table }
        self.name = name

        # Multi-line SQL commands
        self.lastcommand = ""

    def InputSQL(self, input):
        """ Allows text to be inputted
        """
        # Append the lastcommand var
        self.lastcommand += input
        self.lastcommand = self.sqlinterpreter.CleanSQL(self.lastcommand)

        res = self.sqlinterpreter.IsComplete(self.lastcommand)

        # Check for completeness and execute the query if it is
        if res["type"] == "COMPLETE":
            self.lastcommand = "" # Reset last command
            return self.Query(res["query"])

        # if the command isn't complete, just wait
        return res

    def Query(self, query):
        """ Execute a query
        input:
            query   :   string  :   A SQL query to be executed
        returns:
            DBResponse  :   The effect of the query
        """
        # Interpret SQL
        # Currently hardcoded to just accept insertion queries
        ret = DBResponse.DBResponse("None")
        res = self.sqlinterpreter.TryDecodeSQL(query)

        if res["type"] == "ERROR":
            return res

        elif res["type"] == "INCOMPLETE":   # For multiline SQL queries
            self.lastcommand += res["query"]

        elif res["type"] == "INSERT":
            ret = self.insert(
                tbl     = res["table"],
                kvpairs = res["fields"]    # Fields::[(field, value)]
            )

        elif res["type"] == "SELECT":
            ret = self.select(
                table       = res["table"],
                fields      = res["fields"],
                conditions  = res["conditions"]
            )

        elif res["type"] == "CREATE TABLE":
            ret = self.create_table(
                    name = res["table"],
                    fields = res["fields"]
                )

        return ret

    def insert(self, tbl, kvpairs):
        """ Insert a row into a table
        input:
            tbl     : string              : The name of the target table
            kvpairs : [(string, string)]  : A list of key-value pairs of values to insert into fields

        """
        res = err.TABLENOTFOUNDERROR(tbl)

        # TODO: THIS IS A TEST
        if tbl in self.tablenames:
            res = self.tables[tbl].Insert(kvpairs)

        return res

    def select(self, table, fields, conditions):
        """ Select specified fields, of rows where all conditions are met
        """

        res = err.TABLENOTFOUNDERROR(table)
        if table in self.tablenames:
            res = self.tables[table].Select(fields, conditions)

        return res


    def create_table(self, name, fields):
        """ Adds a TypedTable to the list of tables
        input:
            name        : string            : name of the table
            fields      : {string, [string]}: dictionary of field names and their constraints (type is one)
            constraints : [TBD]             : A set of constraints for the values in the table (i.e. primary keys)
        returns:
            DBResponse  : confirmation or error message
        """

        # Create an empty table:
        table = TypedTable()
        res = table.TryCreateTable(name, fields)

        if res["type"] == "SUCCESS":
            self.tables[name] = table
            self.tablenames.append(name)

        return res

    # ===================================================
    # File Operations
    # ===================================================
    def ExportAsSQL(self, filestream, encoding = "LINUX"):
        """ Exports the database as a list of SQL statements to an active filestream
        input:
            filestream  : file    : A python filestream to write to
        returns:
            DBResponse  : An acknowledge or an error, depending on if everything went right
        """
        nl = "\r\n"
        if encoding == "LINUX":
            nl = "\n"
        elif encoding == "WINDOWS":
            nl = "\r\n"

        # Create DB:
        filestream.write("--Create database:" + nl)
        filestream.write("--CREATE DATABASE " + str(self.name) + ";" + nl)

        # Create Tables:
        filestream.write(nl + "--Create tables:" + nl)
        for name in self.tablenames:
            filestream.write("CREATE TABLE " + str(name) + " (" +nl)

            # Creating all fields of the tables
            for i, field in enumerate(self.tables[name].fields.keys()):
                filestream.write("    " + str(field) + " " +
                    str(self.tables[name].fields[field]) +
                    ("," +nl if i+1 < len(self.tables[name].fields.keys()) else nl))
            filestream.write(");" + nl)

        # The data of each table:
        filestream.write(nl + "--Fill in the data of each table:" + nl)
        for table in self.tablenames:               # Export per table:
            for row in self.tables[table].rows:     # Export each row
                fields = row.keys()                 # Not each row has a value for all the keys

                values = "', '".join(map(str,[row[key] for key in fields ]))
                line = "INSERT INTO " +table+" ('"+ "', '".join(map(str, fields)) +"')" + nl +"    VALUES ('"+values+"');"
                filestream.write(line + "" + nl)

        return DBResponse.DBResponse("EXPORT COMPLETE")
        print

    def ImportSQL(self, filestream):
        """ Import a database from a SQL file
        input:
            filestream  : file    : A python filestream to write to
        returns:
            Not sure yet
        """

        lines = filestream.read().split("\n")

        for i in lines:
            ret = self.InputSQL(i)

            if ret["type"] == "ERROR":
                return ret


        res = DBResponse.DBResponse("IMPORT COMPLETE")
        return res
