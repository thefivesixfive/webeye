# webeye Web Scraping Program Alpha
# Developer Caleb North
#                  
                                
# Important variables
global URL_NET_TEST
global clearToGo
global app

URL_NET_TEST = "https://www.google.com"
clearToGo = []
                                                                      
# Importing Modules and Important Files
from PyQt5 import *
from bs4 import *
import time
import sys
import requests

# Import Sub Libs
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import * 

# Main
class App():

	# Initalization
	def __init__(self):
		# Application Init
		global app
		app = QApplication(sys.argv)
		app.setStyle("Fusion")
		
		# Splash
		self.openSplashScreen()
		self.netCheck(self.splash)

		# Window
		self.window = QWidget()
		self.window.setWindowIcon(QtGui.QIcon("webeye_icon.png"))
		self.window.setWindowTitle("webeye")
		self.window.setGeometry(50, 50, 800, 700)

		# Loading Bar
		self.progressBar = QProgressBar()

		# URL Box
		self.urlBox = QLineEdit()
		self.urlBox.setText("twitter.com")

		# Label
		self.textOut = QLabel("Please F\u0332etch Information (rules) before scraping this site")
		self.textOut.setWordWrap(False)
		self.textOut.setAlignment(Qt.AlignLeft)
		self.textOut.setFont(QFont("Consolas", 10))

		# Scroll Area
		self.textScrollArea = QScrollArea()
		self.textScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.textScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.textScrollArea.setWidgetResizable(True)
		self.textScrollArea.setWidget(self.textOut)
	
		# Check Scraping Rules Button
		self.fetchButton = QPushButton(" F\u0332etch Information ")
		self.fetchButton.setShortcut("Ctrl+F")
		self.fetchButton.clicked.connect(self.fetchSiteInfo)

		# Scrape
		self.scrapeButton = QPushButton(" S\u0332crape ")
		self.scrapeButton.clicked.connect(self.scrape)
		self.scrapeButton.setShortcut("Ctrl+S")
		self.scrapeButton.setEnabled(False)

		# Tag Hierarchy
		self.tree = QTreeWidget(self.window)
		self.tree.setHeaderLabel(" Tag Hierarchy")
		self.tree.itemSelectionChanged.connect(self.treeSelection)

		# Next / Prev Label
		self.navLabel = QLabel("Navigate Results")
		self.navLabel.setAlignment(Qt.AlignCenter)
		self.navLabel.setFont(QFont("Consolas", 10))

		# Next / Prev Buttons
		self.nextRes = QPushButton("N\u0332ext")
		self.prevRes = QPushButton("P\u0332rev")
		self.nextRes.clicked.connect(self.next)
		self.prevRes.clicked.connect(self.prev)
		self.nextRes.setShortcut("Ctrl+N")
		self.prevRes.setShortcut("Ctrl+P")
		self.nextRes.setEnabled(False)
		self.prevRes.setEnabled(False)

		# Button List
		self.generalButtons = [self.scrapeButton, self.fetchButton]
		self.navButtons = [self.nextRes, self.prevRes]
		'''for btn in self.generalButtons:
			btn.setFlat(True)
'''
		# Layout
		self.layout = QGridLayout()
		
		# Row 0 
		self.layout.addWidget(self.urlBox, 0, 0, 1, 2)
		self.layout.addWidget(self.scrapeButton, 0, 2)
		self.layout.addWidget(self.fetchButton, 0, 3)
		self.layout.addWidget(self.tree, 0, 4, 4, 2)

		# Row 1
		self.layout.addWidget(self.navLabel, 1, 0, 1, 4)

		# Row 2
		self.layout.addWidget(self.prevRes, 2, 0, 1, 2)
		self.layout.addWidget(self.nextRes, 2, 2, 1, 2)

		# Row 3
		self.layout.addWidget(self.textScrollArea, 3, 0, 1, 4)

		# Row 4
		self.layout.addWidget(self.progressBar, 4, 0, 1, 6)

		# Wrap up window and apply layout
		self.window.setLayout(self.layout)
		self.closeSplashScreen(self.splash)
		self.window.show()
		self.isScraping = False;

		# EXECUTE
		self.exe()

	# Check robots.txt
	def fetchSiteInfo(self):
		self.currentSelection = 0
		# Important Vars
		global scrapeDelay
		global tagList 
		self.currentSelection = 0
		self.tagList = [0]
		self.returnedLs = []

		# Retreive Information from canicrawl.com
		self.progressBar.setValue(0)
		self.re = requests.get("https://canicrawl.com/" + self.urlBox.text().replace(" ", ""))
		self.soup = BeautifulSoup(self.re.text, "html.parser")
		self.progressBar.setValue(33)

		# Determine if a good site :D
		if not ("responded with HTTP status code 200" in str(self.re.text)):
			# If not a good site
			self.progressBar.setValue(66)
			self.textOut.setText("Whoops!  Webeye couldn't find any rules about scraping at \n\"" + self.urlBox.text() + "\" \nPlease be careful while scraping in \"unknown\" scraping territory.")
			self.progressBar.setValue(0)
		else:

			# If a good site
			self.progressBar.setValue(66)
			self.robotReturn = self.soup.find(id="rawView").text

			# Insert \n's
			self.ls = ["Disallow", "Allow", "\n#", "\nUser-Agent", "\nUser-agent", "http", "Crawl", "crawl"]
			for string in self.ls:
				self.robotReturn = self.robotReturn.replace(string.replace("\n", ""), \
															"\n" + string)
			# Set the scraping delay
			scrapeDelay = self.robotReturn[self.robotReturn.find("Crawl-delay") + 13]
			if str(type(scrapeDelay)) != '<class "int">':
				scrapeDelay = self.robotReturn[self.robotReturn.find("Crawl-delay") + 12]
				if str(type(scrapeDelay)) != '<class "int">':
					scrapeDelay = 1
			
			# Continue If a good site
			self.textOut.setText(self.robotReturn)

			self.fresh()
		
		# Retreive Site
		try:
			self.httpStr = "http://"
			self.html = requests.get(self.httpStr + self.urlBox.text().split('/')[0]).text
		except:
			self.progressBar.setValue(0)
			self.textOut.setText("Something went wrong, did you forget to enter a website address? \n Please start after the \'https://\'")
			return

		self.soup = BeautifulSoup(self.html, "html.parser")
		self.tagReturn(self.soup)
		
		# Finalizing
		clearToGo.append(self.urlBox.text().split("/")[0])
		self.progressBar.setValue(100)
		self.isScraping = False
		self.scrapeButton.setEnabled(True)
		self.fresh()

	# Splashscreen
	def openSplashScreen(self):
		# Setup Splash Screen
		self.splash_pix = QPixmap('webeye_logo.png')
		self.splash = QSplashScreen(self.splash_pix, Qt.WindowStaysOnTopHint)
		self.splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
		self.splash.setMask(self.splash_pix.mask())
		self.splash.show()
		self.fresh()

	# Scraping My Way Through Town
	def scrape(self):
		global currentSelection
		global returnLs
		# Determine if Already Scraping or Not
		if (self.isScraping == True):
			return
		self.isScraping = True
		self.scrapeButton.setEnabled(False)

		# URL Box Handling
		self.progressBar.setValue(0)
		self.target = self.urlBox.text()
		self.baseTarget = self.target.split('/')[0]
		self.progressBar.setValue(25)

		# Retreive Site
		try:
			self.httpStr = "http://"
			self.html = requests.get(self.httpStr + self.target).text
		except:
			self.progressBar.setValue(0)
			self.textOut.setText("Something went wrong, did you forget to enter a website address? \nPlease start after the \'https://\'")
			return

		self.soup = BeautifulSoup(self.html, "html.parser")
		self.tagReturn(self.soup)
		self.fresh()

		# If Rules hve been checled for this particular site
		if (self.baseTarget in clearToGo):
						
			# Tag Handling
			self.tag = self.treeSelection()
			self.tag = str(self.tag).replace("<", "")
			self.tag = str(self.tag).replace(">", "")
			self.progressBar.setValue(75)

			# Refresh Tree
			self.tree.clear()
			self.tagReturn(self.soup)

			# Scraping and Returing
			try:
				self.returnLs = self.soup.select(self.tag)
				self.textOut.setText(str(self.returnLs[self.currentSelection]) \
									.replace("; ", ";\n"))
				self.navLabel.setText(f"Navigate Results ({self.currentSelection + 1} / {len(self.returnLs)})")
				self.progressBar.setValue(100)
			except:
				self.textOut.setText("No results for this tag at " + self.urlBox.text() + ". \nMaybe you didn't select one?")
				self.navLabel.setText(f"Navigate Results ( N / A )")
				self.progressBar.setValue(0)
			try:
				# Scraping Halting Request
				self.isScraping = False;
				self.coolDown(scrapeDelay, len(self.returnLs))
			except:
				self.scrapeButton.setEnabled(True)
				self.nextRes.setEnabled(True)
				self.prevRes.setEnabled(True)
		else:
			self.textOut.setText("Please check scraping rules for this site before scraping")
			self.progressBar.setValue(0)

	# Previous Sibling Retreive
	def prev(self):
		self.tag = self.treeSelection()
		self.tag = str(self.tag).replace("<", "")
		self.tag = str(self.tag).replace(">", "")

		self.currentSelection -= 1;
		if self.currentSelection < 0:
			self.currentSelection = len(self.returnLs) - 1
		
		self.textOut.setText(str(self.returnLs[self.currentSelection]) \
									.replace("; ", ";\n"))
		self.navLabel.setText(f"Navigate Results ({self.currentSelection + 1} / {len(self.returnLs)})")

	# Next Sibling Retreive 
	def next(self):
		self.tag = self.treeSelection()
		self.tag = str(self.tag).replace("<", "")
		self.tag = str(self.tag).replace(">", "")

		self.currentSelection += 1;
		if self.currentSelection > len(self.returnLs) - 1:
			self.currentSelection = 0;
		
		self.textOut.setText(str(self.returnLs[self.currentSelection]) \
									.replace("; ", ";\n"))
		self.navLabel.setText(f"Navigate Results ({self.currentSelection + 1} / {len(self.returnLs)})")

	def closeSplashScreen(self, splash):
		splash.hide()

	# Check Internet Connection 
	def netCheck(self, widget):
		try:
			if str(requests.get(URL_NET_TEST)) == '<Response [200]>':
				return True
		except:
			self.connectionFailure(widget)
			return False

	# Deathscreen
	def connectionFailure(self, widget):
		QMessageBox.warning(widget, 'Fatal Error', "No internet connection", QMessageBox.Close)
		sys.exit()

	# Refresh Shortcut
	def fresh(self):
		app.processEvents()

	# Find Current Selection (StackOverflow)
	def treeSelection(self):
		getSelected = self.tree.selectedItems()
		if getSelected:
			baseNode = getSelected[0]
			getChildNode = baseNode.text(0)
			return str(getChildNode)

	# Disable Buttons and Delay
	def coolDown(self, tictoc, length):
		# Enable / Disable Buttons
		for button in self.generalButtons + self.navButtons:
			button.setEnabled(False)
		self.fresh()
		try:
			time.sleep(int(tictoc))
		except:
			pass
		for button in self.generalButtons:
			button.setEnabled(True)
		if length > 1:
			for button in self.navButtons:
				button.setEnabled()

		# Finish
		self.fresh()
		self.isScraping = False

	# Add full list of HTML tags to 
	def tagReturn(self, scroop):
		# Get Information from www.w3schools.com
		self.return_ = requests.get("https://www.w3schools.com/tags").text
		self.soop = BeautifulSoup(self.return_, "html.parser")
		self.tagLs = self.soop.find_all("a", href=True) #Backup? class_="w3-table-all notranslate"
		
		# Begin Tag Retrival and Sorting
		self.reTags = []
		for tag in self.tagLs:
			if "tag" in tag["href"]:
				self.reTags.append(self.findSubset(str(tag), "&lt;", "&gt;"))
		while "" in self.reTags:
			self.reTags.remove("")

		self.reTags = sorted(self.reTags)
		self.newReTags = []

		# Determine Available Tags
		self.y = []
		self.n = []
		for tag in self.reTags:
			if not scroop.find_all(tag) == []:
				self.y.append(tag)
			else:
				self.n.append(tag)

		# Remove Doubles (StackOverFlow)
		self.yes = []
		self.no = []
		
		for item in self.y:
			if item not in self.yes:
				self.yes.append(item)

		for item in self.n:
			if item not in self.no:
				self.no.append(item)

		# Have available tags and unavailable tag individually sorted alphabetically
		self.yes = sorted(self.yes)
		self.no = sorted(self.no)

		# Now Add Tags to Tree

		for tag in self.yes:
			self.item = QTreeWidgetItem(self.tree)
			self.item.setText(0, "<" + tag + ">")
			self.itemFont = QFont("Consolas", 10, QFont.Bold)
			self.itemFont.setItalic(True)
			self.item.setFont(0, self.itemFont)

		for tag in self.no:
			self.item = QTreeWidgetItem(self.tree)
			self.item.setText(0, "<" + tag + ">")
			self.itemFont = QFont("Consolas", 10)
			self.item.setFont(0, self.itemFont)

	# Find Between 2 chars (StackOverflow)
	def findSubset(self, s, first, last):
		try:
			start = s.index(first) + len(first)
			end = s.index(last, start)
			return s[start:end]
		except ValueError:
			return ""

	# Exit()
	def exe(self):
		sys.exit(app.exec_())

if __name__ == "__main__":
	ex = App()

# Comment that does nothing