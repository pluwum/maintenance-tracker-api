import psycopg2
from exception import DatabaseException


class Database():
    """
    Database Model class to manage database transactions for models
    """

    def __init__(self):
        self.db_user = 'some_password'
        self.db_password = ''
        self.db_name = 'your_db_name'
        self.db_host = 'localhost'
        self.connection = None
        self.cursor = None
        self.table = type(self).__name__
        self.query = None
        self.values = None

    def connect(self, db_name=None):
        """
        connect to the database
        """
        if db_name is None:
            db_name = self.db_name

        try:
            self.connection = psycopg2.connect(
                "dbname={} user={} host={}".format(db_name, self.db_user,
                                                   self.db_host))
            # Activate autocommit mode so we can created db
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except Exception as e:
            raise DatabaseException(str(e))
        return True

    def close(self):
        """
        close db connection
        """
        if self.connection is not None:
            self.connection.close()
            return True
        else:
            return False

    def insert(self, **kwargs):
        """
        Insert data into the database
        """
        self.connect()
        columns = []
        self.values = []

        # Get all the columns passed
        if kwargs is not None:
            for key, value in kwargs.items():
                columns.append(key)
                self.values.append(value)
            value_holders = ['%s'] * len(self.values)

        # Create a commas separated list of columns and place holders
        columns = ','.join(columns)
        value_holders = ','.join(value_holders)

        # Construct the query
        self.query = "INSERT INTO {} ({}) VALUES ({});".format(
            self.table, columns, value_holders)
        return self

    def select(self):
        """
        select items from the database
        """
        self.connect()
        if self.table is None:
            print("No database specified")

        self.query = "SELECT * FROM {}".format(self.table)
        return self

    def where(self, column, value):
        """
        Filter items by column and value
        """
        self.query = self.query + ' WHERE ' + str(column) + ' = ' + str(value)
        return self

    def save(self):
        """
        Persist data to the DB
        """
        try:
            self.connect()
            self.cursor.execute(self.query, self.values)
            self.connection.commit()
            self.close()
            return True
        except Exception as e:
            raise DatabaseException(str(e))

    def get(self):
        """
        Display data from the DB
        """
        try:
            self.connect()
            self.cursor.execute(self.query, self.values)
            rows = self.cursor.fetchall()
            self.close()
            return rows
        except Exception as e:
            raise DatabaseException(str(e))

    def update(self, **kwargs):
        """
        Update items in the database
        """
        self.connect()
        columns = []
        self.values = []

        # Get all the columns passed
        if kwargs is not None:
            for key, value in kwargs.items():
                columns.append(key + "=%s")
                self.values.append(value)

        # Create a commas separated list of columns and place holders
        columns = ','.join(columns)

        # Construct the query
        self.query = "UPDATE {} SET {}".format(self.table, columns)

        return self

    def delete(self, **kwargs):
        """
        Delete an item from the database
        """
        # Construct the query
        self.query = "DELETE FROM {}".format(self.table)
        return self

    def create_db(self, database):
        """
        create a new databases
        """
        self.connect('postgres')
        # Construct the query
        self.query = "CREATE DATABASE {}".format(database)
        self.cursor.execute(self.query, self.values)
        self.connection.commit()
        self.close()

    def create_table(self, **kwargs):
        """
        create a new table with columns
        """
        pass
