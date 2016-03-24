import sqlite3
import ConfigParser, os
from entitys import Category

class Management:	
  def __init__(self):
    config = ConfigParser.RawConfigParser()
    config.read('config.ini')
    self.name = config.get('database', 'name')
	
  def createTable(self):
  	try:
  		db = sqlite3.connect(self.name)
  		cursor = db.cursor()
  		cursor.execute('''DROP TABLE IF EXISTS category''')
  		cursor.execute('''CREATE TABLE category(categoryID TEXT PRIMARY KEY, categoryLevel TEXT, categoryParentID TEXT, categoryName TEXT, bestOfferEnabled BOOLEAN)''')
  		db.commit()
  	except Exception as e:
  		db.rollback()
  		print e 
  		pass
  	finally:
  		db.close()

  def isertList(self, categories):
  	try:
  		db = sqlite3.connect(self.name)
  		cursor = db.cursor()
  		cursor.executemany('''INSERT INTO category(categoryID, categoryLevel, categoryParentID, categoryName, bestOfferEnabled) VALUES (?,?,?,?,?)''', categories)
  		db.commit()
  	except Exception as e:
  		db.rollback()
  	finally:
  		db.close()

  def existCategory(self, categoryId):
  	try:
  		db = sqlite3.connect(self.name)
  		cursor = db.cursor()
  		cursor.execute(""" SELECT 1 FROM category WHERE categoryID = ?  """, (categoryId, ))
  		category = cursor.fetchone()
		if category == None:
			return "No category with ID: " + categoryId
		else:
			return 1
  	except Exception as e:
  		print e
  		pass
  	finally:
  		db.close()
  		
  def getCategory(self, categoryId, query):
  	try:
  		db = sqlite3.connect(self.name)
  		cursor = db.cursor()
  		cursor.execute(query, (categoryId, ))
		all_rows = cursor.fetchall()
  		return all_rows
  	except Exception as e:
  		print e 
  		pass
  	finally:
  		db.close()
