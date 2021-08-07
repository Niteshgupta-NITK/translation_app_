from flask import Flask
# from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
# cors = CORS(app);
app.config['SECRET_KEY'] = 'hbidh3r9yygc'
# client = MongoClient()

# db = client.data
# 
# database = db.dataBase






from app import routes