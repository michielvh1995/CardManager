import DBErrors as err          # UNUSED
import DBResponse               # UNUSED
import SQLInterpreter
from Table import Table, TypedTable


# ------------------------------------------------------------
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
        ret = DBResponse.DBResponse("None")
        res = self.sqlinterpreter.TryDecodeSQL(query)

        if res["type"] == "ERROR":
            return res

        elif res["type"] == "INSERT":
            ret = self.insert(
                tbl   = res["table"],
                fields= res["fields"],
                values= res["values"],
                ret   = res["return"]
            )

        elif res["type"] == "SELECT":
            ret = self.select(
                table  = res["table"],
                fields = res["fields"],
                where  = res["where"]
            )

        return ret

    # TODO: Refactor this function and fix its return value
    def insert(self, tbl, fields, values, ret):
        """ Insert a row into a table
        """
        if tbl in self.tablenames:
            res = self.tables[tbl].Insert(fields, values)

        # Query return values and return them
        return res

    # TODO: Fix its return if no results are found
    def select(self, table, fields, where):
        """ Gather data of the specified fields in the specified table
        input:
            table   :   str     :   The name of the table from which data is requested
            fields  :  [str]    :   List of fieldnames of which data is requested
            where   :[str,value]:   List of fieldnames and values on which the data is filtered
        returns     :  [Row]    :   List of list with the requested data

        """
        if table in self.tablenames:
            return self.tables[table].Select(fields = fields, where = where)
        return "SELECT FALSE"
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

class TypedDataBase(DataBase):
    # TODO: when creating tables is done using SQL we need to do the following:
    # When creating tables the return value of create table (from the Table class) becomes a DBresponse
    # Thus error checking needs to be done in the DataBase class as well
    # For now we assume that creating tables is always done correctly
    def __init__(self, passwd = None):
        DataBase.__init__(self, passwd)

    def create_table(self, name, fields, constraints = None):
        """ Adds a TypedTable to the list of tables
        input:
            name        : string            : name of the table
            fields      : {string, string}  : dictionary of field names and their types
            constraints : [TBD]             : A set of constraints for the values in the table (i.e. primary keys)
        returns:
            string: confirmation or error message
        """
        self.tablenames.append(name)

        table = TypedTable(name, fields, constraints)
        self.tables[name] = table

        return "Created table: \"" + str(name)+"\""
