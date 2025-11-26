import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter import font
from tkinter import ttk
import math
from KMeansClustering import KMeansClusteringManager
from fpdf import FPDF
from tkinter import filedialog

#User-Defined Routines lets one write wrapped-up SQL statements that can be started from application but run inside of Database. 

class UIManager():
    def __init__(self, databaseManager):
        self.applicationName = "Home Buyer Helper"
        self.databaseManager = databaseManager

        self.root = tk.Tk()

        #--- Style Variables ---
        self.defaultSize = [1280, 720]

        self.titleFont = font.Font(family = "Helvetica", size = 18, weight = "bold")
        self.buttonFont = font.Font(family = "Helvetica", size = 16)
        self.smallButtonFont = font.Font(family = "Helvetica", size = 10)
        self.textFont = font.Font(family = "Helvetica", size = 12)
        self.pageSize = 50

        self.bgColor      = "#3D3D3D"
        self.highlightColor = "#B22222"
        self.panelColor   = "#666666"
        self.elementColor = "#898989"
        self.textColor    = "#E0E0E0"
        #-----------------------

        #--- kmc Variables ----
        self.kmcGroupCount = 1
        self.kmcGroupCountOptions = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        #----------------------

        #--- User Variables ----
        self.userValues = []
        self.currentUser = ''
        #-----------------------

        self.SetupWindow()

        self.root.mainloop()

    def SetupWindow(self):
        self.root.title(self.applicationName)
        self.root.geometry(f"{self.defaultSize[0]}x{self.defaultSize[1]}")

        #--- Initialize Three Column Frames ---
        self.root.columnconfigure(0, weight = 1)
        self.root.columnconfigure(1, weight = 1)
        self.root.columnconfigure(2, weight = 1)
        self.root.rowconfigure(0, weight = 1)

        self.root.configure(bg=self.bgColor)
        self.exportFrame = tk.Frame(self.root, bg = self.bgColor)
        self.homeListingsFrame = tk.Frame(self.root, bg = self.bgColor)
        self.organizationOptionsFrame = tk.Frame(self.root, bg = self.bgColor)

        #Don't allow children widgets of frames to force expansion
        self.exportFrame.pack_propagate(0)
        self.homeListingsFrame.pack_propagate(0)
        self.organizationOptionsFrame.pack_propagate(0)

        self.exportFrame.grid               (row = 0, column = 0, sticky = "nsew", padx = 5, pady = 5)
        self.homeListingsFrame.grid         (row = 0, column = 1, sticky = "nsew", padx = 5, pady = 5)
        self.organizationOptionsFrame.grid  (row = 0, column = 2, sticky = "nsew", padx = 5, pady = 5)
        #--------------------------------------

        #--- Setup Frame Widgets ---
        self.SetupExportWidgets()
        self.SetupHomeListingsWidgets()
        self.SetupOrganizationOptionsWidgets()
        #--------------------------

        self.SetupDefaultUser()
        
    def SetupExportWidgets(self):
        self.exportPreview = scrolledtext.ScrolledText(self.exportFrame, bg=self.panelColor, fg = self.textColor, font = self.textFont,
                                                        state="normal", wrap = tk.WORD,
                                                        padx = 10, pady = 10)

        self.exportButton = tk.Button(self.exportFrame, text = "Export", 
                                      bg = self.elementColor, fg = self.textColor, font = self.buttonFont, command = self.Export)

        self.exportTitleLabel = tk.Label(self.exportFrame, text="Export Home Listings", 
                                    bg = self.bgColor, fg = self.textColor, font = self.titleFont)

        self.exportTitleLabel.pack()
        self.exportPreview.pack(fill = "both", expand = True)
        self.exportButton.pack(fill = "x")

    def SetupHomeListingsWidgets(self):
        self.homeListingsTitleLabel = tk.Label(self.homeListingsFrame, text="Home Listings",
                                           bg = self.bgColor, fg = self.textColor, font = self.titleFont)
        
        #Page Options
        self.pageOptionsContainer = tk.Frame(self.homeListingsFrame)
        self.pageOptionsLabel = tk.Label(self.pageOptionsContainer, text="Page View:",
                                           bg = self.panelColor, fg = self.textColor, font = self.textFont)
        self.pageSelectLabel = tk.Label(self.pageOptionsContainer, text="Page Number:",
                                           bg = self.panelColor, fg = self.textColor, font = self.textFont)
        self.pageOptions = ['Find Listings', 'My Favorites']
        self.pageTypeCombobox = ttk.Combobox(self.pageOptionsContainer, values = self.pageOptions)
        self.pageTypeCombobox.bind("<<ComboboxSelected>>", self.PageTypeSelected)

        self.combobox = ttk.Combobox(self.pageOptionsContainer, values = [])
        self.combobox.bind("<<ComboboxSelected>>", self.ComboboxSelected)

        #Scrolling Container
        self.listingsContainer = tk.Frame(self.homeListingsFrame)
        self.listingsCanvas = tk.Canvas(self.listingsContainer, bg = self.panelColor)
        self.listingsScrollBar = ttk.Scrollbar(self.listingsContainer, orient = "vertical", command = self.listingsCanvas.yview)
        
        #Generate Listings
        self.TextBoxContainer = tk.Frame(self.homeListingsFrame)
        self.cityTextBox = tk.Entry(self.TextBoxContainer, bg = self.elementColor, font = self.textFont)
        self.countryTextBox = tk.Entry(self.TextBoxContainer, bg = self.elementColor, font = self.textFont)
        self.generateListingsButton = tk.Button(self.homeListingsFrame, text = "Generate Listings", 
                                      bg = self.elementColor, fg = self.textColor, font = self.buttonFont, command = self.GenerateListings)
        
        self.cityTextBox.insert(0, 'Sparks')
        self.countryTextBox.insert(0, 'United States')
        
        #Scrollable Frame
        self.scrollableFrame = tk.Frame(self.listingsCanvas, bg = self.panelColor)
        self.scrollableFrameID = self.listingsCanvas.create_window((0, 0), window = self.scrollableFrame, anchor = "nw")
        
        self.listingsCanvas.configure(yscrollcommand = self.listingsScrollBar.set)
        self.scrollableFrame.bind( #This will update the scrolling region size when frame gets updated
            "<Configure>",
            lambda e: self.listingsCanvas.configure(scrollregion = self.listingsCanvas.bbox("all"))
        )
  
        self.listingsCanvas.bind(
            "<Configure>",
            lambda e: self.listingsCanvas.itemconfig(self.scrollableFrameID, width = e.width)
        )
        
        #---Packing---
        self.homeListingsTitleLabel.pack()

        self.pageOptionsContainer.grid_columnconfigure(0, weight = 1)
        self.pageOptionsContainer.grid_columnconfigure(1, weight = 1)
        self.pageOptionsContainer.grid_columnconfigure(2, weight = 1)
        self.pageOptionsContainer.grid_columnconfigure(3, weight = 1)
        self.pageOptionsContainer.pack()
        self.pageOptionsLabel.grid(row = 0, column = 0)
        self.pageTypeCombobox.grid(row = 0, column = 1)
        self.pageSelectLabel.grid(row = 0, column = 2)
        self.combobox.grid(row = 0, column = 3)

        self.listingsContainer.pack(fill = "both", expand = True)
        self.listingsCanvas.pack(side = "left", fill = "both", expand = True)
        self.listingsScrollBar.pack(side = "right", fill = "y")

        self.TextBoxContainer.pack(fill = "x")
        self.cityTextBox.pack(side = "left", expand = True, fill = "x", padx = 5)
        self.countryTextBox.pack(side = "left", expand = True, fill = "x", padx = 5)
        self.generateListingsButton.pack(fill = "x")

    def SetupOrganizationOptionsWidgets(self):
        self.organizationOptionsTitleLabel = tk.Label(self.organizationOptionsFrame, text="Organize Listings",
                                                  bg = self.bgColor, fg = self.textColor, font = self.titleFont)
        
        #Add New User
        self.userValues = self.databaseManager.GetUsers()

        self.selectUserFrame = tk.Frame(self.organizationOptionsFrame, bg = self.panelColor)
        self.userSelectLabel = tk.Label(self.selectUserFrame, text="Select User: ",
                                                  bg = self.panelColor, fg = self.textColor, font = self.textFont)
        self.userCombobox = ttk.Combobox(self.selectUserFrame, values = self.userValues)
        self.userCombobox.bind("<<ComboboxSelected>>", self.UserSelected)
        self.addUserFrame = tk.Frame(self.organizationOptionsFrame, bg = self.panelColor)
        self.userEntryBox = tk.Entry(self.addUserFrame, bg = self.elementColor, font = self.textFont)
        self.addUserButton = tk.Button(self.addUserFrame, text = "Add User", 
                                      bg = self.elementColor, fg = self.textColor, font = self.buttonFont, command = lambda: self.AddUser())
        
        self.removeUserButton = tk.Button(self.organizationOptionsFrame, text = "Remove User", 
                                      bg = self.elementColor, fg = self.textColor, font = self.buttonFont, command = lambda: self.RemoveUser())

        #Sort By Options
        self.SortPriceHighButton = tk.Button(self.organizationOptionsFrame, text = "Sort by Price: Highest", 
                                      bg = self.elementColor, fg = self.textColor, font = self.buttonFont, command = lambda: self.SortBy("PriceHigh"))
        self.SortPriceLowButton = tk.Button(self.organizationOptionsFrame, text = "Sort by Price: Lowest", 
                                      bg = self.elementColor, fg = self.textColor, font = self.buttonFont, command = lambda: self.SortBy("PriceLow"))
        
        #kmc Grouping
        self.kmcFrame = tk.Frame(self.organizationOptionsFrame, bg = self.panelColor)
        self.kmcCombobox = ttk.Combobox(self.kmcFrame, values = self.kmcGroupCountOptions)
        self.kmcCombobox.bind("<<ComboboxSelected>>", self.KMCComboboxSelected)
        self.kmcRunButton = tk.Button(self.kmcFrame, text = "Run kmc Algorithm", 
                                      bg = self.elementColor, fg = self.textColor, font = self.buttonFont, command = lambda: self.RunKMC())

        #Packing
        self.organizationOptionsTitleLabel.pack()

        self.selectUserFrame.pack(padx = 5, pady = 5)
        self.userSelectLabel.pack(fill = "x", expand = True, side = "left")
        self.userCombobox.pack(fill = "x", expand = True, side = "right")

        self.addUserFrame.pack(padx = 5, pady = 5)
        self.userEntryBox.pack(fill = "x", expand = True, side = "left")
        self.addUserButton.pack(fill = "x", expand = True, side = "right")
        self.removeUserButton.pack(padx = 5, pady = 5)

        self.spacerFrame = tk.Frame(self.organizationOptionsFrame)
        self.spacerFrame.pack(pady = 40)

        self.SortPriceHighButton.pack(anchor = "w", pady = 5)
        self.SortPriceLowButton.pack(anchor = "w", pady = 5)

        self.kmcFrame.pack(anchor = "w", pady = 10)
        self.kmcCombobox.pack(side = "left")
        self.kmcRunButton.pack(side = "right")

    def AddExportPreviewText(self, text): #Enables and re-enables text-scrollable widget to not allow user input.
        self.exportPreview.delete("1.0", tk.END) #Erases all text content from starting index to end.
        self.exportPreview.config(state = "normal")
        self.exportPreview.insert(tk.END, text)
        self.exportPreview.config(state = "disabled")

    def ClearFrame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def KMCComboboxSelected(self, event):
        self.kmcGroupCount = int(self.kmcCombobox.get())

    def RunKMC(self):
        positionData = self.databaseManager.GetHomePositions(self.currentUser)
        if (len(positionData) < 1): return

        points = []
        for row in positionData:
            points.append([row['Longitude'], row['Latitude']])
        
        kmc = KMeansClusteringManager(self.kmcGroupCount, points)
        kmcClusters = kmc.Fit()

        for id, data in kmcClusters.items():
            self.exportPreview.insert(tk.END, f"Cluster ID: {id}\n")
            for p in data["points"]:
                address = self.databaseManager.GetAddressFromPoint((p[0]), (p[1]))
                self.exportPreview.insert(tk.END, f"-    {address}\n")
            self.exportPreview.insert(tk.END, "\n")

    def Export(self):
        text = self.exportPreview.get("1.0", "end-1c")
        #Convert to PDF here!
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.multi_cell(w = 0, h = 6, txt = text, border = 0, align = 'L')
        filepath = filedialog.asksaveasfilename(defaultextension = ".pdf")
        pdf.output(filepath, 'F')

    def PageTypeSelected(self, event):
        pageType = self.pageTypeCombobox.get()

        self.ClearFrame(self.scrollableFrame)

        if (pageType == self.pageOptions[0]): #Listings Page
            self.databaseManager.currentPageTable = self.databaseManager.listingsTableName

            #Re-enable favorite button
            self.generateListingsButton.config(state = tk.NORMAL)
            self.cityTextBox.config(state = tk.NORMAL)
            self.countryTextBox.config(state = tk.NORMAL)
            #---

            #Populate Page
            self.listingsData = self.databaseManager.GetHomeListingData()
            self.SetupComboboxPages()
        elif (pageType == self.pageOptions[1]): #Favorites Page
            self.databaseManager.currentPageTable = self.databaseManager.favoritesTableName

            #Disable widgets relating to favorites
            self.generateListingsButton.config(state = tk.DISABLED)
            self.cityTextBox.config(state = tk.DISABLED)
            self.countryTextBox.config(state = tk.DISABLED)
            #---

            #Populate Page
            self.listingsData = self.databaseManager.GetFavorites(self.currentUser)
            self.SetupComboboxPages()

    def FlagSelected(self, event):
        pass

    def UserSelected(self, event):
        self.currentUser = self.userCombobox.get()

    def AddUser(self):
        userName = self.userEntryBox.get()
        if (self.databaseManager.AddToUserTable(userName)):
            self.userValues.append(userName)
            self.userCombobox.configure(values = self.userValues)

    def RemoveUser(self):
        pass

    def SetupDefaultUser(self):
        if (self.databaseManager.GetUserID('default') == None):
            self.userCombobox.set('default')
            self.currentUser = self.userCombobox.get()

            self.userEntryBox.insert(0, 'default')
            self.AddUser()
            self.userEntryBox.delete(0, tk.END)
        else:
            self.userCombobox.set('default')
            self.currentUser = self.userCombobox.get()

    def ComboboxSelected(self, event):
        if (self.listingsData == None): return

        currentPage = int(self.combobox.get()) * self.pageSize
        self.ClearFrame(self.scrollableFrame)

        for count, row in enumerate(self.listingsData):
            if (count < currentPage): continue
            if (count >= currentPage + self.pageSize): break

            _bathrooms = row['Bathrooms']
            _bedrooms = row['Bedrooms']
            _size = row['Size']
            _houseCategory = row['House Category']
            _price = row['Price']
            _streetName = row['street name']
            _city = row['city']
            _state = row['state']
            _latitude = row['Latitude']
            _longitude = row['Longitude']

            listingInfoText = (
                f"---{count}---\n"
                f"Bathrooms: {_bathrooms}\n"
                f"Bedrooms: {_bedrooms}\n"
                f"Size: {_size}\n"
                f"House Category: {_houseCategory}\n"
                f"Price: ${_price}\n"
                f"Street: {_streetName}\n"
                f"City: {_city}\n"
                f"State: {_state}"
            )

            listingContainer = tk.Frame(self.scrollableFrame, bg = self.bgColor)
            listingContainer.grid_columnconfigure(0, weight = 1)
            listingContainer.grid_columnconfigure(1, weight = 0)
            listingContainer.grid_rowconfigure(0, weight=1)

            listingLabel = tk.Label(listingContainer, text = listingInfoText,
                                    bg = self.bgColor, fg = self.textColor, 
                                    font = self.textFont, wraplength = 320, justify = "left", anchor = "w")
            
            listingOptionsContainer = tk.Frame(listingContainer, bg = self.panelColor)
            listingOptionsContainer.grid(row = 0, column = 1, sticky = "nsew", padx = 5, pady = 5)

            #Setup Widgets for Adding Favorites
            if (self.databaseManager.currentPageTable == self.databaseManager.listingsTableName):
                favoriteButton = tk.Button(listingOptionsContainer, text = "+ Favorite", 
                                        bg = self.highlightColor, fg = self.textColor, font = self.smallButtonFont)
                favoriteButton.config(command = lambda r = row, b = favoriteButton: self.AddToFavorites(r, b))

                if (self.databaseManager.IsFavorited(row['ID'], self.currentUser)):
                    favoriteButton.config(state = tk.DISABLED, bg = self.bgColor)

                favoriteButton.pack(padx = 5, pady = 5)
            #---

            flagOptions = ['Love', 'Like', 'Pass']
            flagCombobox = ttk.Combobox(listingOptionsContainer, values = flagOptions)
            flagCombobox.bind("<<ComboboxSelected>>", self.FlagSelected)
            flagCombobox.pack(padx = 5, pady = 5)

            listingLabel.grid(row = 0, column = 0, sticky="w")
            listingContainer.pack(fill = "x", padx = 5, pady = 5)

    def AddToFavorites(self, listing, button):
        button.config(state = tk.DISABLED, bg = self.bgColor)
        self.databaseManager.AddToFavoritesTable(listing['ID'], self.currentUser)

    def UpdateComboBoxOptions(self):
        pageOptions = []
        for pageNum in range(self.pageCount):
            pageOptions.append(str(pageNum))
        self.combobox['values'] = pageOptions
        self.combobox.set("0")

    def SetupComboboxPages(self):
        if (self.listingsData == None): return

        self.lastPageCount = len(self.listingsData) % self.pageSize
        self.pageCount = math.floor(len(self.listingsData) / self.pageSize)
        if (self.lastPageCount > 0): self.pageCount += 1

        self.UpdateComboBoxOptions()
        self.ComboboxSelected(None)

    def GenerateListings(self):
        cityInput = self.cityTextBox.get()
        countryInput = self.countryTextBox.get()

        #ISSUE: These need to be in a try catch statement for saftey
        self.databaseManager.PullHomeListingData(cityInput, countryInput)
        self.listingsData = self.databaseManager.GetHomeListingData()

        self.SetupComboboxPages()
        #---

    def SortBy(self, sortType): #ISSUE: Favorites are sorted by the listings table, and not by the favorites!
        self.listingsData = self.databaseManager.ExecuteScript(self.databaseManager.sortQueryDict[sortType])
        self.SetupComboboxPages()
