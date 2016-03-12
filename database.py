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
  		cursor.execute('''CREATE TABLE category(ID INTEGER PRIMARY KEY AUTOINCREMENT, categoryID TEXT, categoryLevel TEXT, categoryParentID TEXT, categoryName TEXT, bestOfferEnabled BOOLEAN)''')
  		db.commit()
  	except Exception as e:
  		db.rollback()
  		raise e
  	finally:
  		db.close()

  def isertList(self, categoryList = []):
  	try:
  		db = sqlite3.connect(self.name)
  		for obj in categoryList:
  			with db:
  				db.execute('''INSERT INTO category(categoryID, categoryLevel, categoryParentID, categoryName, bestOfferEnabled) VALUES (?,?,?,?,?)''', (obj.categoryID, obj.categoryLevel, obj.categoryParentID, obj.categoryName, obj.bestOfferEnabled))
  	except Exception as e:
  		db.rollback()
  		raise e
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
  		raise e
  	finally:
  		db.close()
  		
  def getCategory(self, categoryId):
  	try:
  		db = sqlite3.connect(self.name)
  		cursor = db.cursor()
  		"""  maximum depth of six and contains 34 top-level """
  		cursor.execute("""SELECT category1.categoryName AS level1, category2.categoryName AS level2, category3.categoryName AS level3, category4.categoryName AS level4, category5.categoryName AS level5, category6.categoryName AS level6
FROM category AS category1 LEFT JOIN category AS category2 ON category2.categoryParentID = category1.categoryId LEFT JOIN category AS category3 ON category3.categoryParentID = category2.categoryId LEFT JOIN category AS category4 ON category4.categoryParentID = category3.categoryId LEFT JOIN category AS category5 ON category5.categoryParentID = category4.categoryId LEFT JOIN category AS category6 ON category6.categoryParentID = category5.categoryId WHERE category1.categoryId = ?""", (categoryId, ))
		all_rows = cursor.fetchall()
  		return all_rows
  	except Exception as e:
  		raise e
  	finally:
  		db.close()
