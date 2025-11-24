import psycopg2
from psycopg2.extras import execute_values
from psycopg2.extras import RealDictCursor
import atexit
import pyRealtor

class DBManager():
    def __init__(self):
        self.dbName = "HomeBuyer"
        self.dbUser = "postgres"
        self.dbPass = "password"
        self.dbHost = "127.0.0.1"
        self.dbPort = "5432"

        self.listingsTableName = "Listings"
        self.sortQueryDict = {
            "PriceHigh" : "SQL_Scripts\SortByPriceHigh.sql",
            "PriceLow" : "SQL_Scripts\SortByPriceLow.sql",
        }

        self.ConnectToDatabase()
        
        atexit.register(self.ExitHandler)

    def ConnectToDatabase(self):
        try:
            self.conn = psycopg2.connect(database = self.dbName,
                                        user = self.dbUser,
                                        password = self.dbPass,
                                        host = self.dbHost,
                                        port = self.dbPort)
            self.cur = self.conn.cursor(cursor_factory = RealDictCursor)

            print("Database connected successfully")
        except Exception as e:
            print("Database NOT connected successfully")
            print("Error: ", e)
    
    def ExecuteScript(self, scriptPath):
        with open(scriptPath, "r") as file:
            sqlCommand = file.read()
        
        self.cur.execute(sqlCommand)
        rows = self.cur.fetchall()
        
        return rows

    def GetHomeListingData(self):
        sqlQuery = f'SELECT * FROM public."{self.listingsTableName}";'
        self.cur.execute(sqlQuery)
        rows = self.cur.fetchall()
        return rows
    
    def GetHomePositions(self):
        sqlQuery = f'SELECT "Longitude", "Latitude" FROM public."{self.listingsTableName}";'
        self.cur.execute(sqlQuery)
        rows = self.cur.fetchall()
        return rows
    
    def ClearTable(self, tableName):
        self.cur.execute(f'DELETE FROM "{tableName}";')
        self.conn.commit()
    
    def PullHomeListingData(self, _city, _country):
        houseObj = pyRealtor.HousesFacade()
        houseObj.search_save_houses(
            search_area = _city,
            country = _country
        )

        houseData = houseObj.houses_df #processed data
        print(houseData.columns)
        cols = ['"ID"', '"Bathrooms"', '"Bedrooms"', '"Size"', '"House Category"', '"Price"',
                '"street name"', '"city"', '"state"', '"Latitude"', '"Longitude"', '"InsertedDate"']
        values = [tuple(x) for x in houseData.to_numpy()]

        self.ClearTable(self.listingsTableName)

        sqlCommand = f'INSERT INTO "{self.listingsTableName}" ({', '.join(cols)}) VALUES %s'
        execute_values(self.cur, sqlCommand, values)
        self.conn.commit()

    def CloseDataBase(self):
        self.cur.close()
        self.conn.close()

    def ExitHandler(self):
        self.CloseDataBase()