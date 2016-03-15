#!/usr/bin/python

import xml.etree.ElementTree as ET
import re
from entitys import Category
from dominate import document
from dominate.tags import *
import dominate
from dominate.tags import *

class Utils:
	def __init__(self, xmlString):
		if xmlString == '':
			pass
		else:
			self.xmlString = xmlString
	
	def getStringXml(self):
		self.xmlString = re.sub('\\sxmlns="[^"]+"', '', self.xmlString, count=1)
		return ET.fromstring(self.xmlString)
	
	def getCategoryList(self, root):
		categoryList = []
		for category in root.findall('./CategoryArray/Category'):
			bestOfferEnabled = category.find('BestOfferEnabled')
			categoryID = category.find('CategoryID')
			categoryParentID = category.find('CategoryParentID')
			categoryLevel = category.find('CategoryLevel')
			categoryName = category.find('CategoryName')
			
			if bestOfferEnabled is not None:
				bestOfferEnabled = category.find('BestOfferEnabled').text
				bestOfferEnabled = bestOfferEnabled.lower()
				if 'true' == bestOfferEnabled:
					bestOfferEnabled = 1
				else:
					bestOfferEnabled = 0
			
			if categoryID is not None:
				categoryID = category.find('CategoryID').text
			else:
				categoryID = None
			
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
				
			item = Category(categoryID, categoryLevel, categoryParentID, categoryName, bestOfferEnabled)
			categoryList.append(item)
		return categoryList
		
	def setHtml(self, categoryID, categoryList):
		# try JSON 
		arrayCollection = '['
		for line in categoryList:
			for i in range(5):
				array = '{'
				if line[i] is not None:
					array += "\'id\': \'" + str(abs(hash(line[i])))+ "\',"
					if i == 0:
						array += "\'parent\': \'#\',"
					if i > 0:
							array += "\'parent\': \'" + str(abs(hash(line[i-1]))) + "\',"
					array += "\'text\': \'" + line[i].replace("'", "&apos;") + "\'"
					if line[i+1] is None:
						array += ",\'icon\': \'/\'"
					array += '},'
					if not array in arrayCollection:
						arrayCollection += array
		arrayCollection += ']'
			
		doc = dominate.document(title='Category ' + categoryID)
		with doc.head:
			link(rel='stylesheet', href='dist/themes/default/style.css')
			script(type='text/javascript', src='dist/jquery-1.12.1.min.js')
			script(type='text/javascript', src='dist/jstree.js')
			doc += script("$(function() {  $('#jstree').jstree({ 'plugins' : ['json_data'], 'core': {  'data': "+ arrayCollection +"  } }); });")
			with doc:
				with div(id='jstree'):
					attr(cls='jstree')
		with open(categoryID + '.html', 'w') as f:
			f.write(doc.render())
		f.closed
