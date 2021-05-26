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
		print("Kun Reading : ")
		for x in val2 :
			print("\t"+x.string)
	def getInfoOnReading(self , html) :
		val = str(bs4.BeautifulSoup(html , features="html.parser" ).find("div" , {"class" : "on readings"}))
		val2 = bs4.BeautifulSoup(val , features="html.parser").findAll("a")
		print("On Reading : ")
		for x in val2 :
			print("\t"+x.string)
	def getInfoMeaning(self , html) :
		val = str(bs4.BeautifulSoup(html , features="html.parser" ).find("div" , {"class" : "meanings english sense"}))
		val2 = bs4.BeautifulSoup(val , features="html.parser").findAll("span")
		print("English Meanings : ")
		for x in val2 :
			print("\t"+x.string)

chercher = "当"
src = Chercher(chercher)