from ApplicationInterface import UIManager
from DatabaseInteraction import DBManager

 #--- Init Systems ---5
mDatabase = DBManager()
mUI = UIManager(mDatabase)
#---------------------

#---TODO---
#- Add labels or tags to listings to help remember why you favorited that specific home.
#- Feature to compare and contrast homes --> sort of like PC part picker

def main():
   pass

if __name__ == "__main__":
    main()