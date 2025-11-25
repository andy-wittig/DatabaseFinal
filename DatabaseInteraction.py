import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
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
        self.usersTableName = "Users"
        self.favoritesTableName = "Favorites"
        self.currentPageTable = self.listingsTableName
        
        self.sortQueryDict = {
            "PriceHigh" : "SQL_Scripts\SortByPriceHigh.sql",
            "PriceLow" : "SQL_Scripts\SortByPriceLow.sql",
        }

        self.CheckDatabaseExists(self.dbUser, self.dbName, self.dbPass, self.dbHost, self.dbPort)

        self.ConnectToDatabase()
        
        atexit.register(self.ExitHandler)

    def CheckDatabaseExists(self, user, name, password, host, port):
        conn = None
        try:
            conn = psycopg2.connect(
                dbname='postgres',
                user = user,
                password = password,
                host = host,
                port = port
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()

            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (name,))
            
            exists = cur.fetchone()

            if (not exists):
                print(f"Database '{name}' does not exist, creating one.")

                self.ExecuteScript("SQL_Scripts\CreateDatabase.sql", cur)
            else:
                print(f"Database '{name}' already exist, attempting to connect.")

        except psycopg2.Error as e:
            print("Error: ", e)
        finally:
            if (conn): conn.close()

    def ConnectToDatabase(self):
        try:
            self.conn = psycopg2.connect(database = self.dbName,
                                        user = self.dbUser,
                                        password = self.dbPass,
                                        host = self.dbHost,
                                        port = self.dbPort)
            self.cur = self.conn.cursor(cursor_factory = RealDictCursor)

            print("Database connected successfully")
        except psycopg2.Error as e:
            print("Database NOT connected successfully")
            print("Error: ", e)

        self.CheckTablesExist(self.listingsTableName, "SQL_Scripts\CreateListingsTable.sql")
        self.CheckTablesExist(self.usersTableName, "SQL_Scripts\CreateUsersTable.sql")
        self.CheckTablesExist(self.favoritesTableName, "SQL_Scripts\CreateFavoritesTable.sql")

    def CheckTablesExist(self, tableName, scriptPath):
        self.cur.execute("SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = %s;", (tableName,))
        exists = self.cur.fetchone()
        if (not exists):
            print (f"{tableName} table was not found, creating one.")
            self.ExecuteScript(scriptPath)
        else:
            print (f"{tableName} table was found.")
    
    def ExecuteScript(self, scriptPath,  cursor = None):
        if (cursor == None): cursor = self.cur
        
        with open(scriptPath, "r") as file:
            sqlCommand = file.read()
        
        cursor.execute(sqlCommand)
        
        try:
            return cursor.fetchall()
        except psycopg2.ProgrammingError:
            return None

    def GetHomeListingData(self):
        sqlQuery = f'SELECT * FROM public."{self.listingsTableName}";'
        self.cur.execute(sqlQuery)
        rows = self.cur.fetchall()
        return rows
    
    def GetHomePositions(self):
        if (self.currentPageTable == self.listingsTableName):
            sqlQuery = f'SELECT "Longitude", "Latitude" FROM public."{self.listingsTableName}";'
        elif (self.currentPageTable == self.favoritesTableName):
            sqlQuery = f'SELECT "Longitude", "Latitude" FROM public."{self.listingsTableName}" L JOIN public."{self.favoritesTableName}" F ON F."listing_id" = L."ID";'
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
        #print(houseData.columns)

        cols = ['"ID"', '"Bathrooms"', '"Bedrooms"', '"Size"', '"House Category"', '"Price"',
                '"street name"', '"city"', '"state"', '"Latitude"', '"Longitude"', '"InsertedDate"']
        values = [tuple(x) for x in houseData.to_numpy()]

        self.ClearTable(self.listingsTableName)

        sqlCommand = f'INSERT INTO "{self.listingsTableName}" ({', '.join(cols)}) VALUES %s'
        execute_values(self.cur, sqlCommand, values)
        self.conn.commit()

    def AddToFavoritesTable(self, listingID):
        sqlCommand = f'INSERT INTO "{self.favoritesTableName}" (listing_id) VALUES (%s)'
        self.cur.execute(sqlCommand, (listingID,))
        self.conn.commit()

    def GetFavorites(self):
        sqlQuery = f'SELECT L.* FROM public."{self.listingsTableName}" L JOIN public."{self.favoritesTableName}" F ON F."listing_id" = L."ID";'
        self.cur.execute(sqlQuery)
        rows = self.cur.fetchall()
        return rows

    def CloseDataBase(self):
        self.cur.close()
        self.conn.close()

    def ExitHandler(self):
        self.CloseDataBase()