from PyQt5 import QtCore , QtGui , QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import win32clipboard	
from pynput import keyboard
import time
from urllib.request import urlopen
from urllib.parse import quote
import webbrowser	
import re
import bs4


class Chercher() :
	def __init__(self , chercher) :
		website = urlopen(u"https://jisho.org/search/"+quote(chercher))
		html = str(website.read().decode("utf-8") )
		self.getInfoKunReading(html)
		self.getInfoOnReading(html)
		self.getInfoMeaning(html)	
	def getInfoKunReading(self , html) :
		val = str(bs4.BeautifulSoup(html , features="html.parser" ).find("div" , {"class" : "kun readings"}))
		val2 = bs4.BeautifulSoup(val , features="html.parser").findAll("a")
		self.FullInfo = "Kun Reading : "
		for x in val2 :
			self.FullInfo += " " + x.string
	def getInfoOnReading(self , html) :
		val = str(bs4.BeautifulSoup(html , features="html.parser" ).find("div" , {"class" : "on readings"}))
		val2 = bs4.BeautifulSoup(val , features="html.parser").findAll("a")
		self.FullInfo += "\nOn Reading : "
		for x in val2 :
			self.FullInfo += " " +x.string
	def getInfoMeaning(self , html) :
		val = str(bs4.BeautifulSoup(html , features="html.parser" ).find("div" , {"class" : "meanings english sense"}))
		val2 = bs4.BeautifulSoup(val , features="html.parser").findAll("span")
		self.FullInfo += "\nEnglish Meanings : "
		for x in val2 :
			self.FullInfo += " " + x.string 

	def returnInfo(self) :
		return self.FullInfo
		


class Fenetre(QtWidgets.QMainWindow ) :

	def __init__(self , app ) :
		super(Fenetre , self).__init__()

		#Taille de l'ecran :

		
		self.setWindowTitle("Kanjislator")
		self.setStyleSheet("background-color:#012;border-top:10px solid #128BBC;")

		flag = QtCore.Qt.WindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
		self.setWindowFlags(flag)	
		#self.setAttribute(Qt.WA_NoSystemBackground , True)
		#self.setAttribute(Qt.WA_TranslucentBackground , True)
		
		self.widget = QWidget();

		self.KanjiBox = QPushButton("XL", self)
		self.KanjiBox.setFixedSize(120,120)
		self.Details = QLabel("Le Lorem Ipsum est simplement du faux texte employé dans la composition et la mise en page avant impression. Le Lorem Ipsum est le faux texte standard de l'imprimerie depuis les années 1500, quand un imprimeur anonyme assembla ensemble des morceaux de texte pour réaliser un livre spécimen de polices de texte. Il n'a pas fait que survivre cinq siècles, mais s'" , self)
		self.Details.setFixedSize(150,120)
		self.Details.setWordWrap(True)
			
		
		self.KanjiBox.setStyleSheet("width:75px;height:125px;background-color:#FFFFFF;color: #035373;border:none;font-size:8:0px;");
		self.Details.setStyleSheet("color: white;font-size:13px;border:none;");
		

		self.vbox = QHBoxLayout()
		self.vbox.addWidget(self.KanjiBox)
		self.vbox.addWidget(self.Details)
		
		self.widget = QWidget()
		self.widget.setLayout(self.vbox)

		self.threadclass = ThreadClass()
		self.threadclass.start()
		self.threadclass.addPost.connect(self.changeText)

		self.setCentralWidget(self.widget)
		self.makeSize(app)
		self.oldPos = self.pos()
		self.show()
	

	def makeSize(self , app ):
		screen = app.primaryScreen()
		rect = screen.availableGeometry()
		self.setGeometry(0 , (rect.height()/2)-90 , 300 , 180)
	def changeText(self , data , data2) :
		self.KanjiBox.setText(data)
		self.Details.setText(data2)
	def mousePressEvent(self, event):
         self.oldPos = event.globalPos()
	def mouseMoveEvent(self, event):
		delta = QPoint(event.globalPos() - self.oldPos)
		self.move(self.x() + delta.x() , self.y() + delta.y())
		self.oldPos = event.globalPos()
       	

		
	

class ThreadClass(QtCore.QThread):
	addPost = pyqtSignal(str , str)
	def  __init__(self , parent = None) :
		super(ThreadClass , self).__init__()
	def run (self):
		while True :
			self.checkShortCut()

	def checkShortCut(self):
		COMBINATION = [{keyboard.Key.shift , keyboard.KeyCode(char='m')} , {keyboard.Key.shift , keyboard.KeyCode(char='M')}]
		current = set()
		

		def execute():
			win32clipboard.OpenClipboard()
			data = win32clipboard.GetClipboardData()
			win32clipboard.CloseClipboard()
			cher = Chercher(data)
			InfoText = str(cher.returnInfo())
			self.addPost.emit(data , InfoText)
			print(data , InfoText)
			
			
		def on_press(key) :
			if any([key in COMBO for COMBO in COMBINATION]): 
				current.add(key)
				if any(all(k in current for k in COMBO) for COMBO in COMBINATION):
					execute()
		def on_release(key) : 
			if any([key in COMBO for COMBO in COMBINATION]): 
				current.remove(key)
		def changeText(obj) :
			print(data)
			obj.Text.setText(data)
			QCoreApplication.processEvents()

		with keyboard.Listener(on_press=on_press , on_release=on_release) as listener : 
			listener.join()
	



app = QtWidgets.QApplication(sys.argv)
GUI = Fenetre(app )
sys.exit(app.exec_())


