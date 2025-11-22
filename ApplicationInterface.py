import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter import font
from tkinter import ttk

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


        self.bgColor      = "#3D3D3D"
        self.panelColor   = "#666666"
        self.elementColor = "#898989"
        self.textColor    = "#E0E0E0"
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
        
        #Scrollable Frame
        self.scrollableFrame = tk.Frame(self.listingsCanvas, bg = self.elementColor)
        self.listingsCanvas.create_window((0, 0), window = self.scrollableFrame, anchor= "nw")

        self.listingsCanvas.configure(yscrollcommand = self.listingsScrollBar.set)
        self.scrollableFrame.bind( #This will update the scrolling region size when frame gets updated
        "<Configure>",
            lambda e: self.listingsCanvas.configure(
                scrollregion = self.listingsCanvas.bbox("all")
            )
        )
        
        self.homeListingsTitleLabel.pack()

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
        self.organizationOptionsTitleLabel.pack()

    def AddExportPreviewText(self, text): #Enables and re-enables text-scrollable widget to not allow user input.
        self.exportPreview.delete("1.0", tk.END) #Erases all text content from starting index to end.
        self.exportPreview.config(state = "normal")
        self.exportPreview.insert(tk.END, text)
        self.exportPreview.config(state = "disabled")

    def ClearFrame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def GenerateListings(self):
        cityInput = self.cityTextBox.get()
        countryInput = self.countryTextBox.get()

        #ISSUE: These need to be in try catch statements for saftey
        self.databaseManager.PullHomeListingData(cityInput, countryInput)
        listingsData = self.databaseManager.GetHomeListingData()
        #---
        
        self.ClearFrame(self.scrollableFrame)
        for row in listingsData:
            _bathrooms = row[1]
            _bedrooms = row[2]
            _size = row[3]
            _houseCategory = row[4]
            _price = row[5]
            _streetName = row[6]
            _city = row[7]
            _state = row[8]
            _latitude = row[9]
            longitude = row[10]

            listingInfo = (
                f"Bathrooms: {_bathrooms}\n"
                f"Bedrooms: {_bedrooms}\n"
                f"Size: {_size}\n"
                f"House Category: {_houseCategory}\n"
                f"Price: {_price}\n"
                f"Street: {_streetName}\n"
                f"City: {_city}\n"
                f"State: {_state}"
            )

            listingContainer = tk.Frame(self.scrollableFrame, bg = self.panelColor, padx = 10, pady = 10)
            listingLabel = tk.Label(listingContainer, text = listingInfo,
                                    bg = self.bgColor, fg = self.textColor, font = self.textFont, padx = 5, pady = 5)
            
            listingContainer.pack(fill = "x")
            listingLabel.pack()

