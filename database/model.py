import sqlite3
import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from utils.globals import DB_PATH, DB_NAME
from utils.encryption import Encryption
from database.tables import Tables, TableEnum

class Model:
    def __init__(self, db_path: str = f"{DB_PATH}{DB_NAME}"):
        try:
            self.db = sqlite3.connect(db_path)
        except sqlite3.OperationalError:
            raise Exception
        self.cur = self.db.cursor()

        self.create_key_table()
        key = self.get_key()
        self.encryption = Encryption(key)
        
        self.create_table_names() 
        self.create_tables() # create the tables
        self.migrate_table_columns() # add new columns to tables if needed
        self.fill_defaults()
    
    def create_key_table(self):      
        table_query = f"""
            CREATE TABLE IF NOT EXISTS trustlock (
                name TEXT UNIQUE,
                value TEXT
            )
        """
        self.cur.execute(table_query)
        
    def migrate_table_columns(self):
        tables = Tables.tablesDict
        
        for table in tables:
            encrypted_cols = self.get_encrypted_table_cols(table)
            columns = tables[table]
            
            for column in columns:

                if column not in encrypted_cols:
                    print(encrypted_cols)
                    self.add_column(table, column, Tables.tablesDict[table][column])
                    encrypted_colsA = self.get_encrypted_table_cols(table)
                    print(encrypted_colsA)


    def get_key(self):
        key = self.read_key()
        encrypt_key = Encryption.encrypted_key()
        if(len(key) < 1):
            query = "INSERT INTO trustlock (name, value) VALUES (?, ?)"
            self.cur.execute(query, ['trustlock', f'[{encrypt_key}]'])
        else:
            return key[0][0]
        return encrypt_key
    
    def read_key(self):
        query = """
            SELECT value FROM trustlock;
        """
        self.cur.execute(query)
        return self.cur.fetchall()
        
    def create_tables(self):    
        self.create_table(TableEnum.groups,     Tables.groups)
        self.create_table(TableEnum.user,       Tables.user)
        self.create_table(TableEnum.settings,   Tables.settings)
        self.create_table(TableEnum.metadata,   Tables.metadata)
        self.create_table(TableEnum.apps,       Tables.apps,    "group_id", "groups", "id")
        self.create_table(TableEnum.notes,      Tables.notes,   "group_id", "groups", "id")
        self.create_table(TableEnum.todos,      Tables.todos,   "group_id", "groups", "id")
        self.create_table(TableEnum.vault,      Tables.vault,   "group_id", "groups", "id")
        
    def create_table(self, tablename: TableEnum, fields: object, foreign_field: str = None, foreign_tablename: str = None, foreign_table_field: str = None):
        encrypted_table_name = self.encryption.encrypt(tablename.name)
        
        new_table = self.insert_table_name(encrypted_table_name)
        
        names = list(fields.keys())
        definitions = list(fields.values())
        
        table_definition = ""
        encrypted_foreign_key = ""
        
        for i in range(len(names)):
            encrypted_name = self.encryption.encrypt(names[i])
            if names[i] == foreign_field:
                encrypted_foreign_key = encrypted_name
            table_definition += f"[{encrypted_name}] {definitions[i]}"
            if i < len(names) - 1 and not foreign_field: table_definition += ",\n\t\t"
            elif foreign_field: table_definition += ",\n\t\t"
            
        # Create a string to contain the foreign key definition
        foreign_definition = ""
        
        # Make sure you have all the data for the foreign key before continuing
        if foreign_field and foreign_table_field and foreign_tablename and encrypted_foreign_key:
            
            # Get the encrypted table name for the foreign table
            encrypted_foreign_tablename = self.get_encrypted_table_name(foreign_tablename)
            
            # Get the encrypted table field names for the table
            encrypted_foreign_table_fields = self.get_encrypted_table_cols(foreign_tablename)
            
            # Get the encrypted table field name for the table
            encrypted_foreign_table_field = encrypted_foreign_table_fields[foreign_table_field]
            
            # Construct the foreign key definition
            foreign_definition = f"FOREIGN KEY ([{encrypted_foreign_key}]) REFERENCES [{encrypted_foreign_tablename}]([{encrypted_foreign_table_field}])"

        table_query = f"""
            CREATE TABLE IF NOT EXISTS [{encrypted_table_name}](
                {table_definition}
                {foreign_definition}
                
            )
        """

        if new_table: self.cur.execute(table_query)

    def save(self, table, data, close=True):
        # Generate the question marks required for parameterized queries
        values = ", ".join(list(map(lambda v: "?", data.keys())))
        
        # Get the encrypted names of the columns and table
        table_cols = self.get_encrypted_table_cols(table)
        encrypted_tablename = self.get_encrypted_table_name(table)
        
        field_name_list = []
        for name in list(data.keys()):
            # If the column exists in the table add the encrypted name to list
            if name in table_cols: 
                field_name_list.append(f"[{table_cols[name]}]")
            # Throw an error if an invalid column name was passed to this method
            else:
                raise Exception("Invalid colum name provided")
                
        # Create a string from the encrypted column names that will be used to reference the columns names 
        keys = ", ".join(field_name_list)
        
        # encrypt the data and add it to the list of data that must be added
        values_list = []
        for entry in data.values():
            values_list.append(f'{self.encryption.encrypt(entry)}')
        
        # Convert to tuple for proper sqlite handling
        values_list = tuple(values_list)
            
        query = f"INSERT INTO [{encrypted_tablename}]({keys}) VALUES ({values})"

        self.cur.executemany(query, [values_list])
        self.db.commit()
        
        # if close: self.db.close()
        
        

    def read(self, table):
        if table != "tablenames":
            encrypted_table = self.get_encrypted_table_name(table)
            
        query = f"SELECT * FROM [{encrypted_table}]"
        self.cur.execute(query)
        data = self.cur.fetchall()
        
        decrypted_data = []
        if table != "tablenames":
            for entry in data:
                entry_list = []
                for i in range(len(list(entry))):
                    if (table == "user" or table == "settings"):
                            decrypted = self.encryption.decrypt(entry[i])
                            entry_list.append(decrypted)
                    else:
                        if i > 0:
                            decrypted = self.encryption.decrypt(entry[i])
                            entry_list.append(decrypted)
                        else:
                            entry_list.append(entry[i])
                decrypted_data.append(entry_list)
            
        self.db.close()

        return decrypted_data
    
    def delete(self, table, id):
        encrypted_table = self.get_encrypted_table_name(table)
        
        encrypted_cols = self.get_encrypted_table_cols(table)
        query = f"DELETE FROM [{encrypted_table}] WHERE [{encrypted_cols['id']}] = (?)"
        
        self.cur.execute(query, (id,))
        self.db.commit()
        self.db.close()

    def update(self, table, data, id):
        # Get the field names
        fields = data.keys()
        # Get the encrypted cols
        encrypted_cols = self.get_encrypted_table_cols(table)
        
        # Create list of encrypted values and append id for query
        values = list(map(lambda v: f"[{self.encryption.encrypt(v)}]", list(data.values())))
        
        if id == "settings" or id == "user":
            encrypted_id = self.get_config_table_id(id)
            values.append(f"{encrypted_id}")
        else:
            values.append(id)
        
        # Create the data string that will set the data in the query
        data_string_list = []
        for field in fields:
            if field in encrypted_cols:
                data_string_list.append(f"[{encrypted_cols[field]}] = ?")
            else:
                raise Exception(" Invalid column name provided")
        data_string = ", ".join(data_string_list)
        
        # Get the encrypted table name
        encrypted_table = self.get_encrypted_table_name(table)
 
        query = f"UPDATE [{encrypted_table}] SET {data_string} WHERE [{encrypted_cols['id']}] = ?"
        self.cur.execute(query, values)

        self.db.commit()
        self.db.close()

    def clearTable(self, table):
        encrypted_table_name = self.get_encrypted_table_name(table)
        query = f"""
            DROP TABLE IF EXISTS [{encrypted_table_name}]
        """
        self.cur.execute(query)
        self.db.commit()
        self.db.close()
        
    # Start fixing from here
    def reset(self):
        query = """
            UPDATE settings SET nightmode = 0, font = 'Arial', color = '#000000' WHERE id = 'settings'
        """

        self.cur.execute(query)
        self.db.commit()
        self.db.close()

    def add_column(self, table_name, column_name, column_definition):
        encrypted_table_name = self.get_encrypted_table_name(table_name)
        
        encrypted_column_name = self.encryption.encrypt(column_name)
        query = f"ALTER TABLE [{encrypted_table_name}] ADD [{encrypted_column_name}] {column_definition}"
        self.cur.execute(query)
        
    def delete_column(self, table: str, column: str):
        encrypted_table_name: str = self.get_encrypted_table_name(table)
        encrypted_column_name: str or None = None
        
        encrypted_column_names: object = self.get_encrypted_table_cols(table)
        if column in encrypted_column_names:
            encrypted_column_name = encrypted_column_names[column]
        
        query = f"ALTER TABLE [{encrypted_table_name}] DROP COLUMN [{encrypted_column_name}]"
        
        if encrypted_column_name:
            self.cur.execute(query)
            self.db.commit()
            self.db.close()
        
    
    def drop_table(self, table):
        self.cur.execute(f"DROP TABLE {table}")
        
    def create_table_names(self):
        query = """CREATE TABLE IF NOT EXISTS tablenames(
                name TEXT NOT NULL
            )"""
        self.cur.execute(query)
    
    # Insert the table names in the table that tracks the table names
    def insert_table_name(self, value: str):
        get_query = "SELECT * FROM tablenames"
        self.cur.execute(get_query)
        tables = self.cur.fetchall()
        
        for table in tables:
            existing_decrypted_table = self.encryption.decrypt(table[0])
            decrypted_table = self.encryption.decrypt(value)
            if existing_decrypted_table == decrypted_table:
                return False
        
        query = "INSERT INTO tablenames (name) VALUES (?)"
        self.cur.execute(query, (value,))
        self.db.commit()
        return True


    def get_encrypted_table_name(self, tablename):
        self.cur.execute("SELECT * FROM tablenames")
        tables = self.cur.fetchall()
        
        for table in tables:
            decrypted_table = self.encryption.decrypt(table[0])
            if tablename == decrypted_table:
                return table[0]
            
        return None
    
    # get a dict of the table names that map to the encrypted table names
    def get_encrypted_table_cols(self, table: str) -> object:
        decrypted_table = self.get_encrypted_table_name(table)
        
        query = f"SELECT * FROM [{decrypted_table}]"
        data = self.cur.execute(query)
        table_columns = {}
        
        for meta in data.description:
            name = self.encryption.decrypt(meta[0])
            table_columns[name] = meta[0]
            
        return table_columns
    
    def get_config_table_id(self, table):
        tablename = self.get_encrypted_table_name(table)
        
        query = f"SELECT * FROM [{tablename}]"
        
        self.cur.execute(query)
        data = self.cur.fetchall()
        return data[0][0]
    
    def create_defaults(self, tablename, initial_data, close_db=False):
        
        enc_tablename = self.get_encrypted_table_name(tablename)
        get_query = f"SELECT * FROM [{enc_tablename}]"
        
        self.cur.execute(get_query)
        
        table_data = self.cur.fetchall()
        
        if(len(table_data) > 0):
            return
        
        self.save(tablename, initial_data, close_db)
        
        
    
    def fill_defaults(self):
        
        default_settings = {
            'id': 'settings',
            'nightmode': "0",
            'font': 'Roboto Condensed',
            'color': '#000000',
            'vault_on': '0',
            'timer': '30',
            'calendar': '0',
            'twofa': '0',
            'auto_save': json.dumps({ "google": False, "onedrive": False })
        }
        
        default_groups = {
            'name': 'Ungrouped',
            'description': 'Anything that is not in a group'
        }        
        
        self.create_defaults('settings', default_settings)
        # self.create_defaults('user', {'id': 'user'})
        self.create_defaults('groups', default_groups, True)

    def valid_account(self, db_path):
        valid_db = Model.valid_database(db_path)
        
        if(not valid_db):
            return [False, "The database is corrupted or not a valid Trust Lock database"]
        
        new_user = Model(db_path).read("user")
        
        if(len(new_user) < 1):
            return [False, "User not found in database"]
        
        passphrase = self.read("user")[0][4]
        
        if(passphrase != new_user[0][4]):
            return [False, "Trying to import incorrect account."]
        
        return [True, None]
        
    @staticmethod 
    def valid_database(db_path):
        new_db = None
        try:
           new_db = Model(db_path)
        except Exception:
            return False
        
        # Check db integrity
        new_db.cur.execute("PRAGMA integrity_check;")
        
        # Make sure the integrity is ok
        integrity_check = new_db.cur.fetchone()
        if(integrity_check[0] != "ok"):
            return False
        
        return True
    
model = Model()
for app in model.read("apps"):
    print(app)
# model.update("settings", {"font": "Roboto Condensed"}, "settings")
# model.update("settings", {"font": "Proxon"}, "settings")
