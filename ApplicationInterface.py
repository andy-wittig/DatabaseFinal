import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter import font
from tkinter import ttk
import math
from KMeansClustering import KMeansClusteringManager

#User-Defined Routines lets one write wrapped-up SQL statements that can be started from application but run inside of Database. 

class UIManager():
    def __init__(self, databaseManager):
        self.applicationName = "Home Buyer Helper"
        self.databaseManager = databaseManager

        self.root = tk.Tk()

        #--- Style Variables ---
        self.defaultSize = [1280, 720]

        self.titleFont = font.Font(family="Helvetica", size=18, weight = "bold")
        self.buttonFont = font.Font(family="Helvetica", size=16)
        self.textFont = font.Font(family="Helvetica", size=12)
        self.pageSize = 50

        self.bgColor      = "#3D3D3D"
        self.panelColor   = "#666666"
        self.elementColor = "#898989"
        self.textColor    = "#E0E0E0"
        #-----------------------

        #--- kmc Variables ----
        self.kmcGroupCount = 1
        self.kmcGroupCountOptions = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        #----------------------

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
        
    def SetupExportWidgets(self):
        self.exportPreview = scrolledtext.ScrolledText(self.exportFrame, bg=self.panelColor,
                                                        state="disabled", wrap = tk.WORD,
                                                        padx = 10, pady = 10)
        #self.exportPreview.vbar.config(troughcolor = self.bgColor, bg = self.elementColor)

        self.exportButton = tk.Button(self.exportFrame, text = "Export", 
                                      bg = self.elementColor, fg = self.textColor, font = self.buttonFont)

        self.exportTitleLabel = tk.Label(self.exportFrame, text="Export Home Listings", 
                                    bg = self.bgColor, fg = self.textColor, font = self.titleFont)

        self.exportTitleLabel.pack()
        self.exportPreview.pack(fill = "both", expand = True)
        self.exportButton.pack(fill = "x")

    def SetupHomeListingsWidgets(self):
        self.homeListingsTitleLabel = tk.Label(self.homeListingsFrame, text="Home Listings",
                                           bg = self.bgColor, fg = self.textColor, font = self.titleFont)
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

        #Combobox
        self.combobox = ttk.Combobox(self.homeListingsFrame, values = [])
        self.combobox.bind("<<ComboboxSelected>>", self.ComboboxSelected)
        
        self.homeListingsTitleLabel.pack()
        self.combobox.pack()

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
        
        #Sort By options
        self.SortPriceHighButton = tk.Button(self.organizationOptionsFrame, text = "Sort by Price: Highest", 
                                      bg = self.elementColor, fg = self.textColor, font = self.buttonFont, command = lambda: self.SortBy("PriceHigh"))
        self.SortPriceLowButton = tk.Button(self.organizationOptionsFrame, text = "Sort by Price: Lowest", 
                                      bg = self.elementColor, fg = self.textColor, font = self.buttonFont, command = lambda: self.SortBy("PriceLow"))
        
        #kmc Grouping
        self.kmcFrame = tk.Frame(self.organizationOptionsFrame)
        self.kmcCombobox = ttk.Combobox(self.kmcFrame, values = self.kmcGroupCountOptions)
        self.kmcCombobox.bind("<<ComboboxSelected>>", self.KMCComboboxSelected)
        self.kmcRunButton = tk.Button(self.kmcFrame, text = "Run kmc Algorithm", 
                                      bg = self.elementColor, fg = self.textColor, font = self.buttonFont, command = lambda: self.RunKMC())

        self.organizationOptionsTitleLabel.pack()
        self.SortPriceHighButton.pack(anchor = tk.CENTER, pady = 5)
        self.SortPriceLowButton.pack(anchor = tk.CENTER, pady = 5)
        self.kmcFrame.pack(anchor = tk.CENTER, pady = 5)
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
        positionData = self.databaseManager.GetHomePositions()
        if (len(positionData) < 1): return

        positions = []
        for row in positionData:
            positions.append([row['Longitude'], row['Latitude']])
        
        kmc = KMeansClusteringManager(self.kmcGroupCount, positions)
        kmcClusters = kmc.Fit()

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

            listingInfo = (
                f"Listing Number {count}\n"
                f"Bathrooms: {_bathrooms}\n"
                f"Bedrooms: {_bedrooms}\n"
                f"Size: {_size}\n"
                f"House Category: {_houseCategory}\n"
                f"Price: {_price}\n"
                f"Street: {_streetName}\n"
                f"City: {_city}\n"
                f"State: {_state}"
            )

            #listingLabelContainer = tk.Frame(self.scrollableFrame, bg = self.bgColor)
            listingLabel = tk.Label(self.scrollableFrame, text = listingInfo,
                                    bg = self.bgColor, fg = self.textColor, 
                                    font = self.textFont, justify = "left", anchor = "w")
            
            #listingLabelContainer.pack(fill = "x", padx = 5, pady = 5)
            listingLabel.pack(fill = "x", padx = 5, pady = 5)

    def UpdateComboBoxOptions(self):
        pageOptions = []
        for pageNum in range(self.pageCount):
            pageOptions.append(str(pageNum))
        self.combobox['values'] = pageOptions
        self.combobox.set("0")

    def SetupComboboxPages(self):
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

    def SortBy(self, sortType):
        self.listingsData = self.databaseManager.ExecuteScript(self.databaseManager.sortQueryDict[sortType])
        self.SetupComboboxPages()
