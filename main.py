from ApplicationInterface import UIManager
from DatabaseInteraction import DBManager

 #--- Init Systems ---
mDatabase = DBManager()
mUI = UIManager(mDatabase)
#---------------------

def main():
   pass

if __name__ == "__main__":
    main()