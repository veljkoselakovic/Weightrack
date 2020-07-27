import binascii
import hashlib
import os
import sqlite3
import string
import smtplib
import ssl
import uuid
from random import choice, randint
import yaml

from DBInfo import DBInfo
from weight import Weight


def create_connection(db_file):
    """
    Create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
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
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        print(e)


create_commands = """ CREATE TABLE IF NOT EXISTS Accounts (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    surname text NOT NULL,
                                    username text NOT NULL UNIQUE,
                                    salt text NOT NULL,
                                    pwd text NOT NULL UNIQUE,
                                    email text NOT NULL UNIQUE,
                                    height real,
                                    weight real,
                                    state text NOT NULL,    
                                    uID text UNIQUE                           
                                ); """

arg = """ INSERT INTO Accounts (name, surname, username, salt, pwd, email, height, weight, state, uID)
            VALUES(?,?,?,?,?,?,?,?,?,?)"""


def get_random_string(length):
    """
    Create a random string
    :param length: length of the string
    :return: a random string
    """
    letters = string.ascii_lowercase
    result_str = ''.join(choice(letters) for i in range(length))
    return result_str


def hash_password(password):
    """
    Hash a password for storing.
    :param password: plain text password
    :return: an array in which the first 64 elements represent the salt, and the second represent the hashed pwd itself
    """
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


class Account():
    """
    Main class for now
    """

    def __init__(self, name=None, surname=None, username=None, passwd=None, email=None, height=None, weight=None,
                 state='metric'):
        """
        Constructor for a first time user if username is given, or an empty constructor otherwise
        :param name: name
        :param surname: surname
        :param username: username -REQUIRED FOR A NEW USER @TODO: add name, surname and email to required parameters
        :param email: email
        :param height: height @TODO: add a height class for imperial/metric conversion on the fly
        :param weight: weight Class already implemented, @TODO: Test thoroughly
        :param state: metric/imperial measurement standard @TODO: Rename/Refactor to something more descriptive
        @TODO: Reorganize the code into smaller, more readable parts
        @TODO: Detailed comments
        """
        if username is not None:
            self.name = name
            self.surname = surname
            self.username = username
            self.uID = uuid.uuid4()
            self.email = email
            if len(passwd) < 8:
                raise Exception("Password too short. Minimum length is 8 characters")
            pwd = hash_password(passwd)
            salt = pwd[:64]
            stPwd = pwd[64:]

            self.DBInfo = DBInfo(uID=self.uID)
            conn = create_connection("Acc.db")
            create_table(conn, create_commands)
            cur = conn.cursor()
            cur.execute(arg, (name, surname, username, salt, stPwd, email, height, weight, state, str(self.uID)))
            conn.commit()
            if height is None:
                self.height = -1
            else:
                self.height = height
            if weight is None:
                self.weight = None
            else:
                self.weight = Weight(weight, state=state)

    def logIn(self, username, pwd):
        """
        Logs in a user
        :param username: username
        :param pwd: password
        :return: None @TODO: Maybe return True/False?
                            (Exceptions implemented, don't think it's worth doing)
        @TODO: Detailed comments
        """
        conn = create_connection("Acc.db")
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM Accounts WHERE Accounts.username=?", (username,))
        except sqlite3.OperationalError:
            raise Exception("User doesn't exist")
        rows = cur.fetchall()
        for row in rows:
            salt = row[4]
            stPwd = row[5]
            pwdhash = hashlib.pbkdf2_hmac('sha512', pwd.encode('utf-8'), salt.encode('ascii'), 100000)
            pwdhash = binascii.hexlify(pwdhash).decode('ascii')
            print()
            if pwdhash != stPwd:
                raise Exception("Invalid password")

            self.name = row[1]
            self.surname = row[2]
            self.username = row[3]
            self.email = row[6]
            self.height = row[7]
            self.weight = Weight(row[8], row[9])
            self.uID = row[10]

        self.DBInfo = DBInfo(self.uID)

    def __repr__(self):
        """
        String representation of the Account class
        :return: Returns the uID for now @TODO: A nice log for the developer maybe
        """
        return str(self.uID)

    def measure(self, wght):
        """
        Measure current body mass
        :param wght: New mass in preferred unit @TODO: Test with different standard
        :return: None
        """
        self.weight.set(wght)
        self.DBInfo.add(wght)

    @staticmethod
    def resetPassword(email):
        """
        STATIC METHOD
        Resets the password for the given email after verification
        :param email: email
        :return:
        @TODO: Improve the email server/gmail account handling (NO HARDCODED PASSWORDS)
        @TODO: Detailed comments
        """

        port = 465  # For SSL
        # Create a secure SSL context
        context = ssl.create_default_context()

        strchk = get_random_string(randint(5, 10))
        conf = yaml.safe_load(open('conf/application.yml'))
        senderemail = conf['user']['email']
        senderpwd = conf['user']['password']
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(senderemail, senderpwd)
            server.sendmail("wfaccloss@gmail.com", email, "Subject: Password recovery string: \n\n" + strchk)

        chckinput = input("Input the code that was sent to your email: ")
        if strchk == chckinput:
            newpwd = input("Enter your new password: ")
            if len(newpwd) < 8:
                raise Exception("Password too short. Minimum length is 8 characters")
            pwd = hash_password(newpwd)
            salt = pwd[:64]
            stPwd = pwd[64:]
            conn = create_connection("Acc.db")
            create_table(conn, create_commands)
            cur = conn.cursor()
            cur.execute("UPDATE Accounts SET salt = ?, pwd = ? WHERE email = ?", (salt, stPwd, email))
            conn.commit()
            cur.close()
        else:
            raise Exception("Wrong recovery code")

    def resetEmail(self, newmail):
        """
        Resets the email
        :param newmail: New email
        :return: None
        @TODO: Confirmation of email
        """
        conn = create_connection("Acc.db")
        create_table(conn, create_commands)
        cur = conn.cursor()
        cur.execute("UPDATE Accounts set email = ? WHERE username = ?", (newmail, self.username))
        conn.commit()
        cur.close()

    def display(self):
        """
        Displays the collected data in a chart
        :return: None
        @TODO: Implement this in the GUI
        @TODO: Different types of charts?
        @TODO: Detailed comments
        """
        import matplotlib.pyplot as plt
        wghts = self.DBInfo.allWeights()
        w = []
        for i in wghts:
            w.append(i[0])
            print(i)
        dates = self.DBInfo.allDates()
        k = []
        import numpy as np
        for i in dates:
            k.append(i[0])
            # i = i[0].split()
            # k.append(i[1][3:])
            print(type(i))

        print(k)
        plt.plot(k, w, linestyle='-', linewidth=1, color='red')
        plt.title(self.username)
        # plt.xticks(np.arange(0, 60, step=5))
        plt.show()


# @TODO: Username is already taken error
# @TODO: Confirmation of email when registering
# @TODO: Email confirmation when changing email
# @TODO: Variable height
# @TODO: BIG ONE GUI
# @TODO: Overall more detailed comments
# @TODO: Better exception handling
# @TODO: DJANGO vs Remi vs offline only
'''Far future todos'''
# @TODO: Add a table with nutrients?
# @TODO: Connection with MyFitnessPal
# @TODO: Connection with Mi API
