#!/usr/bin/python

import ConfigParser, os
import httplib2
from xml.dom.minidom import parse, parseString
import urlparse
from lxml import etree
import struct
import urllib2
import socket

class Request:
  def __init__(self):
    config = ConfigParser.RawConfigParser()
    config.read('config.ini')
    self.call_name = config.get('keys', 'call-name')
    self.app_name = config.get('keys', 'app-name')
    self.dev_name = config.get('keys', 'dev-name')
    self.cert_name = config.get('keys', 'cert-name')
    self.siteid = config.get('keys', 'siteid')
    self.compatibility_level = config.get('keys', 'compatibility-level')
    self.endpoint = config.get('endpoints', 'url')
    self.view_all_nodes = config.get('keys', 'viewn-all-nodes')
    self.category_site_id = config.get('keys', 'category-site-id')
    self.detai_level = config.get('keys', 'detail-level')
    self.encoding = config.get('keys', 'encoding')
    self.auth_token = config.get('auth', 'token')
        
  def getCategories(self, parentId):
    root = etree.Element("GetCategoriesRequest",xmlns="urn:ebay:apis:eBLBaseComponents")
    credentials_elem = etree.SubElement(root, "RequesterCredentials")
    token_elem = etree.SubElement(credentials_elem, "eBayAuthToken")
    token_elem.text = self.auth_token    
    if parentId > 0:
        parentId_elem = etree.SubElement(root, "CategoryParent")
        parentId_elem.text = str(parentId)
    viewAllNodes_elem = etree.SubElement(root, "ViewAllNodes")
    viewAllNodes_elem.text = str(self.view_all_nodes).lower()
    categorySiteId_elem = etree.SubElement(root, "CategorySiteID")
    categorySiteId_elem.text = str(self.category_site_id)
    if self.detai_level:
        detailLevel_elem = etree.SubElement(root, "DetailLevel")
        detailLevel_elem.text = str(self.detai_level)
    request = etree.tostring(root, pretty_print=False,
                             xml_declaration=True, encoding="utf-8")
    response = getResponse(self, "GetCategories", request)
    return response
    
def getResponse(self, operation_name, data, **headers):
    http_headers = {
        "X-EBAY-API-COMPATIBILITY-LEVEL": self.compatibility_level,
        "X-EBAY-API-DEV-NAME": self.dev_name,
        "X-EBAY-API-APP-NAME": self.app_name,
        "X-EBAY-API-CERT-NAME": self.cert_name,
        "X-EBAY-API-CALL-NAME": operation_name,
        "X-EBAY-API-SITEID": self.siteid,
        'X-EBAY-API-DETAIL-LEVEL': '0',
        "Content-Type": "text/xml"}
    http_headers.update(headers)
    req = urllib2.Request(self.endpoint, data, http_headers)
    res = urllib2.urlopen(req, timeout=150)
    return res.read()
