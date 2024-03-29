from __future__ import annotations
from typing import Any
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import yaml
import time
import openai
import fn_call_utils 
import os
from bson.objectid import ObjectId

with open("C:/Workspace/Jargis/Jargis-Backend/backend/config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

uri = f"mongodb+srv://brianezinwoke:{config['db']['password']}@cluster0.cfdfcjs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

print(client.list_database_names())
db = client["Jargis"]
terms = db["terms"]
categories = db["categories"]

def get_categoryID(category:str) -> str | None:
    x = categories.find_one(filter={'name':category.lower()})
    try:
        return x['_id']
    except TypeError:
        return None

def add_term(term: str, definition: str, categories: list[str] = ['all'], verfication: str = "unverified") -> int:
    category_list = []
    for c in categories:
        cid = get_categoryID(c)
        if cid:
            category_list.append(cid)
        else:
            print('Could not find category. Use add_category() to create a new category')

    if category_list is None:
        category_list.append(get_categoryID)

    new_term = {'term': term,
                'definitions': [{'_id': ObjectId(), 
                                'definition': definition,
                                'categories': category_list,  # type: ignore
                                'flagged': False, 
                                'verification': verfication,
                                'alternate_defintions': []}],
                'search_count': 0
                }
    x = terms.insert_one(new_term)
    return x.inserted_id

def get_term(query):
    documents = terms.find(query)
    return documents

def update_definition():
    return

def add_definition():
    pass



# new_term = {'term': 'DTE', 'descriptions': ['Design Technology Engineering', 'Designated to Entity']}
if __name__ == '__main__':
    docs = get_term({'term': 'DTE'})
    for d in docs:
        print(d["_id"])
    print(categories.find_one({'name':'Technology'}))
    print(get_categoryID('Technolo'))

    # print(os.environ.get('OPENAI_API_KEY'))