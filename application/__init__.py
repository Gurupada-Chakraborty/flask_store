from flask import Flask
import pymongo

app = Flask(__name__)
app.config['SECRET_KEY'] = '29d260c3ca9011a17895c3191d95189c47aeed83'
app.config['MONGO_URI'] = 'mongodb+srv://db_mongo_user:mongo_db_2894@cluster0.lw2qew9.mongodb.net/?retryWrites=true&w=majority'

client = pymongo.MongoClient(app.config['MONGO_URI'])

client.test
print("Mongo connection successfull ..")

# db = client['db']
# col = db['stores']


from application import routes