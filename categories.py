#!/usr/bin/python

import sys, getopt
from clientws import Request
from util import Utils
from entitys import Category
from database import Management

def render(categoryId):
	try:
		managment = Management()
		message = managment.existCategory(categoryId)
		if message == 1:
			all_rows = managment.getCategory(categoryId)
			util = Utils('')
			util.setHtml(categoryId, all_rows)
		else:
			print(message)	
	except Exception as e:
  		raise e
  		
def rebuild():
	try:
		request = Request()
		response = request.getCategories(10542)
		util = Utils(response)
		root = util.getStringXml()
		categoryList = []
		categoryList = util.getCategoryList(root)
		managment = Management()
		managment.createTable()
		managment.isertList(categoryList)
	except Exception as e:
  		raise e

def main(argv):
   try:
   	opts, args = getopt.getopt(argv, "b:r:h", ["rebuild","render", "help"])
   except getopt.GetoptError:
      print '-h --help'
      sys.exit(2)
   for opt, arg in opts:
      if opt in ("-h", "--help"):
         print 'categories --rebuild'
         print 'categories --render <category_id>'
         print 'categories -h | categories --help'
         sys.exit()
      elif opt == '--rebuild':
         rebuild()
      elif opt == '--render':
      	render(args[:1][0])
         
if __name__ == "__main__":
   main(sys.argv[1:])