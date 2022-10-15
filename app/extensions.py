from pymongo import MongoClient
import os


class MongoConnect:

    def __init__(self, data):
        # MongoDB connection
        self.client = MongoClient("mongodb://localhost:27017/")
        cursor = self.client.techdb

        self.collection = cursor.gitrepo
        self.data = data

# fetching data
    def read(self):
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'}
                  for data in documents]
        return output

# posting data to collections
    def write(self, data):
        new_document = data
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted'}
        return output
