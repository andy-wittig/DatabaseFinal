import psycopg2
from psycopg2.extras import execute_values
import atexit
import pyRealtor

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
        self.conn.commit()
    
    def ExecuteScript(self, scriptPath):
        with open(scriptPath, "r") as file:
            sqlCommand = file.read()
        
        self.cur.execute(sqlCommand)
        self.conn.commit()
    
    def PullHomeListingData(self, _city, _country):
        houseObj = pyRealtor.HousesFacade()
        houseObj.search_save_houses(
            search_area = _city,
            country = _country
        )
        print(houseData.columns)
        
        houseData = houseObj.houses_df #processed data
        cols = list(houseData.columns)
        values = [tuple(x) for x in houseData.to_numpy()]
        tableName = "Listings"

        sqlCommand = f"INSERT INTO {tableName} ({', '.join(cols)}) VALUES %s"
        execute_values(self.cur, sqlCommand, values)
        self.conn.commit()

    def CloseDataBase(self):
        self.cur.close()
        self.conn.close()

    def ExitHandler(self):
        self.CloseDataBase()