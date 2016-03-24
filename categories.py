#!/usr/bin/python

import sys, getopt
import ConfigParser
import time
import thread
import threading
from util import Utils
from entitys import Category
from database import Management
from clientws import Request

config = ConfigParser.RawConfigParser()
config.read('config.ini')


def setPool(threads):
	try:
		if int(level) > -1:
			config.set('threads', 'pool', threads)
			with open('config.ini', 'wb') as configfile:
				config.write(configfile)
				return
	except ValueError:
		print "Input takes only positive integers: " + level
		
		
def setLevel(level):
	try:
		if int(level) > -1:
			config.set('keys', 'level-limit', level)
			with open('config.ini', 'wb') as configfile:
				config.write(configfile)
				return
	except ValueError:
		print "Input takes only positive integers: " + level

	 
def setParent(parent):
	try:
		if int(parent) > -1:
			config.set('keys', 'parent-id', parent)
			with open('config.ini', 'wb') as configfile:
				config.write(configfile)
				return
	except ValueError:
		print "Input takes only positive integers: " + parent	

	
def render(categoryId):
	try:
		managment = Management()
		message = managment.existCategory(categoryId)
		if message == 1:
			util = Utils('')
			level = int(config.get('keys', 'level-limit'))
			template = config.get('template', 'folder')
			query = util.getQuery(level)
			all_rows = managment.getCategory(categoryId, query)
			util.setHtml(categoryId, all_rows, level, template)
		else:
			print(message)	
	except Exception as e:
  		raise e


def getCategoryPartLists(parent, response):
	categoryList = []
	util = Utils(response)
	root = util.getStringXml()
	categoryList = util.getCategoryList(root, parent)
	return categoryList
	
def getListJoinThreadx(parent, queue):
	categoryList = []
	for thread in queue:
		thread.join()
		if thread.response is not None:
			categoryList.extend(getCategoryPartLists(parent, thread.response))
			thread.response = None
	return categoryList
	
def getFullList(categoryPartList, parent, level_limit):
	queue = []
	parentItem = None
	categoryList = []
	pool = int(config.get('threads', 'pool'))
	if len(categoryPartList) == 1:
		parent = -1
	for item in categoryPartList:
		if item.categoryID <> parent:
			thread = Request(item.categoryID, level_limit, 1)
			thread.start()
			queue.append(thread)
			if (len(queue) % pool) == 0:
				categoryList.extend(getListJoinThreadx(None, queue))
				queue = []
		else:
			parentItem = item
	if len(queue) > 0:
		categoryList.extend(getListJoinThreadx(None, queue))
		queue = []
	if parent <> -1:
		categoryList.append(parentItem)
	return categoryList
	
	
def __rebuild():
	parentItem = None
	queue = []
	categoryList = []
	categoryPartList = []
	level_limit = config.get('keys', 'level-limit')
	parent = config.get('keys', 'parent-id')
	pool = int(config.get('threads', 'pool'))
	if level_limit > 1:
		thread = Request(parent, 1, 0)
		thread.start()
		thread.join()
		if thread.response is not None:
			categoryPartList = getCategoryPartLists(parent, thread.response)
			thread.response = None
			if len(categoryPartList) > 0:
				categoryList.extend(getFullList(categoryPartList, parent, level_limit))
	categories = categoryList		
	managment = Management()
	managment.createTable()
	util = Utils('')
	categories = util.listToInsert(categories)
	managment.isertList(categories)

	
def main(argv):
   try:
   	opts, args = getopt.getopt(argv, "b:l:p:r:h", ["rebuild","level","parent","render", "help"])
   except getopt.GetoptError:
      print '-h --help'
      sys.exit(2)
   for opt, arg in opts:
      if opt in ("-h", "--help"):
      	print '-----------------------------------------------------'
      	print 'categories --rebuild'
      	print 'categories --render <category_id>'
      	print 'categories -h | categories --help'
      	print 'categories --level <LevelLimit>'
      	print 'categories --parent <CategoryParent>'
      	print 'categories --pool <threeds>'
      	print '             level | LevelLimit 6 default value'
      	print '             parent | CategoryParent 0 default value'
      	print '             pool | Threads 350 default value'
      	print '-----------------------------------------------------'
      	sys.exit()
      elif opt == '--rebuild':
      	#start_time = time.time()
      	__rebuild()
      	#print(" %s seconds " % (time.time() - start_time))
      elif opt == '--level':
      	setLevel(args[:1][0])
      elif opt == '--pool':
      	setPool(args[:1][0])
      elif opt == '--parent':
      	setParent(args[:1][0])
      elif opt == '--render':
      	render(args[:1][0])
       
	  
if __name__ == "__main__":
   main(sys.argv[1:])
