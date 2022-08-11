from application import app
from flask import render_template, request, flash, redirect, url_for, jsonify
import csv
import pandas as pd
import pymongo
from . import stores

client = pymongo.MongoClient(app.config['MONGO_URI'])

db = client['db']
col = db['stores']


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/csvSave',methods = ['POST'])
def upload_route_summary():
    error = None
    if request.method == 'POST':

        # Create variable for uploaded file
        try :
            f = request.files['fileupload']  

            #store the file contents as a string
            
            # fstring = f.read()
            
            df = pd.read_csv(f)
            
            #create list of dictionaries keyed by header row
            # csv_dicts = [{k: v for k, v in row.items()} for row in csv.DictReader(fstring.splitlines(), skipinitialspace=True)]
            
            csv_dicts = df.to_dict('records')
            
            # col.insert_many(csv_dicts)
            for i in csv_dicts:
                resp = stores.Stores().set_store_details(i)
                stores.Stores().add_record(resp)
            #do something list of dictionaries
            flash(u"Success !!", "success")
        except Exception as e:
            flash(u"Error : " +str(e), "danger" )
    return redirect(url_for("index"))

@app.route("/listall", methods=['GET'])
def fetchall():
    cur = list(col.find({},{'_id':0}))
    return jsonify({'data' : cur})