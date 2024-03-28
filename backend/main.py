from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import yaml
import time
import openai
import fn_call_utils 
import os

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

def insert_term(new_term):
    x = terms.insert_one(new_term)
    return x.inserted_id

def get_term(query):
    documents = terms.find(query)
    return documents

def update_description():
    return




# new_term = {'term': 'DTE', 'descriptions': ['Design Technology Engineering', 'Designated to Entity']}
if __name__ == '__main__':
    docs = get_term({'term': 'DTE'})
    for d in docs:
        print(d)
    print(os.environ.get('OPENAI_API_KEY'))