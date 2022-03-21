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
from PyQt5 import QtGui 
from PyQt5.QtCore import * 

style_file = open('webeye_formatting.css', 'r')

# Set Up Application and Enable Styling 
app = QApplication(sys.argv)
app.setStyleSheet(style_file.read())
app.setStyle('Fusion')

# Main

class App():

	# Initalization
	def __init__(self):
		# Application Init
		self.app = QApplication(sys.argv)
		self.app.setStyleSheet(style_file.read())
		self.app.setStyle('Fusion')

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
		self.textOut.setFont(QFont("Consolas"))

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
		self.tree = QTreeWidget()
		self.tree.setObjectName("Tag hierarchy")
		self.treeRoot = QTreeWidgetItem(["<html>"])
		self.tree.addTopLevelItem(self.treeRoot)
		self.tree.itemSelectionChanged.connect(self.treeSelection)
		self.tagReturn()

		# Next / Prev Sibling
		self.scrapeLabel2 = QLabel("Navigate Tag Siblings")
		self.scrapeLabel2.setAlignment(Qt.AlignCenter)
		self.nextSib = QPushButton("Next")
		self.prevSib = QPushButton("Prev")

		# Button List
		self.buttonList = [self.scrapeButton, self.fetchButton, self.nextSib, self.prevSib]

		# Layout
		self.layout = QGridLayout()
		
		# Row 0 
		self.layout.addWidget(self.urlBox, 0, 0, 1, 3)
		self.layout.addWidget(self.scrapeButton, 0, 3)
		self.layout.addWidget(self.fetchButton, 0, 4)
		self.layout.addWidget(self.tree, 0, 5, 5, 3)

		# Row 1
		self.layout.addWidget(self.scrapeLabel2, 1, 0, 1, 2)

		# Row 2
		self.layout.addWidget(self.prevSib, 2, 0)
		self.layout.addWidget(self.nextSib, 2, 1)

		# Row 3
		self.layout.addWidget(self.textScrollArea, 3, 0, 1, 5)

		# Row 4
		self.layout.addWidget(self.progressBar, 4, 0, 1, 5)

		# Wrap up window and apply layout
		self.window.setLayout(self.layout)
		self.closeSplashScreen(self.splash)
		self.window.show()
		self.isScraping = False;

		# EXECUTE
		self.exe()

	# Check robots.txt
	def fetchSiteInfo(self):
		global scrapeDelay
		global tagList 
		tagList = [0]
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
		if (self.isScraping == True):
			return
		self.isScraping = True
		self.scrapeButton.setEnabled(False)
		self.fresh()

		# URL Box Handling
		self.progressBar.setValue(0)
		self.target = self.urlBox.text()
		self.baseTarget = self.target.split('/')[0]
		self.progressBar.setValue(25)
		# If Rules hve been checled for this particular site
		if (self.baseTarget in clearToGo):
			# Retreive Site
			self.httpStr = "http://"
			self.html = requests.get(self.httpStr + self.target).text
			self.soup = BeautifulSoup(self.html, "html.parser")
			self.progressBar.setValue(50)
			
			# Tag Handling
			self.tag = self.treeSelection()
			if self.tag != 000:
				self.progressBar.setValue(75)
				self.scraping = False
				self.scrapeButton.setEnabled(True)
				self.progressBar.setValue(100)
				return self.textOut.setText("Please select a tag")

			self.tag = self.tag.replace("<", "")
			self.tag = self.tag.replace(">", "")
			self.progressBar.setValue(75)

			# Scraping and Returing
			try:
				self.returned = self.soup.find(self.tag)
				self.returned = self.returned.text.replace("; ", ";\n")
				self.textOut.setText(self.returned)
				self.progressBar.setValue(100)
			except:
				self.textOut.setText("No results for this tag at " + self.urlBox.text())
				self.progressBar.setValue(0)
			try:
				# Scraping Halting Request
				self.isScraping = False;
				self.coolDown(scrapeDelay)
			except:
				self.scrapeButton.setEnabled(True)
		else:
			self.textOut.setText("Please check scraping rules for this site before scraping")
			self.progressBar.setValue(0)

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
		self.app.processEvents()

	# Find Current Selection (StackOverflow)
	def treeSelection(self):
		getSelected = self.tree.selectedItems()
		if getSelected:
			baseNode = getSelected[0]
			getChildNode = baseNode.text(0)
			print(getChildNode)
			return str(getChildNode)

	# Disable Buttons and Delay
	def coolDown(self, tictoc):
		for button in self.buttonList:
			button.setEnabled(False)
		self.fresh()
		print(tictoc)
		self.fresh()
		try:
			time.sleep(int(tictoc))
		except:
			pass
		for button in self.buttonList:
			button.setEnabled(True)
		self.fresh()
		self.isScraping = False

	# Add full list of HTML tags to 
	def tagReturn(self):
		self.return_ = requests.get("https://www.w3schools.com/tags").text
		self.soop = BeautifulSoup(self.return_, "html.parser")
		self.tagLs = self.soop.find_all(class_="w3-table-all notranslate")
		print()
		for ls in self.tagLs:
			print("<"+self.findSubset(str(ls), "&lt;", "&gt;"))

	# Find Between 2 chars (StackOverflow)
	def findSubset(self, s, first, last):
		try:
			start = s.index(first) + len(first)
			end = s.index(last, start)
			return s[start:end]
		except ValueError:
			return "hm"

	# Exit()
	def exe(self):
		sys.exit(app.exec_())

if __name__ == "__main__":
	ex = App()

# Comment that does nothing