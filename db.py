import pymongo
from bson.objectid import ObjectId

class database():

	def __init__(self):
		self.host = "localhost"
		self.port = "27017"
		self.database = "Security_News"

	def __connect__(self):
		self.client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
		self.db = self.client[self.database]
	
	def __disconnect__(self):
		self.client.close()

	def findall(self, coll , reg=None):
		self.__connect__()
		col = self.db[coll]
		return col.find({},reg)

	def find(self, coll, param):
		self.__connect__()
		col = self.db[coll]
		return col.find(param)

	def insert(self, data, coll):
		self.__connect__()
		col = self.db[coll]
		try:
			col.insert_many(data)
			return True
		except Exception as e:
			return str(e)

	def update(self, key, data, coll):
		self.__connect__()
		col = self.db[coll]
		try:
			col.update(key,data,upsert=True)
			return True
		except Exception as e:
			return str(e)

	def delete(self, data, coll):
		self.__connect__()
		col = self.db[coll]
		try:
			col.delete_one(data)
			return True
		except Exception as e:
			return str(e)

	def drop_coll(self, coll):
		self.__connect__()
		col = self.db[coll]
		col.drop()