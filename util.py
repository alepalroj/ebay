#!/usr/bin/python

import xml.etree.ElementTree as ET
import re
from entitys import Category
import sys
import ConfigParser
import os

class Utils:
	def __init__(self, xmlString):
		if xmlString == '':
			pass
		else:
			self.xmlString = xmlString
	
	def getStringXml(self):
		self.xmlString = re.sub('\\sxmlns="[^"]+"', '', self.xmlString, count=1)
		return ET.fromstring(self.xmlString)
	
	def getCategoryList(self, root, parent):
		categories =[]
		categoryList = []
		for category in root.findall('./CategoryArray/Category'):
			bestOfferEnabled = category.find('BestOfferEnabled')
			categoryID = category.find('CategoryID')
			categoryParentID = category.find('CategoryParentID')
			categoryLevel = category.find('CategoryLevel')
			categoryName = category.find('CategoryName')
			
			if categoryID is not None:
				categoryID = category.find('CategoryID').text
			else:
				categoryID = None
				
			if bestOfferEnabled is not None:
				bestOfferEnabled = category.find('BestOfferEnabled').text
				bestOfferEnabled = bestOfferEnabled.lower()
				if 'true' == bestOfferEnabled:
					bestOfferEnabled = 1
				else:
					bestOfferEnabled = 0
			
			if categoryParentID is not None:
				categoryParentID = category.find('CategoryParentID').text
			else:
				categoryParentID = None
			
			if categoryID is not None and categoryParentID is not None:
				if categoryID == categoryParentID:
					categoryParentID = None
					
			if categoryLevel is not None:
				categoryLevel = category.find('CategoryLevel').text
			else:
				categoryLevel = None
				
			if categoryName is not None:
				categoryName = category.find('CategoryName').text
			else:
				categoryName = None
				
			if categoryID is not None:
				item = Category(categoryID, categoryLevel, categoryParentID, categoryName, bestOfferEnabled)
				categoryList.append(item)
		return categoryList

		
	def listToInsert(self, inn):
		output = []
		for item in inn:
			try:
				output.append((item.categoryID, item.categoryLevel, item.categoryParentID, item.categoryName, item.bestOfferEnabled))
			except:
				pass				
		return output
		
		
	def uniqe(self, inputs):
		output = []
		for item in inputs:
			if item not in output:
				output.append(item)
		return output

	def _setRoot(self, root):
		return '_'+ str(abs(hash(str(root)))) + ' = insFld(foldersTree, gFld("'+str(root)+'", "javascript:undefined"))'
		
	def _setChild(self, root, child):
		return '_'+ str(abs(hash(str(child)))) + ' = insFld(_'+str(root)+', gFld("'+str(child)+'", "javascript:undefined"))'
		
		
	def setHtml(self, categoryID, categoryList):
		jsfile = ''		
		jsfile += "USETEXTLINKS = 1\n"
		jsfile += "STARTALLOPEN = 0\n"
		jsfile += "USEFRAMES = 0\n"
		jsfile += "USEICONS = 0\n"
		jsfile += "WRAPTEXT = 1\n"
		jsfile += "PRESERVESTATE = 1\n"
		jsfile += "\n"	
		jsfile += 'foldersTree = gFld("<b>Ebay</b>","'+ categoryID +'.html")'
		jsfile += "\n"
		jsfile += 'foldersTree.treeID = "Ebay"'
		jsfile += "\n"
		nodes = {}
		values = []		
		for line in categoryList:
			for i in range(5):
				if line[i] is not None:
					if not str(line[i]) in nodes:
						if i == 0:
							data = self._setRoot(str(line[i]))
							nodes['_'+str(abs(hash(line[i])))] = data
							values.append('_'+str(abs(hash(line[i]))))
						else:
							if nodes['_'+str(abs(hash(str(line[i-1]))))] <> None:
								data = self._setChild(str(abs(hash(line[i-1]))),str(line[i]))
								nodes['_'+str(abs(hash(line[i])))] = data
								values.append('_'+str(abs(hash(line[i]))))
		for item in self.uniqe(values):
			jsfile += nodes[item] + "\n"
		self.writeJs(categoryID, jsfile)
		content = self.readHTML(categoryID)
		content = content.replace("{{categoryID}}", categoryID)
		self.writeHTML(categoryID, content)
		
	def writeJs(self, categoryID, data):
		try:
			jsfile = open(categoryID+'.js', "w")
			jsfile.write(data)
			jsfile.close()
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror)
		except:
			print "Unexpected error:", sys.exc_info()[0]


	def readHTML(self, categoryID):
		config = ConfigParser.RawConfigParser()
		config.read('config.ini')
		_dir = os.path.dirname(__file__)
		template = config.get('template', 'folder')
		try:
			htmlfile = open(''+_dir+''+template, "r")
			content = htmlfile.read()
			htmlfile.close()
			return content
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror)
		except:
			print "Unexpected error:", sys.exc_info()[0]
			
	def writeHTML(self, categoryID, data):
		try:
			html = open(categoryID+'.html', "w")
			html.write(data)
			html.close()
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror)
		except:
			print "Unexpected error:", sys.exc_info()[0]
