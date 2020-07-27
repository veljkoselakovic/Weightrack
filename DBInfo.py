import sqlite3


def create_connection(db_file):
    """
        Create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    @TODO: REMOVE THIS FUNCTION, USE THE IDENTICAL ONE IN ACCOUNT
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """
    Create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    @TODO: REMOVE THIS FUNCTION, USE THE IDENTICAL ONE IN ACCOUNT
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        print(e)


create_commands = """ CREATE TABLE IF NOT EXISTS WeightTrack (
                                    id integer PRIMARY KEY,
                                    weight REAL NOT NULL,
                                    date text                                    
                                ); """


class DBInfo():
    """
    Class for handling user's weight database
    @TODO: Rename/Refactor variable names, amount is weird?
    @TODO: Detailed comments
    """

    def __init__(self, uID):
        """
        Constructor
        :param uID: User's unique ID string
        """
        self.uID = uID
        self.conn = create_connection(str(uID) + ".db")
        create_table(self.conn, create_commands)

    def add(self, amount):
        """
        Add a weight to the database, uses the current datetime
        :param amount: amount to be added
        :return: None
        @TODO: Add weights with custom dates
        """
        cur = self.conn.cursor()
        cur.execute("INSERT INTO WeightTrack (weight, date) VALUES(?, DATETIME('now', 'localtime'))", (amount,))
        self.conn.commit()

    def allWeights(self):
        """
        Returns a list of all weights in the database
        :return: list of weights
        """
        cur = self.conn.cursor()
        cur.execute("SELECT weight FROM WeightTrack")
        wghts = cur.fetchall()
        return wghts

    def allDates(self):
        """
        Returns a list of all dates in the database
        :return: list of dates
        """
        cur = self.conn.cursor()
        cur.execute("SELECT date FROM WeightTrack")
        dates = cur.fetchall()
        return dates
