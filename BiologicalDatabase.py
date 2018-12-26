import numpy as np
import mysql.connector
'''
1. run MySQL server through System Preferences

2. connect
/usr/local/mysql-5.7.17-macos10.12-x86_64/bin/mysql -u root -p
password: ugent



SHOW DATABASES;
CREATE DATABASE project_biological_databases;
USE project_biological_databases
'''

class BiologicalDatabase:
    # Start the connection to the database
    def __init__(self):
        self.cnx = mysql.connector.connect(user='root', password='ugent',
                                  host='localhost',
                                  database='project_biological_databases')
        self.cursor = self.cnx.cursor()

    # Access table syntax
    def print_table_syntax(self, table_name):
        response = list()
        self.cursor.execute(
            'DESCRIBE {}'.format(table_name)
        )
        for element in self.cursor.fetchall():
            response.append(element)
        return response



    # There are two tables:
    # borrelia (parent)
    # lysins (child)

    #####################
    # A. borrelia table #
    #####################
    # 1. Clear table
    def clear_entire_borrelia_table(self):
        self.cursor.execute("DELETE from borrelia")
        self.cnx.commit()
        return

    # 2. Add borrelia to table
    def add_borrelia_to_borrelia_table(self, borrelia_id, borrelia_name):
        self.cursor.execute("INSERT INTO borrelia (borrelia_id, borrelia_name) VALUES (%s, %s);",
                       (str(borrelia_id), str(borrelia_name)))

        self.cnx.commit()
        return

    # 3. Delete protein from table
    def delete_borrelia_from_borrelia_table_by_borrelia_id(self, borreliaid):
        self.cursor.execute(
            "DELETE from borrelia WHERE borrelia_id = " + "'" + borreliaid + "';")
        self.cnx.commit()
        return
    def delete_borrelia_from_borrelia_table_by_borrelia_name(self, borrelianame):
        self.cursor.execute(
            "DELETE from borrelia WHERE borrelia_name = " + "'" + borrelianame + "';")
        self.cnx.commit()
        return


    # 4. Query from table
    def query_borrelia_table_all(self):
        # header
        header = list()
        h = self.print_table_syntax('borrelia')
        for cell in h:
            header.append(cell[0])
        # rows
        response = list()
        self.cursor.execute("SELECT * FROM borrelia;")
        for line in self.cursor.fetchall():
            response.append(line)
        return header, response
    def query_borrelia_table_by_borrelia_id(self, borrelia_id):
        # header
        header = list()
        h = self.print_table_syntax('borrelia')
        for cell in h:
            header.append(cell[0])
        # rows
        response = list()
        self.cursor.execute("SELECT * FROM borrelia WHERE borrelia_id = " + "'" + str(borrelia_id) + "';")
        for line in self.cursor.fetchall():
            response.append(line)
        return header, response
    def query_borrelia_table_by_borrelia_name(self, borrelia_name):
        # header
        header = list()
        h = self.print_table_syntax('borrelia')
        for cell in h:
            header.append(cell[0])
        # rows
        response = list()
        self.cursor.execute("SELECT * FROM borrelia WHERE borrelia_name = " + "'" + str(borrelia_name) + "';")
        for line in self.cursor.fetchall():
            response.append(line)
        return header, response


    ##############################
    # B. lysins table #
    ##############################
    # 1. Clear table
    def clear_entire_lysins_table(self):
        self.cursor.execute("DELETE from lysins")
        self.cnx.commit()
        return

    # 2. Add lysins to the lysins
    def add_entry_to_lysins_table(self, borrelia_id, lysin_uniprotid, lysin_name, conserved_domains, properties):
        self.cursor.execute("INSERT INTO lysins (borrelia_id, lysin_id, lysin_name, conserved_domains, properties) VALUES (%s, %s, %s, %s, %s);",
                       (borrelia_id, lysin_uniprotid, lysin_name, conserved_domains, properties))
        self.cnx.commit()
        return

    # 3. Delete lysin from table
    def delete_lysin_from_lysins_table_by_borrelia_id(self, borreliaid):
        self.cursor.execute(
            "DELETE from lysins WHERE borrelia_id = " + "'" + borreliaid + "';")
        self.cnx.commit()
        return
    def delete_lysin_from_lysins_table_by_lysin_uniprotid(self, lysin_uniprotid):
        self.cursor.execute(
            "DELETE from lysins WHERE lysin_id = " + "'" + lysin_uniprotid + "';")
        self.cnx.commit()
        return
    def delete_lysin_from_lysins_table_by_lysin_name(self, lysin_name):
        self.cursor.execute(
            "DELETE from lysins WHERE lysin_name = " + "'" + lysin_name + "';")
        self.cnx.commit()
        return
    def delete_lysin_from_lysins_table_by_conserveddomain(self, conserveddomain):
        self.cursor.execute(
            "DELETE from lysins WHERE conserved_domains = " + "'" + conserveddomain + "';")
        self.cnx.commit()
        return
    def delete_lysin_from_lysins_table_by_properties(self, properties):
        self.cursor.execute(
            "DELETE from lysins WHERE properties = " + "'" + properties + "';")
        self.cnx.commit()
        return

    # 4. Query from table
    def query_lysins_table_all(self):
        # header
        header = list()
        h = self.print_table_syntax('lysins')
        for cell in h:
            header.append(cell[0])
        # rows
        response = list()
        self.cursor.execute("SELECT * FROM lysins;")
        for line in self.cursor.fetchall():
            response.append(line)
        return header, response

    def query_lysins_table_by_borrelia_id(self, borrelia_id):
        # header
        header = list()
        h = self.print_table_syntax('lysins')
        for cell in h:
            header.append(cell[0])
        # rows
        response = list()
        self.cursor.execute("SELECT * FROM lysins WHERE borrelia_id = " + "'" + str(borrelia_id) + "';")
        for line in self.cursor.fetchall():
            response.append(line)
        return header, response
    def query_lysins_table_by_lysin_id(self, lysin_uniprotid):
        # header
        header = list()
        h = self.print_table_syntax('lysins')
        for cell in h:
            header.append(cell[0])
        # rows
        response = list()
        self.cursor.execute("SELECT * FROM lysins WHERE lysin_id = " + "'" + lysin_uniprotid + "';")
        for line in self.cursor.fetchall():
            response.append(line)
        return header, response
    def query_lysins_table_by_lysin_name(self, lysin_name):
        # header
        header = list()
        h = self.print_table_syntax('lysins')
        for cell in h:
            header.append(cell[0])
        # rows
        response = list()
        self.cursor.execute("SELECT * FROM lysins WHERE lysin_name = " + "'" + lysin_name + "';")
        for line in self.cursor.fetchall():
            response.append(line)
        return header, response
    def query_lysins_table_by_conserved_domains(self, conserved_domains):
        # header
        header = list()
        h = self.print_table_syntax('lysins')
        for cell in h:
            header.append(cell[0])
        # rows
        response = list()
        self.cursor.execute("SELECT * FROM lysins WHERE conserved_domains = " + "'" + conserved_domains + "';")
        for line in self.cursor.fetchall():
            response.append(line)
        return header, response
    def query_lysins_table_by_properties(self, properties):
        # header
        header = list()
        h = self.print_table_syntax('lysins')
        for cell in h:
            header.append(cell[0])
        # rows
        response = list()
        self.cursor.execute("SELECT * FROM lysins WHERE properties = " + "'" + properties + "';")
        for line in self.cursor.fetchall():
            response.append(line)
        return header, response

# DB = BiologicalDatabase()
# DB.clear_entire_lysins_table()
# DB.clear_entire_borrelia_table()
#
# DB.add_borrelia_to_borrelia_table(1, 'laure')
# DB.add_borrelia_to_borrelia_table(2, 'dimi')
# DB.add_borrelia_to_borrelia_table(3, 'bjorn')
# DB.add_borrelia_to_borrelia_table(4, 'tom')
# DB.add_borrelia_to_borrelia_table(5, 'simmy the simon')
# DB.add_borrelia_to_borrelia_table(6, 'ondina')
#
#
# DB.add_entry_to_lysins_table(1, 'uniprot1', 'lysinname4', 'conserveddomain1', 'properties2')
# DB.add_entry_to_lysins_table(1, 'uniprot3', 'lysinname5', 'conserveddomain', 'properties')
# DB.add_entry_to_lysins_table(2, 'uniprot9', 'lysinname6', 'conserveddomain3', 'properties5')
# DB.add_entry_to_lysins_table(1, 'uniprot2', 'lysinname5', 'conserveddomain', 'properties4')
# DB.add_entry_to_lysins_table(4, 'uniprot4', 'lysinname3', 'conserveddomain', 'properties3')
# DB.add_entry_to_lysins_table(5, 'uniprot6', 'lysinname2', 'conserveddomain', 'properties2')
# DB.add_entry_to_lysins_table(5, 'uniprot7', 'lysinname5', 'conserveddomain4', 'properties1')
# DB.add_entry_to_lysins_table(1, 'uniprot4', 'lysinname3', 'conserveddomain', 'properties5')
# DB.add_entry_to_lysins_table(5, 'uniprot4', 'lysinname0', 'conserveddomain6', 'properties3')
# DB.add_entry_to_lysins_table(2, 'uniprot6', 'lysinname9', 'conserveddomain', 'properties')
# DB.add_entry_to_lysins_table(4, 'uniprot9', 'lysinname1', 'conserveddomain2', 'properties')
# DB.add_entry_to_lysins_table(5, 'uniprot1', 'lysinname3', 'conserveddomain2', 'properties')
# DB.add_entry_to_lysins_table(3, 'uniprot7', 'lysinname1', 'conserveddomain2', 'properties6')
# DB.add_entry_to_lysins_table(1, 'uniprot6', 'lysinname2', 'conserveddomain5', 'properties6')
# DB.add_entry_to_lysins_table(2, 'uniprot4', 'lysinname6', 'conserveddomain5', 'properties7')
# DB.add_entry_to_lysins_table(5, 'uniprot2', 'lysinname1', 'conserveddomain3', 'properties')
# DB.add_entry_to_lysins_table(4, 'uniprot1', 'lysinname3', 'conserveddomain3', 'properties')
