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

        self.listingsTableName = "Listings"

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
    
    def ExecuteScript(self, scriptPath):
        with open(scriptPath, "r") as file:
            sqlCommand = file.read()
        
        self.cur.execute(sqlCommand)
        self.conn.commit()

    def GetHomeListingData(self):
        sqlQuery = f"SELECT * FROM {self.listingsTableName};"
        self.cur.execute(sqlQuery)
        rows = self.cur.fetchall()
        return rows
    
    def PullHomeListingData(self, _city, _country):
        houseObj = pyRealtor.HousesFacade()
        houseObj.search_save_houses(
            search_area = _city,
            country = _country
        )

        houseData = houseObj.houses_df #processed data
        print(houseData.columns)
        cols = list(houseData.columns)
        values = [tuple(x) for x in houseData.to_numpy()]

        sqlCommand = f"INSERT INTO {self.listingsTableName} ({', '.join(cols)}) VALUES %s"
        execute_values(self.cur, sqlCommand, values)
        self.conn.commit()

    def CloseDataBase(self):
        self.cur.close()
        self.conn.close()

    def ExitHandler(self):
        self.CloseDataBase()