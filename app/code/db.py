import sqlite3


class GithubDatabase(object):

    def __init__(self, db=None):
        """
            Create SQLite database connection and cursor.
        """
        if db is None:
            self.db = "../db/github.db"
        else:
            self.db = db
        self.conn = sqlite3.connect(self.db)
        self.cur = self.conn.cursor()
        self.connected = True

    def insert_many(self, rows):
        """
            Inserts several rows to the USERS table.
        """
        sql = "INSERT INTO USERS \
                (USERNAME, ID, IMAGE_URL, TYPE, URL) \
                VALUES (?, ?, ?, ?, ?) \
                ON CONFLICT(ID) DO UPDATE SET \
                    USERNAME=EXCLUDED.USERNAME, \
                    IMAGE_URL=EXCLUDED.IMAGE_URL, \
                    TYPE=EXCLUDED.TYPE, \
                    URL=EXCLUDED.URL"
        self.cur.executemany(sql, rows)
        self.conn.commit()
        row_count = self.cur.rowcount
        return row_count

    def create_table(self):
        """
            Creates USERS table in case it doesn't exist.
        """
        self.cur.execute('''CREATE TABLE IF NOT EXISTS USERS
        (USERNAME   TEXT            NOT NULL,
        ID          INT PRIMARY KEY NOT NULL,
        IMAGE_URL   TEXT,
        TYPE        TEXT            NOT NULL,
        URL         TEXT);''')
        self.conn.commit()

    def get_records(self, limit=0, perpage=25):
        """
            Get data from the database.
            Params:
                - limit. Starting record from the results
                - perpage. The number of records in each request
            Returns:
                - A list of tuple(s) with the row(s) retrieved
        """
        if perpage is None:
            # All records needed with no pagination
            self.select = self.cur.execute("SELECT * FROM USERS \
                ORDER BY ID")
        else:
            self.select = self.cur.execute("SELECT * FROM USERS \
                ORDER BY ID LIMIT ?, ?", (limit, perpage))
        return self.select.fetchall()

    def get_username(self, username):
        """
            Gets one record from a specific user.
        """
        self.select = self.cur.execute("SELECT * FROM USERS \
            WHERE USERNAME=?", (username,))
        return self.select.fetchall()

    def close(self):

        self.conn.close()
        self.connected = False
