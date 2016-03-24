#!/usr/bin/python

import ConfigParser, os
import httplib2
from xml.dom.minidom import parse, parseString
import urlparse
from lxml import etree
import struct
import urllib2
import socket
import thread
import threading


class Request(threading.Thread):
	def __init__(self, parent, level, selector):
		threading.Thread.__init__(self)
		config = ConfigParser.RawConfigParser()
		config.read('config.ini')
		self.call_name = config.get('keys', 'call-name')
		self.app_name = config.get('keys', 'app-name')
		self.dev_name = config.get('keys', 'dev-name')
		self.cert_name = config.get('keys', 'cert-name')
		self.siteid = config.get('keys', 'category-site-id')
		self.compatibility_level = config.get('keys', 'compatibility-level')
		self.endpoint = config.get('endpoints', 'url')
		self.view_all_nodes = config.get('keys', 'viewn-all-nodes')
		self.category_site_id = config.get('keys', 'category-site-id')
		self.detai_level = config.get('keys', 'detail-level')
		self.encoding = config.get('keys', 'encoding')
		self.auth_token = config.get('auth', 'token')
		self.level_limit = level
		self.parent = parent
		self.response = None
		self.selector = int(selector)
		self.lock = threading.Lock()

	def run(self):
		try:
			req = self.getCategories(int(self.parent))
			res = self.getResponse(req)
			self.response = res
		finally:
			pass

	def getCategories(self, parent):
		root = etree.Element("GetCategoriesRequest",xmlns="urn:ebay:apis:eBLBaseComponents")
		credentials_elem = etree.SubElement(root, "RequesterCredentials")
		token_elem = etree.SubElement(credentials_elem, "eBayAuthToken")
		token_elem.text = str(self.auth_token)
		
		if parent > 0:
			parentId_elem = etree.SubElement(root, "CategoryParent")
			parentId_elem.text = str(parent)
		
		viewAllNodes_elem = etree.SubElement(root, "ViewAllNodes")
		viewAllNodes_elem.text = str(self.view_all_nodes).lower()
		
		outputselector_categoryID_elem = etree.SubElement(root, "OutputSelector")
		outputselector_categoryID_elem.text = str('CategoryArray.Category.CategoryID')

		outputselector_categoryLevel_elem = etree.SubElement(root, "OutputSelector")
		outputselector_categoryLevel_elem.text = str('CategoryArray.Category.CategoryLevel')
		
		if self.selector > 0:
			#outputselector_categoryLevel_elem = etree.SubElement(root, "OutputSelector")
			#outputselector_categoryLevel_elem.text = str('CategoryArray.Category.CategoryLevel')
			outputselector_categoryParentID_elem = etree.SubElement(root, "OutputSelector")
			outputselector_categoryParentID_elem.text = str('CategoryArray.Category.CategoryParentID')
			outputselector_categoryName_elem = etree.SubElement(root, "OutputSelector")
			outputselector_categoryName_elem.text = str('CategoryArray.Category.CategoryName')
			outputselector_bestOfferEnabled_elem = etree.SubElement(root, "OutputSelector")
			outputselector_bestOfferEnabled_elem.text = str('CategoryArray.Category.BestOfferEnabled')
		
		categorySiteId_elem = etree.SubElement(root, "CategorySiteID")
		categorySiteId_elem.text = str(self.category_site_id)
		
		if self.detai_level:
			detailLevel_elem = etree.SubElement(root, "DetailLevel")
			detailLevel_elem.text = str(self.detai_level)
		
		#if self.selector < 1 and self.level_limit:
		if self.level_limit:
			levelLimit_elem = etree.SubElement(root, "LevelLimit")
			levelLimit_elem.text = str(self.level_limit)

		request = etree.tostring(root, pretty_print=False,xml_declaration=True, encoding="utf-8")
		return request
		
	def getResponse(self, data, **headers):
		http_headers = {"X-EBAY-API-COMPATIBILITY-LEVEL": self.compatibility_level,"X-EBAY-API-DEV-NAME": self.dev_name,"X-EBAY-API-APP-NAME": self.app_name,"X-EBAY-API-CERT-NAME": self.cert_name,"X-EBAY-API-CALL-NAME": self.call_name,"X-EBAY-API-SITEID": self.siteid,"Content-Type": "text/xml"}
		http_headers.update(headers)
		try:
			req = urllib2.Request(self.endpoint, data, http_headers)
			res = urllib2.urlopen(req)
			response = res.read()
			res.close()
			return response
		except Exception as e:
			pass
		
