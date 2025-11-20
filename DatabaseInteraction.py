import psycopg2
import atexit

class DBManager():
    def __init__(self):
        self.dbName = "DatabaseName"
        self.dbUser = "user"
        self.dbPass = "password"
        self.dbHost = "127.0.0.1"
        self.dbPort = "5442"

        self.ConnectToDatabase()
        
        atexit.register(self.ExitHandler)

    def ConnectToDatabase(self):
        try:
            self.conn = psycopg2.connect(database = self.dbName,
                                        user = self.dbUser,
                                        password = self.dbPass,
                                        host = self.dbHost,
                                        port = self.dbPort)
            self.cur = self.conn.cursor()

            print("Database connected successfully")
        except:
            print("Database not connected successfully")

    def ExecuteQuery(self, queryMessage):
        self.cur.execute(queryMessage)
        return self.cur.fetchall()
    
    def ExecuteScript(self, scriptPath):
        with open(scriptPath, "r") as file:
            sqlCommand = file.read()
        
        self.cur.execute(sqlCommand)
        return self.cur.fetchall()

    def CloseDataBase(self):
        self.cur.close()
        self.conn.close()

    def ExitHandler(self):
        self.CloseDataBase()