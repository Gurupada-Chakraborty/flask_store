from application import app
from flask import render_template, request, flash, redirect, url_for, jsonify
import pandas as pd
import pymongo
from . import stores

# connecting to mongodb
client = pymongo.MongoClient(app.config['MONGO_URI'])

db = client['db']
col = db['stores']

# default home path
@app.route('/')
def index():
    return render_template("index.html")

# route for saving records from csv file
@app.route('/csvSave',methods = ['POST'])
def upload_route_summary():
    if request.method == 'POST':

        # Create variable for uploaded file
        try :
            # getting uploaded file content
            f = request.files['fileupload']  
            df = pd.read_csv(f)
            csv_dicts = df.to_dict('records')
            list_flag = []
            for i in csv_dicts:
                resp = stores.Stores().set_store_details(i)
                list_flag.append(stores.Stores().add_record(resp))
            # defining messages to be sent through flash to ui
            if list_flag.count(1) == len(list_flag):
                flash(u"Success : Records added !", "success")
            else:
                flash(u"Validation error : {} out of {} records updated !".format(list_flag.count(1), len(list_flag)), "warning")
        except Exception as e:
            flash(u"Error : " +str(e), "danger" )
    return redirect(url_for("index"))

# route for querying the db
@app.route("/query", methods=['POST'])
def query():
    # getting json from UI and processing
    data = request.json
    # data = dict(data)
    qp = {}
    query_dict = {}
    qp[data['fields']] = data['search']
    if "Price" in [k for k,v in qp.items()]:
        qp["Price"] = int(qp["Price"])
        query_dict['price'] = qp["Price"]
    if "Store ID" in [k for k,v in qp.items()]:
        query_dict['store_id'] = qp['Store ID']
    if "SKU" in [k for k,v in qp.items()]:
        query_dict['sku'] = qp['SKU']
    if "Product Name" in [k for k,v in qp.items()]:
        query_dict['product_name'] = qp['Product Name']
    res = list(col.find(query_dict, {"_id":0}))
    return jsonify({'data' : res})