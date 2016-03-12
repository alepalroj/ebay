#!/usr/bin/python

class Category(object):
  def __init__(self, categoryID, categoryLevel, categoryParentID, categoryName, bestOfferEnabled):
  		self.categoryID = categoryID
  		self.categoryLevel = categoryLevel
  		self.categoryParentID = categoryParentID
  		self.categoryName = categoryName
  		self.bestOfferEnabled = bestOfferEnabled