import csv                      # TODO: Move to new file
import re                       # TODO: Move to new file

from DBResponse import FILESysAcknowledge as ack
from DBErrors   import FileSysError       as err
from Database   import TypedDataBase

class FileService:
    def __init__(self, file, encoding = None, endl = "\n"):
        self.FS = open(file, "r+w")
        self.enc = encoding
        self.endl = endl

        self.sectEnd = "--------------------------------------------" + endl

        # value cleaning:
        self.re_clean = re.compile('[^a-zA-Z]')

    def Read(self):
        """ Simple function: reads the entire database and returns it
        returns:
            TypedDataBase : The database retrieved from the file
        """
        # Reset file pointer
        self.FS.seek(0)

        # Retrieve the name of the database and the amount of tables
        header = self.FS.readline().split(" : ")
        name = header[0]
        tableCount = int(header[1])

        db = TypedDataBase(name = name)

        # Retrieve the tables:
        for i in range(tableCount):
            # Get to the next section of the file
            self.readTilSectionEnd()

            # Get the name of the table
            tblhead = self.FS.readline().split(" : ")
            tblname = tblhead[1]           # Name of the table
            cnstCnt = int(tblhead[2])      # The amount of constraints; each is one line

            # Retrieve the field names and their types:
            # BUG: There's a bug here where all lines end with "\r\n"
            fnames = self.FS.readline()[:-2].split(",")
            ftypes = self.FS.readline()[:-1].split(",")

            # TODO: Throw an error if not each field got a type:
            if not len(fnames) == len(ftypes):
                return "ERROR: len fnames !=  lenftypes"

            # TODO: Retrieve the constraints:
            for i in range(cnstCnt):
                self.FS.readline()

            # Combine type & names
            fields = {}
            for i in range(len(fnames)):
                fields[self.cleanValue(fnames[i])] = self.cleanValue(ftypes[i])


            # Now add the table to the database
            tbres = db.create_table(tblname, fields)

            # TODO: Check if the table is successfully created
            if tbres["type"] == "ERROR":
                return tbres

            # Now insert the values to the table

            # TODO: Skip the empty line, throw an error if it is not empty
            if len(self.FS.readline()) > 1:
                return "ERROR : EMPTY LINE NOT EMPTY"

            # Now read lines until the next empty line:
            ln = self.FS.readline()
            while len(ln) > 1:
                # BUG: There's a bug here where all lines end with "\r\n"
                vals = ln[:-2].split(",")

                # Insert them into the table
                db.insert(tbl = tblname, kvpairs = zip(fnames, vals))

                # Get the next line
                ln = self.FS.readline()

        return db



    def OverwriteAll(self, db):
        """ Simple function: overwrite the entire file with the new database
        input:
            db      :   TypedDataBase   :   The database that is to be written to a file
        returns:
            Respone :   Either a SUCCESS or an ERROR
        """
        self.FS.truncate(0)     # Clear the file

        # Write the database name
        self.FS.write(db.name)
        self.FS.write(" : ")
        self.FS.write(str(len(db.tablenames)))

        self.endSection()

        # Write all the tables
        for name in db.tablenames:
            self.writeTable(db.tables[name])
            self.endSection()

    # TODO: write function explanation
    def searchForTable(self, tablename):
        """ Set the file index pointer to where this table resides
        """
        self.FS.seek(0)
        while True:
            self.readTilSectionEnd()


            tblhead = self.FS.readline()
            if tblhead:
                tblname = tblhead.split(" : ")[1]           # Name of the table
                if tblname == tablename:
                    self.FS.seek(-len(tblhead)-1,1)
                    return ack(position = self.FS.tell())
            else:
                return err(explanation = "Table not in file")

    # TODO: Make this function more efficient
    # TODO: Make it use a temporary file when writing
    # TODO: Implement checks so that we do not have to reread and rewrite everything
    def UpdateTable(self, table):
        """ Searches for a table and replaces its row values for the new rows
        input:
            table     : TypedTable  :   A table that has changed and needs to be updated
        returns:
            Response  : Either an FILESysAcknowledge or FileSysError, whether or not it succeeded
        """
        sft = self.searchForTable(table.name)

        if sft["type"] == "ERROR":
            return sft

        # Read the rest of the file
        self.readTilSectionEnd()
        tmp = self.FS.readlines()

        # Return to the point where the table started
        self.FS.seek(sft["position"])

        # Write the table
        self.writeTable(table)
        self.endSection()

        # Rewrite the rest of the file
        self.FS.writelines(tmp)

        # TODO: Do proper error checking
        # TODO: Make this function more efficient
        return ack()

    def AppendTable(self, table):
        """ TODO: WRITE THIS FUNCTION
         Write new values in a table at the end of it in the file.
        input:
            table       :   TypedTable  :   A table that has new values, that will be appended to it
        returns:
            Response    :   Either an FILESysAcknowledge or FileSysError, whether or not it succeeded
        """

    def writeTable(self, table):
        """ TODO: write function explanation
        Exports a table
        """
        self.FS.write("table : ")
        self.FS.write(table.name)
        self.FS.write(" : ")
        self.FS.write(str(len([1])))    # TODO: Write the amount of constraints
        self.FS.write(self.endl)

        # Get the header of the table (fieldnames)
        nms = table.fields.keys()
        writer = csv.DictWriter(self.FS, fieldnames = nms)
        writer.writeheader()

        # Get and write the types of each of the fields
        types = []
        for name in nms:
            types.append(table.fields[name])

        self.FS.write(",".join(types))
        self.FS.write(self.endl)

        # TODO: write the constraints of the tables
        self.FS.write("CONSTRAINT LINE\n")
        self.FS.write(self.endl)

        # Now write the table
        writer.writerows(table.rows)

    # ===================================================
    # Helper functions
    # ===================================================

    def endSection(self):
        """ Write the end of a section
        """
        self.FS.write(self.endl)
        self.FS.write(self.sectEnd)
        self.FS.write(self.endl)
        self.FS.flush()

    def readTilSectionEnd(self):
        """ Read the file until a section ends
        """
        while True:
            ln = self.FS.readline()
            if ln == self.sectEnd or not ln:
                self.FS.readline()
                return

    def cleanValue(self, val):
        """ Strips a value off of all non alphabetical characters
        input:
            val     :   string    : The value to be cleaned
        returns:
            String  :   The cleaned value string
        """
        return self.re_clean.sub('',val)

    def __del__(self):
        self.FS.flush()
        self.FS.close()
